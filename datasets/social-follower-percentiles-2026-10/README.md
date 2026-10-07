# Follower count percentiles on seven social platforms (October 2026)

How many followers or subscribers an account needs to reach each percentile on X (Twitter), Bluesky, Telegram, TikTok, YouTube, Kick and Twitch, measured on 5 October 2026 over the accounts in the PlayerSells index.

**Measured:** 5 October 2026  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [X (Twitter) follower rank](https://playersells.com/tools/twitter-follower-rank)
- [Bluesky follower rank](https://playersells.com/tools/bluesky-follower-rank)
- [Telegram channel rank](https://playersells.com/tools/telegram-channel-rank)
- [TikTok follower rank](https://playersells.com/tools/tiktok-follower-rank)
- [YouTube subscriber rank](https://playersells.com/tools/youtube-subscriber-rank)
- [Kick follower rank](https://playersells.com/tools/kick-follower-rank)
- [Twitch follower rank](https://playersells.com/tools/twitch-follower-rank)

## Files

### `follower_percentiles.csv` (731 rows)

One row per platform and percentile: the follower or subscriber count at that percentile.

| Column | Type | Description |
|---|---|---|
| `platform` | string | x, bluesky, telegram, tiktok, youtube, kick or twitch |
| `percentile` | number | 0 to 99 in steps of 1, then the extra top-1% breakpoints (99.5, 99.8, 99.9, 99.95, 99.99) where the sample is large enough |
| `value` | integer | Followers (subscribers on Telegram and YouTube) at that percentile |
| `metric` | string | followers or subscribers |
| `measured_on` | date | Date the percentile ladder was measured |

### `platforms.csv` (7 rows)

One row per platform: what was measured, how many accounts, and how far the numbers generalise.

| Column | Type | Description |
|---|---|---|
| `platform` | string | Platform key used in follower_percentiles.csv |
| `label` | string | Platform name |
| `unit` | string | What one row of the index is (account, channel, creator) |
| `metric` | string | followers or subscribers |
| `framing` | string | population: the index has a long tail of small accounts; tracked: the catalog covers a selected part of the platform and percentiles describe that part only |
| `sample_size` | integer | Accounts the percentiles were computed over |
| `indexed_total` | integer | Accounts in the PlayerSells index for that platform when measured |
| `measured_on` | date | Date the percentiles were measured |
| `coverage_note` | string | What the sample does and does not represent |
| `method_url` | string | Page on playersells.com that publishes and explains these numbers |

## How it was measured

For each platform PlayerSells computes a 101-point ladder of the follower or subscriber count (percentile_disc at every whole percentile) over the accounts in its index. On X, Bluesky and Telegram the ladder is computed over a sample of the index (459,415 of 22,837,969 X accounts, 970,889 of 4,173,274 Bluesky accounts, 1,020,191 of 3,384,503 Telegram channels). TikTok, YouTube and Twitch are measured whole. On Kick the ladder covers the 328,559 channels whose follower count has been read, out of 458,657 in the catalog, because Kick's live directory does not return follower counts and a separate per-channel pass fills them in.

Inside the top 1% a single step from p99 to p100 spans several orders of magnitude, so extra breakpoints are measured at 99.5, 99.8, 99.9, 99.95 and 99.99 where the sample holds enough accounts above them. TikTok and YouTube stop at 99.9.

p100, the single largest account in each sample, is left out: it is one account, not a distribution, and on a sampled platform it is not even the largest account in the index.

These are the same ladders the rank tools on playersells.com use to place an account.

## Limitations

- Percentiles describe the accounts in the PlayerSells index, which is built by crawling public profiles. Accounts nobody links to, private accounts and deleted accounts are missing.
- TikTok and YouTube are tracked catalogs seeded from larger creators (median 5,738 TikTok followers and 63,500 YouTube subscribers), so a small creator placing low there has learned something about the catalog, not about the platform.
- Kick and Twitch hold channels PlayerSells has recorded going live, not every registered account. Read their percentiles as a place among channels that actually stream.
- The streaming catalogs grow every week, so their ladders date quickly.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Follower count percentiles on seven social platforms (October 2026)*. https://playersells.com/tools/twitter-follower-rank. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
