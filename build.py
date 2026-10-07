#!/usr/bin/env python3
"""
Rebuild the PlayerSells open datasets.

    python build.py              # CSVs and docs from the snapshots in sources/
    python build.py --refresh    # first re-read the sources, then build
    python build.py --stage      # also assemble dist/hf/<slug> and dist/kaggle/<slug>

Every CSV is written from a file in sources/. --refresh re-creates those files
from where the numbers are published:

  * live pages on playersells.com (article tables, the X benchmark page and
    its JSON), so the open data cannot disagree with what the site shows;
  * the PlayerSells repository (rank ladders and the Telegram benchmark, which
    are checked-in constants there), when PLAYERSELLS_REPO points at it;
  * the analysis exports behind the Kick and Twitch reports, when
    PLAYERSELLS_OUTREACH points at them. Absolute viewer totals are dropped on
    the way in: the reports publish shares, not totals.

A source that cannot be reached keeps its existing snapshot. After building,
a set of checks compares headline numbers with the published pages and the
build fails if any of them moved.

Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import re
import shutil
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import spec  # noqa: E402

SRC = ROOT / "sources"
OUT = ROOT / "datasets"
HF = ROOT / "hf"
DIST = ROOT / "dist"
SITE = spec.SITE

# Private inputs for --refresh, not part of the published repo: point these at
# the site checkout and the research folder, or link them under _local/.
REPO = Path(os.environ.get("PLAYERSELLS_REPO", ROOT / "_local" / "repo"))
OUTREACH = Path(os.environ.get("PLAYERSELLS_OUTREACH", ROOT / "_local" / "outreach"))

PAGES = {
    "kick-gambling": "/learn/how-much-of-kick-is-gambling-one-week-measured-against-twitch",
    "crypto-telegram": "/learn/crypto-telegram-channels-are-losing-subscribers-measured",
    "x-premium": "/learn/does-x-premium-increase-reach-60000-accounts-compared",
    "simulcast": "/learn/kick-and-twitch-simulcasting-measured-where-viewers-watch",
    "x-engagement-benchmarks": "/insights/engagement-rate-benchmarks",
}
X_INSIGHTS_JSON = "/insights/data.json"
# Kaggle dataset ids are <owner>/<slug>; the owner is the Kaggle username or organisation.
KAGGLE_OWNER = os.environ.get("KAGGLE_OWNER", "playersells")

# Platform facts the rank tools print. framing and path are re-read from the
# repository on --refresh; the rest is wording.
RANK_META = {
    "x": ("X (Twitter)", "account", "followers"),
    "bluesky": ("Bluesky", "account", "followers"),
    "telegram": ("Telegram", "channel", "subscribers"),
    "tiktok": ("TikTok", "creator", "followers"),
    "youtube": ("YouTube", "channel", "subscribers"),
    "kick": ("Kick", "channel", "followers"),
    "twitch": ("Twitch", "channel", "followers"),
}
RANK_COVERAGE = {
    "x": "A sample of the X accounts in the PlayerSells index. The index has a long tail of small accounts but is not a census of X.",
    "bluesky": "A sample of the Bluesky accounts in the PlayerSells index, which is built from Bluesky's public firehose and follow graph.",
    "telegram": "A sample of the public Telegram channels in the PlayerSells index. Private channels are missing.",
    "tiktok": "Every creator in the PlayerSells TikTok catalog, which was seeded from creators that other creators reference. Not representative of TikTok as a whole.",
    "youtube": "Every channel in the PlayerSells YouTube catalog, which was seeded from larger channels. Not representative of YouTube as a whole.",
    "kick": "Kick channels PlayerSells has recorded going live whose follower count has been read. Not every registered account.",
    "twitch": "Twitch channels PlayerSells has recorded going live. Not every registered account.",
}

KICK_GAMBLING = {"slots", "poker", "sports-betting"}
TWITCH_GAMBLING = {"Slots", "Poker", "Virtual Casino"}
MIN_CHANNELS = 5


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def log(msg: str) -> None:
    print(msg, flush=True)


def fetch(path: str) -> str | None:
    url = SITE + path
    req = urllib.request.Request(url, headers={"User-Agent": "playersells-open-data/1.0 (+https://playersells.com)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8")
    except Exception as e:  # network down, 5xx, timeout: keep the old snapshot
        log(f"  ! could not fetch {url}: {e}")
        return None


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, header: list[str], rows: list[list]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def num(text: str):
    """'11,403' -> 11403, '85.6%' -> 85.6, '-6.50%' -> -6.5, '1.58x' -> 1.58, '' -> None."""
    t = text.strip().replace(",", "").replace("%", "").replace("x", "").replace("+", "")
    if t == "":
        return None
    try:
        v = float(t)
    except ValueError:
        return None
    return int(v) if re.fullmatch(r"-?\d+", t) else v


def ts_object(src: str, marker: str) -> dict:
    """Turn the object literal that follows `marker` in a TypeScript file into a dict."""
    start = src.index(marker)
    start = src.index("{", start + len(marker) - 1)
    depth, i = 0, start
    while True:
        c = src[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    body = src[start:i + 1]
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
    body = re.sub(r"(?m)^\s*//.*$", "", body)
    body = re.sub(r"(?<=\d)_(?=\d)", "", body)
    body = re.sub(r"(?m)(^|[{,\s])([A-Za-z_]\w*)\s*:", r'\1"\2":', body)
    body = re.sub(r",(\s*[}\]])", r"\1", body)
    return json.loads(body)


class TableParser(HTMLParser):
    """Collects every <table> on a page as {header: [...], rows: [[...]]}."""

    def __init__(self):
        super().__init__()
        self.tables: list[dict] = []
        self._t = None
        self._row = None
        self._cell = None
        self._in_head = False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._t = {"header": [], "rows": []}
        elif self._t is not None:
            if tag == "thead":
                self._in_head = True
            elif tag == "tr":
                self._row = []
            elif tag in ("td", "th"):
                self._cell = []

    def handle_endtag(self, tag):
        if self._t is None:
            return
        if tag in ("td", "th") and self._cell is not None:
            self._row.append(re.sub(r"\s+", " ", "".join(self._cell)).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if self._in_head:
                self._t["header"] = self._row
            else:
                self._t["rows"].append(self._row)
            self._row = None
        elif tag == "thead":
            self._in_head = False
        elif tag == "table":
            self.tables.append(self._t)
            self._t = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def page_tables(html: str) -> list[dict]:
    p = TableParser()
    p.feed(html)
    return p.tables


def table(key: str, first_header: str) -> dict:
    """The table on a snapshotted page whose first column is `first_header`."""
    snap = read_json(SRC / "pages" / f"{key}.json")
    for t in snap["tables"]:
        if t["header"] and t["header"][0] == first_header:
            return t
    raise SystemExit(f"table '{first_header}' not found on {key}: has "
                     + ", ".join(repr(t['header'][:1]) for t in snap['tables']))


# --------------------------------------------------------------------------
# refresh: re-read the sources into sources/
# --------------------------------------------------------------------------

def refresh() -> None:
    log("refresh: pages on playersells.com")
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for key, path in PAGES.items():
        html = fetch(path)
        if html is None:
            continue
        # Tables that name individual accounts or channels stay on the site only.
        tables = [t for t in page_tables(html) if not (t["header"] and t["header"][0] in ("Account", "Channel"))]
        extra = {}
        if key == "x-engagement-benchmarks":
            text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html))
            m = re.search(r"measured over the 30 days to (\d{1,2} \w+ \d{4})", text)
            extra["window_end_text"] = m.group(1) if m else None
            m = re.search(r"Across ([\d,]+) measured X accounts \(([^)]+)\)", text)
            extra["population_text"] = m.group(0).replace(" )", ")") if m else None
        write_json(SRC / "pages" / f"{key}.json",
                   {"url": SITE + path, "retrieved_at": now, **extra, "tables": tables})
        log(f"  {key}: {len(tables)} tables")

    raw = fetch(X_INSIGHTS_JSON)
    if raw is not None:
        d = json.loads(raw)
        keep = {k: d.get(k) for k in ("object", "url", "computedAt", "windowDays", "license",
                                      "citation", "methodology", "uncertainty", "findings", "notes")}
        write_json(SRC / "x_insights_data.json", keep)
        log(f"  x insights json: {len(d.get('findings', []))} findings")

    ar = REPO / "src" / "lib" / "audience-rank.ts"
    if ar.exists():
        src = ar.read_text(encoding="utf-8")
        baked = ts_object(src[src.index("const BAKED"):], "> = {")
        meta = {}
        for m in re.finditer(r'key:\s*"(\w+)".*?framing:\s*"(\w+)".*?path:\s*"([^"]+)"', src, re.S):
            meta[m.group(1)] = {"framing": m.group(2), "path": m.group(3)}
        write_json(SRC / "rank_ladders.json", {"source": "src/lib/audience-rank.ts", "ladders": baked, "meta": meta})
        log(f"  rank ladders: {', '.join(baked)}")
    else:
        log(f"  ! {ar} not found, keeping sources/rank_ladders.json")

    tb = REPO / "src" / "app" / "(en)" / "telegram-engagement-rate" / "_data" / "benchmark.ts"
    if tb.exists():
        bench = ts_object(tb.read_text(encoding="utf-8"), "TELEGRAM_REACH_BENCHMARK: ReachBenchmarkEdition = {")
        write_json(SRC / "telegram_reach_benchmark.json", bench)
        log(f"  telegram benchmark: {bench['edition']}")
    else:
        log(f"  ! {tb} not found, keeping sources/telegram_reach_benchmark.json")

    kt = OUTREACH / "research-2026-10-03" / "kick_twitch_week_2026-09-26"
    if kt.exists():
        rows = []
        for name in ("kick_category_share.csv", "twitch_category_share.csv"):
            lines = [l for l in (kt / name).read_text(encoding="utf-8").splitlines()
                     if l and not l.startswith("Output format")]
            for r in csv.DictReader(io.StringIO("\n".join(lines))):
                rows.append([r["platform"], r["period"], r["category"], r["share_pct"], r["channels"]])
        write_csv(SRC / "kick_twitch_category_share_2026-09-26.csv",
                  ["platform", "period", "category", "share_pct", "channels"], rows)
        log(f"  kick/twitch category shares: {len(rows)} rows (viewer totals dropped)")
    else:
        log(f"  ! {kt} not found, keeping the snapshot")

    sr = OUTREACH / "research-2026-10-05" / "report2" / "results.json"
    if sr.exists():
        d = read_json(sr)
        drop_keys = {"top_simulcasters"}
        keep = {}
        for k, v in d.items():
            if k in drop_keys or "viewer_hours" in k:
                continue
            if isinstance(v, list):
                v = [{kk: vv for kk, vv in row.items() if "viewer_hours" not in kk} for row in v]
            keep[k] = v
        # Rank order is kept; the absolute viewing it was ranked by is not.
        keep["by_category"] = [dict(row, rank=i + 1) for i, row in enumerate(keep["by_category"])]
        keep["kick_category_simulcast_share"] = [
            dict(row, rank=i + 1) for i, row in enumerate(keep["kick_category_simulcast_share"])]
        write_json(SRC / "simulcast_2026-09-28.json", keep)
        log("  simulcast results (names and viewer-hour totals dropped)")
    else:
        log(f"  ! {sr} not found, keeping the snapshot")


# --------------------------------------------------------------------------
# build: one function per dataset, each returns {file: row count}
# --------------------------------------------------------------------------

def build_follower_percentiles(d: Path) -> dict:
    src = read_json(SRC / "rank_ladders.json")
    rows, plat = [], []
    for p, (label, unit, metric) in RANK_META.items():
        L = src["ladders"][p]
        meta = src["meta"].get(p, {})
        when = L.get("computedAt")
        q = L["quantiles"]
        assert len(q) == 101, p
        for i in range(100):          # p100 left out on purpose, see README
            rows.append([p, i, q[i], metric, when])
        for pct, val in L.get("tail") or []:
            rows.append([p, pct, val, metric, when])
        plat.append([p, label, unit, metric, meta.get("framing"), L["sampleSize"], L["indexedTotal"],
                     when, RANK_COVERAGE[p], SITE + meta.get("path", "")])
    return {
        "follower_percentiles.csv": write_csv(d / "follower_percentiles.csv",
                                              ["platform", "percentile", "value", "metric", "measured_on"], rows),
        "platforms.csv": write_csv(d / "platforms.csv",
                                   ["platform", "label", "unit", "metric", "framing", "sample_size",
                                    "indexed_total", "measured_on", "coverage_note", "method_url"], plat),
    }


def build_kick_twitch_viewing(d: Path) -> dict:
    src = list(csv.DictReader((SRC / "kick_twitch_category_share_2026-09-26.csv").open(encoding="utf-8")))
    groups: dict[tuple, list] = {}
    for r in src:
        groups.setdefault((r["platform"], r["period"]), []).append(r)
    rows = []
    for (platform, period) in sorted(groups, key=lambda k: (k[0], k[1] != "week", k[1])):
        g = groups[(platform, period)]
        gamb = KICK_GAMBLING if platform == "kick" else TWITCH_GAMBLING
        small_share, small_n = 0.0, 0
        for r in sorted(g, key=lambda r: -float(r["share_pct"])):
            ch = int(r["channels"])
            cat = r["category"].replace("\ufffd", "'")
            if ch < MIN_CHANNELS or not cat:
                small_share += float(r["share_pct"])
                small_n += 1
                continue
            rows.append([platform, period, cat, r["share_pct"], ch, str(cat in gamb).lower()])
        if small_n:
            rows.append([platform, period, f"(other: {small_n} categories with fewer than {MIN_CHANNELS} channels)",
                         f"{small_share:.3f}", "", "false"])
    out = {"category_viewing_share.csv": write_csv(
        d / "category_viewing_share.csv",
        ["platform", "period", "category", "share_of_viewing_pct", "channels", "is_gambling"], rows)}

    t = table("kick-gambling", "Category")
    g_rows = []
    for r in t["rows"]:
        g_rows.append([r[0], num(r[1]), num(r[2])])
    g_rows = [r for r in g_rows if not r[0].startswith("Channels live")]
    out["gambling_share_week.csv"] = write_csv(
        d / "gambling_share_week.csv",
        ["category", "kick_share_of_viewing_pct", "twitch_share_of_viewing_pct"], g_rows)

    t = table("kick-gambling", "Measure (30 days to October 3, 2026)")
    out["rank_comparison_30d.csv"] = write_csv(
        d / "rank_comparison_30d.csv", ["measure", "twitch", "kick"],
        [[r[0], num(r[1]), num(r[2])] for r in t["rows"]])
    return out


def build_simulcast(d: Path) -> dict:
    s = read_json(SRC / "simulcast_2026-09-28.json")
    summary = [
        ["names_live_on_both_platforms", s["handles_on_both_platforms"], "count", "Same name live on Kick and on Twitch at some point in the week"],
        ["names_overlapping_one_hour_or_more", s["handles_overlap_ge_4_slots"], "count", "Live in the same 15-minute block for at least four blocks"],
        ["simulcasters", s["simulcasters"], "count", "Of those, in matching categories in at least half of the blocks"],
        ["hours_live_on_both_all_simulcasters", s["overlap_hours_total"], "hours", ""],
        ["median_hours_live_on_both_per_simulcaster", s["overlap_hours_median"], "hours", ""],
        ["median_share_of_twitch_time_also_live_on_kick", s["overlap_share_of_twitch_time_median_pct"], "percent", "Per streamer"],
        ["kick_share_of_combined_viewers", s["split_kick_share_of_combined_pct"], "percent", "All simulcasters pooled"],
        ["median_streamer_kick_share", s["split_median_kick_share_pct"], "percent", "Per streamer"],
        ["simulcasters_with_most_viewers_on_twitch", s["split_majority_on_twitch"], "count", ""],
        ["simulcasters_with_most_viewers_on_kick", s["split_majority_on_kick"], "count", ""],
        ["twitch_channels_observed", s["twitch_channels_observed"], "count", "Streams that reached the top 30 of their category"],
        ["twitch_channels_observed_2h_or_more", s["twitch_channels_observed_ge_2h"], "count", ""],
        ["twitch_channels_2h_or_more_that_simulcast", s["twitch_ge_2h_simulcasters"], "count", ""],
        ["share_of_observed_twitch_viewing_that_was_simulcast", s["twitch_viewing_share_simulcast_pct"], "percent", ""],
        ["kick_channels_observed", s["kick_channels_observed"], "count", ""],
        ["kick_channels_live_2h_or_more", s["kick_channels_ge_2h"], "count", ""],
        ["kick_channels_2h_or_more_that_simulcast_min", s["kick_ge_2h_simulcasters"], "count", "Minimum"],
        ["share_of_kick_viewing_that_was_simulcast_min", s["kick_viewing_share_simulcast_pct"], "percent", "Minimum"],
        ["check_full_read_blocks_share_of_simulcast_blocks", s["unc_share_of_simulcast_slots_uncapped_pct"], "percent", "Blocks where the Twitch category had under 30 live streams"],
        ["check_full_read_simulcasters", s["unc_simulcasters_with_ge4_uncapped_slots"], "count", ""],
        ["check_full_read_kick_share_of_combined_viewers", s["unc_split_kick_share_of_combined_pct"], "percent", ""],
        ["check_full_read_median_streamer_kick_share", s["unc_split_median_kick_share_pct"], "percent", ""],
        ["check_loose_rules_simulcasters", s["sens_ov_pm1_ge4_any_category"], "count", "15-minute timing tolerance, any category"],
        ["check_strict_rules_simulcasters", s["sens_strict_ov_ge8_agree_ge75"], "count", "Two hours of overlap, categories matching in three quarters"],
    ]
    out = {"summary.csv": write_csv(d / "summary.csv", ["measure", "value", "unit", "note"], summary)}
    out["kick_share_distribution.csv"] = write_csv(
        d / "kick_share_distribution.csv", ["kick_share_band", "simulcasters"],
        [[r["kick_share"], r["simulcasters"]] for r in s["kick_share_distribution"]])
    out["split_by_audience_size.csv"] = write_csv(
        d / "split_by_audience_size.csv",
        ["avg_combined_viewers_band", "simulcasters", "kick_share_of_combined_viewers_pct"],
        [[r["avg_combined_viewers"], r["simulcasters"], r["kick_share_pct"]] for r in s["split_by_size"]])
    tops = []
    for n in (10, 50, 100, 500, 1000):
        tops.append([n, s[f"twitch_top{n}_simulcasters"], s[f"kick_top{n}_simulcasters_lower_bound"]])
    out["top_channels_simulcasting.csv"] = write_csv(
        d / "top_channels_simulcasting.csv",
        ["top_n", "twitch_channels_simulcasting_on_kick", "kick_channels_simulcasting_on_twitch_min"], tops)
    out["twitch_category_split.csv"] = write_csv(
        d / "twitch_category_split.csv",
        ["rank_by_simulcast_viewing", "twitch_category", "simulcasters", "kick_share_of_combined_viewers_pct"],
        [[r["rank"], r["category"], r["simulcasters"], r["kick_share_pct"]]
         for r in s["by_category"] if r["simulcasters"] >= 10])
    out["kick_category_simulcast_share.csv"] = write_csv(
        d / "kick_category_simulcast_share.csv",
        ["rank_by_kick_viewing", "kick_category", "simulcast_share_of_category_viewing_min_pct"],
        [[r["rank"], r["kick_category"], r["simulcast_share_pct"]] for r in s["kick_category_simulcast_share"]])
    return out


def build_telegram_change(d: Path) -> dict:
    t = table("crypto-telegram", "Category")
    rows = [[r[0], num(r[1]), num(r[2]), num(r[3]), num(r[4])] for r in t["rows"]]
    out = {"subscriber_change_by_category.csv": write_csv(
        d / "subscriber_change_by_category.csv",
        ["category", "channels", "lost_subscribers_pct", "gained_subscribers_pct", "median_change_pct"], rows)}
    t = table("crypto-telegram", "Starting size")
    cats = [h.split(":")[0].strip() for h in t["header"][1:]]
    rows = []
    for r in t["rows"]:
        for cat, cell in zip(cats, r[1:]):
            m = re.match(r"([\d.]+)% \(n=([\d,]+)\)", cell)
            if m:
                rows.append([r[0], cat, num(m.group(2)), float(m.group(1))])
            else:
                rows.append([r[0], cat, None, None])
    out["shrink_rate_by_size.csv"] = write_csv(
        d / "shrink_rate_by_size.csv", ["starting_size_band", "category", "channels", "lost_subscribers_pct"], rows)
    return out


def build_telegram_reach(d: Path) -> dict:
    b = read_json(SRC / "telegram_reach_benchmark.json")
    pct = lambda v: round(v * 100, 3)  # noqa: E731
    rows = []
    for band in b["bands"]:
        rows.append([band["key"], band["minSubs"], band["maxSubs"], band["n"], pct(band["p10"]), pct(band["p25"]),
                     pct(band["p50"]), pct(band["p75"]), pct(band["p90"]), band["medianViews"]])
    rows.append(["all", b["minSubs"], None, b["total"]["n"], None, None, pct(b["total"]["p50"]), None, None, None])
    out = {"reach_by_size.csv": write_csv(
        d / "reach_by_size.csv",
        ["band", "min_subscribers", "max_subscribers", "channels", "p10_reach_pct", "p25_reach_pct",
         "median_reach_pct", "p75_reach_pct", "p90_reach_pct", "median_views_per_post"], rows)}
    out["reach_by_niche.csv"] = write_csv(
        d / "reach_by_niche.csv", ["niche", "channels", "median_reach_pct"],
        [[r["category"], r["n"], pct(r["p50"])] for r in b["niches"]["rows"]])
    return out


def build_x_premium(d: Path) -> dict:
    t = table("x-premium", "Follower band")
    out = {}
    rows = []
    for r in t["rows"]:
        lo, hi = [num(x) for x in r[5].split(" to ")]
        rows.append([r[0], num(r[1]), num(r[2]), num(r[3]), num(r[4]), lo, hi, num(r[6])])
    out["reach_by_follower_band.csv"] = write_csv(
        d / "reach_by_follower_band.csv",
        ["follower_band", "accounts", "median_followers", "median_views_per_post", "views_per_follower_pct",
         "views_per_follower_p25_pct", "views_per_follower_p75_pct", "engagement_per_follower_pct"], rows)

    snap = read_json(SRC / "pages" / "x-premium.json")
    t = next(t for t in snap["tables"] if t["header"][:2] == ["Follower band", "Premium accounts"])
    rows = []
    for r in t["rows"]:
        m = re.match(r"(.*?)\s*\((.*)\)$", r[0])
        band, note = (m.group(1), m.group(2)) if m else (r[0], "")
        rows.append([band, note, num(r[1]), num(r[2]), num(r[3]), num(r[4]), num(r[5])])
    out["premium_vs_no_badge.csv"] = write_csv(
        d / "premium_vs_no_badge.csv",
        ["follower_band", "band_note", "premium_accounts", "no_badge_accounts",
         "premium_views_per_follower_pct", "no_badge_views_per_follower_pct", "ratio"], rows)

    t = next(t for t in snap["tables"] if t["header"][:2] == ["Follower band", "Posts per day"])
    out["premium_by_posting_rate.csv"] = write_csv(
        d / "premium_by_posting_rate.csv",
        ["follower_band", "posts_per_day", "premium_accounts", "no_badge_accounts",
         "premium_views_per_follower_pct", "no_badge_views_per_follower_pct"],
        [[r[0], r[1], num(r[2]), num(r[3]), num(r[4]), num(r[5])] for r in t["rows"]])
    return out


def build_x_engagement(d: Path) -> dict:
    snap = read_json(SRC / "pages" / "x-engagement-benchmarks.json")
    end = dt.datetime.strptime(snap["window_end_text"], "%d %B %Y").date().isoformat()
    accounts = num(re.search(r"Across ([\d,]+)", snap["population_text"]).group(1))
    key = {"10th percentile": "p10", "25th percentile": "p25", "50th percentile (median)": "p50",
           "75th percentile": "p75", "90th percentile": "p90", "Mean": "mean"}
    t = table("x-engagement-benchmarks", "Percentile")
    out = {"engagement_rate_percentiles.csv": write_csv(
        d / "engagement_rate_percentiles.csv", ["statistic", "engagement_rate_pct", "accounts", "window_end"],
        [[key[r[0]], num(r[1]), accounts, end] for r in t["rows"]])}
    t = table("x-engagement-benchmarks", "Follower band")
    out["engagement_rate_by_follower_band.csv"] = write_csv(
        d / "engagement_rate_by_follower_band.csv",
        ["follower_band", "accounts", "p25_engagement_rate_pct", "median_engagement_rate_pct",
         "p75_engagement_rate_pct", "window_end"],
        [[r[0], num(r[1]), num(r[2]), num(r[3]), num(r[4]), end] for r in t["rows"]])
    j = read_json(SRC / "x_insights_data.json")
    jend = j["computedAt"][:10]
    rows = [[f["dimension"], f["bucket"], f["label"], f["effectPct"], f["effectLoPct"], f["effectHiPct"],
             str(f["significant"]).lower(), f["accounts"], f["accountsAgreeing"], f["n"],
             f["medianMultiple"], f["p90Multiple"], jend] for f in j["findings"]]
    out["posting_pattern_effects.csv"] = write_csv(
        d / "posting_pattern_effects.csv",
        ["dimension", "bucket", "label", "effect_pct", "effect_lo_pct", "effect_hi_pct", "significant",
         "accounts", "accounts_agreeing", "posts", "median_multiple", "p90_multiple", "window_end"], rows)
    return out


BUILDERS = {
    "social-follower-percentiles-2026-10": build_follower_percentiles,
    "kick-twitch-category-viewing-2026-09-26": build_kick_twitch_viewing,
    "kick-twitch-simulcasting-2026-09-28": build_simulcast,
    "telegram-subscriber-change-2026-08-to-10": build_telegram_change,
    "telegram-reach-benchmarks-2026-10": build_telegram_reach,
    "x-reach-per-follower-premium-2026": build_x_premium,
    "x-engagement-benchmarks-2026-10": build_x_engagement,
}


# --------------------------------------------------------------------------
# checks against published numbers
# --------------------------------------------------------------------------

def rows_of(path: Path) -> list[dict]:
    return list(csv.DictReader(path.open(encoding="utf-8")))


def checks() -> list[str]:
    bad = []

    def expect(name, got, want, tol=0.0):
        ok = abs(float(got) - float(want)) <= tol if isinstance(want, (int, float)) else got == want
        if not ok:
            bad.append(f"{name}: got {got}, published {want}")

    fp = {(r["platform"], r["percentile"]): int(r["value"])
          for r in rows_of(OUT / "social-follower-percentiles-2026-10" / "follower_percentiles.csv")}
    expect("X median followers", fp[("x", "50")], 490)
    expect("X top 5% starts", fp[("x", "95")], 14177)
    expect("X top 1% starts", fp[("x", "99")], 76100)
    expect("Bluesky median", fp[("bluesky", "50")], 133)
    expect("Bluesky p99", fp[("bluesky", "99")], 9405)
    expect("Telegram median", fp[("telegram", "50")], 51)
    expect("TikTok median", fp[("tiktok", "50")], 5738)
    expect("YouTube median", fp[("youtube", "50")], 63500)
    expect("Kick median", fp[("kick", "50")], 8)

    cv = rows_of(OUT / "kick-twitch-category-viewing-2026-09-26" / "category_viewing_share.csv")
    def gsum(platform, period):
        return round(sum(float(r["share_of_viewing_pct"]) for r in cv
                         if r["platform"] == platform and r["period"] == period and r["is_gambling"] == "true"), 2)
    expect("Kick gambling share, week", gsum("kick", "week"), 7.20, 0.01)
    expect("Twitch gambling share, week", gsum("twitch", "week"), 1.70, 0.01)
    expect("Kick gambling share, Oct 1", round(gsum("kick", "2026-10-01"), 1), 8.7, 0.01)
    expect("Kick gambling share, Oct 2", round(gsum("kick", "2026-10-02"), 1), 5.9, 0.01)
    jc = next(r for r in cv if r["platform"] == "kick" and r["period"] == "week" and r["category"] == "just-chatting")
    expect("Kick Just Chatting channels", int(jc["channels"]), 64561)
    for platform in ("kick", "twitch"):
        tot = sum(float(r["share_of_viewing_pct"]) for r in cv if r["platform"] == platform and r["period"] == "week")
        expect(f"{platform} week shares add up", round(tot, 0), 100, 1)

    sm = {r["measure"]: r["value"] for r in rows_of(OUT / "kick-twitch-simulcasting-2026-09-28" / "summary.csv")}
    expect("simulcasters", int(sm["simulcasters"]), 5063)
    expect("Kick share of combined viewers", round(float(sm["kick_share_of_combined_viewers"]), 1), 16.7, 0.01)
    expect("median Kick share", float(sm["median_streamer_kick_share"]), 21.7, 0.01)

    tc = {r["category"]: r for r in rows_of(OUT / "telegram-subscriber-change-2026-08-to-10" / "subscriber_change_by_category.csv")}
    expect("crypto channels", int(tc["Crypto"]["channels"]), 814)
    expect("crypto lost share", float(tc["Crypto"]["lost_subscribers_pct"]), 85.6, 0.01)
    expect("all channels", int(tc["All channels"]["channels"]), 14874)

    # The crypto article quotes the Telegram benchmark; both must agree.
    tr = {r["band"]: r for r in rows_of(OUT / "telegram-reach-benchmarks-2026-10" / "reach_by_size.csv")}
    expect("Telegram 1k-5k median reach", round(float(tr["1k-5k"]["median_reach_pct"]), 1), 27.5, 0.01)
    expect("Telegram 500k+ median reach", round(float(tr["500k+"]["median_reach_pct"]), 1), 3.1, 0.01)
    expect("Telegram channels measured", int(tr["all"]["channels"]), 139115)
    art = table("crypto-telegram", "Subscribers")
    band_by_label = {"1,000 to 5,000": "1k-5k", "5,000 to 20,000": "5k-20k", "20,000 to 100,000": "20k-100k",
                     "100,000 to 500,000": "100k-500k", "500,000 and up": "500k+"}
    for r in art["rows"]:
        if r[0] in band_by_label:
            k = band_by_label[r[0]]
            expect(f"article vs benchmark channels {k}", int(tr[k]["channels"]), num(r[1]))
            expect(f"article vs benchmark median {k}", round(float(tr[k]["median_reach_pct"]), 1), num(r[2]), 0.01)
    niche = {r["niche"]: r for r in rows_of(OUT / "telegram-reach-benchmarks-2026-10" / "reach_by_niche.csv")}
    for r in table("crypto-telegram", "Category (5k to 100k subscribers)")["rows"]:
        k = r[0].lower()
        expect(f"article vs benchmark niche {k}", round(float(niche[k]["median_reach_pct"]), 1), num(r[2]), 0.01)

    xb = {r["follower_band"]: r for r in rows_of(OUT / "x-reach-per-follower-premium-2026" / "reach_by_follower_band.csv")}
    expect("X 1M+ views per follower", float(xb["Over 1 million"]["views_per_follower_pct"]), 1.20, 0.001)
    expect("X sample", sum(int(r["accounts"]) for r in xb.values()), 60892)

    xp = rows_of(OUT / "x-engagement-benchmarks-2026-10" / "engagement_rate_percentiles.csv")
    if int(xp[0]["accounts"]) != 152187:
        log(f"  note: the X benchmark page now measures {xp[0]['accounts']} accounts; "
            "update the X engagement summary in spec.py")
    return bad


# --------------------------------------------------------------------------
# documents
# --------------------------------------------------------------------------

def size_category(n: int) -> str:
    return "n<1K" if n < 1000 else "1K<n<10K" if n < 10_000 else "10K<n<100K"


def readme_body(ds: dict, counts: dict) -> str:
    L = [f"# {ds['title']}", "", ds["summary"], "",
         f"**Measured:** {ds['measured']}  ",
         f"**Publisher:** PlayerSells ({SITE})  ",
         f"**License:** [{spec.LICENSE_NAME}]({spec.LICENSE_URL})  ",
         f"**Attribution:** {spec.ATTRIBUTION}", "",
         "## Where the numbers are published", ""]
    L += [f"- [{name}]({url})" for name, url in ds["method_urls"]]
    L += ["", "## Files", ""]
    for f in ds["files"]:
        L += [f"### `{f['name']}` ({counts[f['name']]:,} rows)", "", f["description"], "",
              "| Column | Type | Description |", "|---|---|---|"]
        L += [f"| `{c}` | {t} | {desc} |" for c, t, desc in f["columns"]]
        L.append("")
    L += ["## How it was measured", ""] + [f"{p}\n" for p in ds["method"]]
    L += ["## Limitations", ""] + [f"- {x}" for x in ds["limits"] + spec.COMMON_LIMITS]
    L += ["", "## How to cite", "",
          f"PlayerSells (2026). *{ds['title']}*. {ds['method_urls'][0][1]}. Licensed under {spec.LICENSE_NAME}.", "",
          f"When you reuse these numbers, credit \"{spec.ATTRIBUTION}\" with a link.", "",
          "Rebuild from source: `python build.py --refresh` in the repository root.", ""]
    return "\n".join(L)


def hf_card(ds: dict, counts: dict) -> str:
    total = sum(counts.values())
    y = ["---", "license: cc-by-4.0", f"pretty_name: \"{ds['title']}\"", "language:", "- en", "tags:"]
    y += [f"- {k.replace(' ', '-')}" for k in ds["keywords"]]
    y += ["size_categories:", f"- {size_category(total)}", "configs:"]
    for i, f in enumerate(ds["files"]):
        y += [f"- config_name: {f['name'][:-4]}", f"  data_files: \"{f['name']}\""]
        if i == 0:
            y.append("  default: true")
    y += ["---", ""]
    return "\n".join(y) + readme_body(ds, counts)


def kaggle_meta(ds: dict) -> dict:
    type_map = {"string": "string", "integer": "integer", "number": "number", "boolean": "boolean", "date": "datetime"}
    desc = (ds["summary"] + "\n\n" + "\n\n".join(ds["method"]) + "\n\nLimitations:\n"
            + "\n".join(f"- {x}" for x in ds["limits"] + spec.COMMON_LIMITS)
            + "\n\nPublished at " + ", ".join(u for _, u in ds["method_urls"])
            + f"\n\n{spec.ATTRIBUTION}. License {spec.LICENSE_NAME}.")
    return {
        "title": ds["kaggle_title"],
        "subtitle": ds["subtitle"],
        "id": f"{KAGGLE_OWNER}/{ds['slug']}",
        "licenses": [{"name": "CC-BY-4.0"}],
        "keywords": ds["keywords"],
        "description": desc,
        "resources": [
            {"path": f["name"], "description": f["description"],
             "schema": {"fields": [{"name": c, "type": type_map[t], "description": dsc}
                                   for c, t, dsc in f["columns"]]}}
            for f in ds["files"]
        ],
    }


def check_text(ds: dict) -> list[str]:
    blob = json.dumps(ds, ensure_ascii=False)
    return [f"{ds['slug']}: contains a dash character {ch!r}" for ch in ("\u2014", "\u2013") if ch in blob]


def stage(slug: str, ds: dict) -> None:
    for target in ("hf", "kaggle"):
        dst = DIST / target / slug
        if dst.exists():
            shutil.rmtree(dst)
        dst.mkdir(parents=True)
        for f in ds["files"]:
            shutil.copy2(OUT / slug / f["name"], dst / f["name"])
        if target == "hf":
            shutil.copy2(HF / slug / "README.md", dst / "README.md")
        else:
            shutil.copy2(OUT / slug / "dataset-metadata.json", dst / "dataset-metadata.json")
            shutil.copy2(OUT / slug / "README.md", dst / "README.md")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true", help="re-read the sources before building")
    ap.add_argument("--stage", action="store_true", help="assemble dist/hf and dist/kaggle upload folders")
    args = ap.parse_args()

    if args.refresh:
        refresh()

    problems = []
    index = []
    for ds in spec.DATASETS:
        slug = ds["slug"]
        d = OUT / slug
        counts = BUILDERS[slug](d)
        names = [f["name"] for f in ds["files"]]
        assert sorted(counts) == sorted(names), (slug, sorted(counts), names)
        (d / "README.md").write_text(readme_body(ds, counts), encoding="utf-8")
        (HF / slug).mkdir(parents=True, exist_ok=True)
        (HF / slug / "README.md").write_text(hf_card(ds, counts), encoding="utf-8")
        write_json(d / "dataset-metadata.json", kaggle_meta(ds))
        problems += check_text(ds)
        index.append((ds, counts))
        log(f"built {slug}: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
        if args.stage:
            stage(slug, ds)

    write_json(ROOT / "datasets.json", [
        {"slug": ds["slug"], "title": ds["title"], "summary": ds["summary"], "measured": ds["measured"],
         "files": {k: v for k, v in c.items()}, "published_at": [u for _, u in ds["method_urls"]]}
        for ds, c in index])

    problems += checks()
    if problems:
        log("\nCHECKS FAILED:")
        for p in problems:
            log("  - " + p)
        return 1
    log("\nall checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
