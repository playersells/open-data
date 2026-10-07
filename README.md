# PlayerSells Open Data

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23201221.svg)](https://doi.org/10.5281/zenodo.23201221)

Aggregate measurements of social and streaming platforms, collected by [PlayerSells](https://playersells.com) with its own crawlers and published here under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Every number in this repository is also published on playersells.com, on the page linked from each dataset. The files hold totals, shares and percentiles only: no account lists, no channel names, no personal data.

| Dataset | What it measures | Measured |
|---|---|---|
| [social-follower-percentiles-2026-10](datasets/social-follower-percentiles-2026-10) | Followers or subscribers at every percentile on X, Bluesky, Telegram, TikTok, YouTube, Kick and Twitch | 5 Oct 2026 |
| [kick-twitch-category-viewing-2026-09-26](datasets/kick-twitch-category-viewing-2026-09-26) | Share of concurrent viewing by category on Kick and Twitch, gambling included | 26 Sep to 2 Oct 2026 |
| [kick-twitch-simulcasting-2026-09-28](datasets/kick-twitch-simulcasting-2026-09-28) | Streamers live on Kick and Twitch at once, and where their viewers watched | 28 Sep to 4 Oct 2026 |
| [telegram-subscriber-change-2026-08-to-10](datasets/telegram-subscriber-change-2026-08-to-10) | Share of Telegram channels that lost subscribers, by topic and size | Aug to Oct 2026 |
| [telegram-reach-benchmarks-2026-10](datasets/telegram-reach-benchmarks-2026-10) | Views per subscriber for 139,115 Telegram channels, by size band and niche | 3 Oct 2026 |
| [x-reach-per-follower-premium-2026](datasets/x-reach-per-follower-premium-2026) | X post views per follower by account size, Premium against no badge | Aug to Oct 2026 |
| [x-engagement-benchmarks-2026-10](datasets/x-engagement-benchmarks-2026-10) | X engagement rate percentiles by follower band, plus posting pattern effects | 30 days to 7 Oct 2026 |

Each dataset folder has the CSV files, a README with every column, the method and the limitations, and a `dataset-metadata.json` for Kaggle. Hugging Face dataset cards are in [`hf/`](hf).

## License and attribution

[CC BY 4.0](LICENSE). You may copy, adapt and redistribute the data, commercially or not, including in research, journalism and AI-generated answers, as long as you credit:

> Source: PlayerSells (https://playersells.com)

with a link, and say if you changed the numbers. To cite a specific dataset, use the line under "How to cite" in its README, or [`CITATION.cff`](CITATION.cff) for the whole collection.

The collection is archived on Zenodo. [10.5281/zenodo.23201221](https://doi.org/10.5281/zenodo.23201221) always resolves to the latest edition; this edition (2026.10) is [10.5281/zenodo.23201222](https://doi.org/10.5281/zenodo.23201222).

## What these numbers are and are not

- They come from PlayerSells' own crawlers, which read public profiles, public channel previews and public live directories. They describe what those crawlers read, not a census of any platform.
- Counts are the ones the platforms display. Bots, embedded players and inflated counts cannot be separated out.
- Every dataset README lists its own sampling limits. Read them before quoting a figure.

## Rebuilding

```
python build.py            # rebuild every CSV and document from sources/
python build.py --refresh  # re-read the published pages and source files first
python build.py --stage    # also prepare dist/hf/<slug> and dist/kaggle/<slug> for upload
```

`build.py` uses only the Python standard library. After building it compares headline figures with the numbers published on playersells.com and fails if any of them moved.

## Contact

Questions, corrections or requests for a cut of the data: info@playersells.com
