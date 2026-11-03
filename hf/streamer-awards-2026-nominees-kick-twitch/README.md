---
license: cc-by-4.0
pretty_name: "Where do the 2026 Streamer Awards nominees stream? Kick and Twitch watch time, 2026"
language:
- en
tags:
- kick
- twitch
- streamer-awards
- live-streaming
- creator-economy
- streamers
size_categories:
- n<1K
configs:
- config_name: nominees_by_platform
  data_files: "nominees_by_platform.csv"
  default: true
- config_name: kick_share_benchmark
  data_files: "kick_share_benchmark.csv"
- config_name: categories
  data_files: "categories.csv"
- config_name: weekly
  data_files: "weekly.csv"
---
# Where do the 2026 Streamer Awards nominees stream? Kick and Twitch watch time, 2026

The 110 nominees of the 28 single-streamer categories of the 2026 Streamer Awards, the first edition open to Kick streamers, measured on Kick and Twitch from 28 September to 2 November 2026. 12 were live on Kick for at least an hour and 5 drew more viewing on Kick than on Twitch. Kick carried 4.5% of the nominees' combined Kick and Twitch watch time, against 21.9% for the 1,000 most-watched English-language channels on the two platforms.

**Measured:** 15-minute live samples, 28 September to 2 November 2026 (UTC), read 3 November 2026  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [Streamer Awards 2026 Nominees: 4.5% of Watch Time on Kick](https://playersells.com/learn/where-do-streamer-awards-2026-nominees-stream-kick-and-twitch-measured)

## Files

### `nominees_by_platform.csv` (4 rows)

Nominees by the platforms they were live on for at least an hour in the five weeks.

| Column | Type | Description |
|---|---|---|
| `where_streamed` | string | Twitch only, both, Kick only, or neither |
| `nominees` | integer | Nominees |
| `share_pct` | number | Share of the 110 nominees |

### `kick_share_benchmark.csv` (4 rows)

Kick's share of watch time among the most-watched Kick and Twitch channels (English-language and all languages) and among the nominees.

| Column | Type | Description |
|---|---|---|
| `group` | string | Channel group |
| `kick_channels` | string | Kick channels in the English-language group (for the nominees: nominees active on Kick) |
| `kick_share_of_watch_time_english_pct` | number | Kick hours watched as a share of Kick plus Twitch hours watched, English-language channels |
| `kick_share_of_watch_time_all_languages_pct` | number | The same without the language filter |

### `categories.csv` (11 rows)

Award categories with any Kick viewing (categories at 0.0% omitted).

| Column | Type | Description |
|---|---|---|
| `category` | string | Award category |
| `nominees` | integer | Nominees in the category |
| `active_on_kick` | integer | Nominees live on Kick for at least an hour |
| `mainly_on_kick` | integer | Nominees with more Kick than Twitch watch time |
| `kick_share_of_watch_time_pct` | number | Kick share of the category nominees' combined watch time |

### `weekly.csv` (5 rows)

The nominee group week by week.

| Column | Type | Description |
|---|---|---|
| `week_2026` | string | The 7-day week, UTC |
| `nominees_live_on_kick_1h_plus` | integer | Nominees live on Kick for at least an hour that week |
| `kick_share_of_watch_time_pct` | number | Kick share of the group's Kick plus Twitch watch time |

## How it was measured

Panel: every unique nominee of the 28 categories of the 2026 Streamer Awards that name one streamer per nominee (nominee list on Wikipedia, 3 November 2026). Brand, game, group, duo, collab, marathon, event and series categories are left out.

Each name was matched to a Twitch channel whose login or display name equals it and to a Kick channel whose name equals it and that carries Kick's verified badge; three Twitch matches use a handle variant.

Two PlayerSells samplers run every 15 minutes: Kick's whole live directory, and the top 30 live streams of every Twitch category. Hours watched = viewer count at each reading times a quarter hour. Weeks 28 Sep to 4 Oct, 6 to 12 Oct, 13 to 19 Oct, 20 to 26 Oct and 27 Oct to 2 Nov 2026 (UTC).

Benchmark: every Kick and Twitch channel ranked by five-week watch time; language is the channel's language setting in each platform's directory. No channel name, handle or identifier is included. Aggregates only.

## Limitations

- Kick and Twitch only: YouTube and other platforms are not measured.
- Twitch is read only for the top 30 streams of each category, so Twitch hours of small nominees are a lower bound.
- Nominees using a different name on a platform are missed; unverified Kick channels are not used.
- Five weeks only; 5 October 2026 is not covered. Displayed viewer counts are the platforms' own.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Where do the 2026 Streamer Awards nominees stream? Kick and Twitch watch time, 2026*. https://playersells.com/learn/where-do-streamer-awards-2026-nominees-stream-kick-and-twitch-measured. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
