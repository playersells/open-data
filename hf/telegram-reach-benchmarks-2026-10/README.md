---
license: cc-by-4.0
pretty_name: "Telegram channel reach per post by size and niche, October 2026 edition"
language:
- en
tags:
- telegram
- engagement-rate
- reach
- benchmarks
- views-per-subscriber
size_categories:
- n<1K
configs:
- config_name: reach_by_size
  data_files: "reach_by_size.csv"
  default: true
- config_name: reach_by_niche
  data_files: "reach_by_niche.csv"
---
# Telegram channel reach per post by size and niche, October 2026 edition

How many views a Telegram channel's average post gets per subscriber, for every public broadcast channel with at least 1,000 subscribers whose page PlayerSells read in the 60 days to 3 October 2026. The typical channel with 1,000 to 5,000 subscribers reaches 27.5% of its subscribers per post; above 500,000 it is 3.1%.

**Measured:** 3 October 2026 (pages read 4 August to 3 October 2026)  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [What is a good Telegram engagement rate?](https://playersells.com/telegram-engagement-rate)

## Files

### `reach_by_size.csv` (6 rows)

Distribution of views per subscriber in each subscriber band, plus an all-channels row.

| Column | Type | Description |
|---|---|---|
| `band` | string | Subscriber band, or all |
| `min_subscribers` | integer | Lower bound of the band (inclusive) |
| `max_subscribers` | integer | Upper bound of the band (exclusive); empty for the top band |
| `channels` | integer | Channels measured in the band |
| `p10_reach_pct` | number | 10th percentile of average views per post divided by subscribers, in percent |
| `p25_reach_pct` | number | 25th percentile |
| `median_reach_pct` | number | Median |
| `p75_reach_pct` | number | 75th percentile |
| `p90_reach_pct` | number | 90th percentile |
| `median_views_per_post` | integer | Median average views per post |

### `reach_by_niche.csv` (18 rows)

Median views per subscriber by niche, channels with 5,000 to 100,000 subscribers.

| Column | Type | Description |
|---|---|---|
| `niche` | string | Topic label from a keyword classifier |
| `channels` | integer | Channels measured |
| `median_reach_pct` | number | Median average views per post divided by subscribers, in percent |

## How it was measured

For every public channel it tracks, PlayerSells reads the subscriber count and the view counts of the most recent posts from the channel's public t.me preview. Reach per post is the average view count divided by the subscriber count.

The table counts every qualifying channel with no sampling: broadcast channels with at least 1,000 subscribers, a view count above zero and a public page read between 4 August and 3 October 2026. 139,115 channels, measured on 3 October 2026 at 14:29 UTC.

Across all of them the median is 14.5%, and 10.1% of channels average more views per post than they have subscribers.

The niche table holds channels with 5,000 to 100,000 subscribers that the classifier assigned a niche, in niches with at least 200 such channels.

## Limitations

- Private and invite-only channels, and groups, cannot be measured this way.
- Average views include posts that are still collecting views, so channels that post many times a day can read lower than their settled reach.
- Views per subscriber above 100% come from forwards, cross-posts or paid promotion.
- This is a dated edition, re-measured once a quarter.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Telegram channel reach per post by size and niche, October 2026 edition*. https://playersells.com/telegram-engagement-rate. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
