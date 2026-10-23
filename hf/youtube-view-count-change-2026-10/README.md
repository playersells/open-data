---
license: cc-by-4.0
pretty_name: "YouTube public view gains before and after first-frame view counting, 2026"
language:
- en
tags:
- youtube
- view-count
- engaged-views
- creator-economy
- video
- social-media
- benchmarks
size_categories:
- n<1K
configs:
- config_name: comparisons
  data_files: "comparisons.csv"
  default: true
- config_name: weekly_index
  data_files: "weekly_index.csv"
- config_name: change_by_subscribers
  data_files: "change_by_subscribers.csv"
- config_name: change_by_topic_and_language
  data_files: "change_by_topic_and_language.csv"
---
# YouTube public view gains before and after first-frame view counting, 2026

How fast 3,565 large YouTube channels gained public views in the 28 days after YouTube began counting views from the first frame of playback on 24 August 2026, against the 28 days before. The median channel gained views 12.5% faster, against -3.5% and +2.1% in comparisons made entirely before the change, and total views gained by the same channels fell 8.3%.

**Measured:** Daily public view counters, 6 July to 19 October 2026, read 23 October 2026  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [Did YouTube's New View Count Inflate Views? 3,565 Channels](https://playersells.com/learn/did-youtubes-new-view-count-inflate-views-3565-channels-measured)

## Files

### `comparisons.csv` (7 rows)

Change in views gained per day, same channels, for windows across, before and after 24 August 2026.

| Column | Type | Description |
|---|---|---|
| `comparison` | string | Which pair of windows is compared |
| `windows_2026` | string | The earlier window, against the later window |
| `channels` | integer | Channels in the comparison |
| `median_change_pct` | number | Median across channels of (views gained per day, later window / earlier window - 1), in percent |
| `p25_change_pct` | number | 25th percentile of the same |
| `p75_change_pct` | number | 75th percentile of the same |
| `channels_faster_pct` | number | Share of channels that gained views faster in the later window |
| `total_change_pct` | number | Change in the sum of views gained across all channels |

### `weekly_index.csv` (12 rows)

Each channel's weekly view gain against its own average week from 27 July to 24 August 2026, median across 3,564 channels.

| Column | Type | Description |
|---|---|---|
| `week_start` | date | First day of the 7-day window |
| `median_change_vs_pre_change_week_pct` | number | Median across channels of (weekly gain / average pre-change week - 1), in percent |
| `channels_above_pre_change_pace_pct` | number | Share of channels whose weekly gain was above their pre-change average week |
| `total_views_gained_billion` | number | Sum of public views gained by the channels in the week, billions |

### `change_by_subscribers.csv` (3 rows)

Main comparison (27 July to 24 August against 24 August to 21 September 2026) by subscriber count on 24 August.

| Column | Type | Description |
|---|---|---|
| `subscribers_on_2026_08_24` | string | Subscriber band on 24 August 2026; the smallest channel had 1,440,000 |
| `channels` | integer | Channels in the band |
| `median_change_pct` | number | Median change in views gained per day, in percent |
| `channels_faster_pct` | number | Share of channels that gained views faster |
| `channels_30pct_faster_pct` | number | Share of channels that gained views at least 30% faster |
| `total_change_pct` | number | Change in the sum of views gained |

### `change_by_topic_and_language.csv` (9 rows)

Main comparison by channel topic (PlayerSells directory label, at least 80 channels) and by main language.

| Column | Type | Description |
|---|---|---|
| `group` | string | Topic label, Unlabeled, English, or Other or unknown language |
| `channels` | integer | Channels in the group |
| `median_change_pct` | number | Median change in views gained per day, in percent |
| `channels_faster_pct` | number | Share of channels that gained views faster |
| `total_change_pct` | number | Change in the sum of views gained |

## How it was measured

PlayerSells' YouTube directory reads the public statistics of the channels it tracks through the YouTube Data API and keeps one view counter reading per channel per day. The panel is every channel with at least 20 daily readings before 24 August 2026 (5,981 channels) and a reading on every day from 27 July to 21 September 2026: 3,681 channels, all with at least 1,440,000 subscribers on 24 August (median 3,080,000). Queries ran on 23 October 2026.

For each channel, views gained per day in a window is the counter at the end minus the counter at the start, divided by the number of days. A channel's change is the later window over the earlier one. The tables give the median across channels, the 25th and 75th percentiles, the share of channels that gained faster, and the change in the sum across channels. Channels with no views gained in the earlier window are left out (116 in the main comparison). The trend variant uses the least squares slope of the daily counter in each window.

Comparisons that sit entirely before or entirely after 24 August show how much views drift without a counting change. The weekly table divides each channel's weekly gain by its average week from 27 July to 24 August 2026, for the 3,564 channels also read every day to 19 October.

Instrument check, 23 October 2026: for 25 channels, the public view counts of all their uploads added up to a median 1.0003 times the channel counter, so the channel counter follows the public video counters that viewers see.

Topic labels come from the PlayerSells directory's own classification; 1,601 channels in the panel have none. No channel name, handle or identifier is included. The files hold aggregates only.

## Limitations

- Large channels only: every channel in the panel had at least 1,440,000 subscribers.
- There are no 2025 readings for these channels, so late-summer seasonality cannot be fully separated from the counting change.
- The channel counter mixes long-form videos, Shorts, live streams and podcasts. Shorts views were already counted from the first frame before 24 August 2026.
- Public counters only: no engaged views, watch time or unique viewers.
- Public counters sometimes pause for a day and then catch up, so single weeks are noisy.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *YouTube public view gains before and after first-frame view counting, 2026*. https://playersells.com/learn/did-youtubes-new-view-count-inflate-views-3565-channels-measured. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
