---
license: cc-by-4.0
pretty_name: "Kick and Twitch share of viewing by category, week of 26 September 2026"
language:
- en
tags:
- kick
- twitch
- live-streaming
- gambling
- slots
- viewership
- categories
size_categories:
- 10K<n<100K
configs:
- config_name: category_viewing_share
  data_files: "category_viewing_share.csv"
  default: true
- config_name: gambling_share_week
  data_files: "gambling_share_week.csv"
- config_name: rank_comparison_30d
  data_files: "rank_comparison_30d.csv"
---
# Kick and Twitch share of viewing by category, week of 26 September 2026

Share of concurrent viewing that each streaming category took on Kick and on Twitch from 26 September to 2 October 2026, daily and for the whole week, measured with one method on both platforms. Gambling took 7.2% of Kick viewing and 1.7% of Twitch viewing on these readings.

**Measured:** 26 September 2026 00:00 UTC to 3 October 2026 00:00 UTC  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [How Much of Kick Is Gambling? One Week vs Twitch](https://playersells.com/learn/how-much-of-kick-is-gambling-one-week-measured-against-twitch)

## Files

### `category_viewing_share.csv` (18,181 rows)

Share of concurrent viewing per category, per platform, per day and for the whole week.

| Column | Type | Description |
|---|---|---|
| `platform` | string | kick or twitch |
| `period` | string | A UTC date (YYYY-MM-DD) or week for the whole seven days |
| `category` | string | Kick category slug or Twitch category name, as the platforms publish them. One row per period groups every category with fewer than 5 channels |
| `share_of_viewing_pct` | number | Viewers in the category as a percentage of all viewers on the platform in that period |
| `channels` | integer | Distinct channels seen live in the category during the period. On Twitch this counts only streams that reached the top 30 of their category |
| `is_gambling` | boolean | true for the categories counted as gambling: Kick slots, poker and sports-betting; Twitch Slots, Poker and Virtual Casino |

### `gambling_share_week.csv` (5 rows)

The gambling comparison table as published, for the whole week.

| Column | Type | Description |
|---|---|---|
| `category` | string | Gambling category or the total |
| `kick_share_of_viewing_pct` | number | Share of Kick viewing; empty where Kick has no such category |
| `twitch_share_of_viewing_pct` | number | Share of Twitch viewing; empty where Twitch has no such category |

### `rank_comparison_30d.csv` (6 rows)

Channels by average concurrent viewers while live, Twitch against Kick, 30 days to 3 October 2026.

| Column | Type | Description |
|---|---|---|
| `measure` | string | What is counted |
| `twitch` | integer | Value on Twitch |
| `kick` | integer | Value on Kick |

## How it was measured

Kick: a sampler walks Kick's whole public live directory page by page and records every live channel's viewer count and category. Over the week it recorded 201,070 channels.

Twitch: Twitch's public interface does not let a crawler page through the full live list, so the sampler reads every category every 15 minutes and records up to 30 streams per category, the most watched first. Over the week it recorded 385,643 channels.

Share of viewing: one reading per channel per 15-minute block (the average if there were several), viewers summed by category and divided by the platform total for the period. This is the share of concurrent viewers, not of hours watched.

A spot check on 3 October 2026 found the Twitch sampler holding about 62% of the viewers Twitch's own counters showed in Slots, Virtual Casino and Poker, against about 70% in other large categories. Adjusted for that, Twitch's gambling share is about 1.9%. The Kick sampler held about 95% to 97% of Kick's own counters.

The rank comparison counts channels live at least once in the 10 days to 3 October 2026, ranked by average concurrent viewers while live over the 30 days to that date.

## Limitations

- One week. Gambling viewing moves with events and individual streamers.
- Category labels are the streamers' own. A slots stream filed under Just Chatting counts as Just Chatting.
- The Twitch sampler sees only the top 30 streams of each category at a time, so Twitch channel counts are floors and Twitch shares in very large categories miss the long tail.
- No absolute viewer or hours-watched totals are published, because the samplers measure shares more reliably than totals.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Kick and Twitch share of viewing by category, week of 26 September 2026*. https://playersells.com/learn/how-much-of-kick-is-gambling-one-week-measured-against-twitch. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
