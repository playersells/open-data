---
license: cc-by-4.0
pretty_name: "Kick and Twitch simulcasting, week of 28 September 2026"
language:
- en
tags:
- kick
- twitch
- simulcasting
- multistreaming
- live-streaming
- viewership
size_categories:
- n<1K
configs:
- config_name: summary
  data_files: "summary.csv"
  default: true
- config_name: kick_share_distribution
  data_files: "kick_share_distribution.csv"
- config_name: split_by_audience_size
  data_files: "split_by_audience_size.csv"
- config_name: top_channels_simulcasting
  data_files: "top_channels_simulcasting.csv"
- config_name: twitch_category_split
  data_files: "twitch_category_split.csv"
- config_name: kick_category_simulcast_share
  data_files: "kick_category_simulcast_share.csv"
---
# Kick and Twitch simulcasting, week of 28 September 2026

Streamers who broadcast on Kick and Twitch at the same time from 28 September to 4 October 2026, and how their concurrent viewers split between the two platforms. Twitch drew 83.3% of the combined viewers and Kick 16.7%.

**Measured:** 28 September 2026 00:00 UTC to 5 October 2026 00:00 UTC  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [Kick and Twitch Simulcasts: 83% of Viewers Watch on Twitch](https://playersells.com/learn/kick-and-twitch-simulcasting-measured-where-viewers-watch)

## Files

### `summary.csv` (24 rows)

Headline measures of the week, including the sensitivity checks.

| Column | Type | Description |
|---|---|---|
| `measure` | string | What is measured |
| `value` | number | The value |
| `unit` | string | count, hours or percent |
| `note` | string | How to read it |

### `kick_share_distribution.csv` (4 rows)

Simulcasters grouped by the share of their combined viewers that watched on Kick.

| Column | Type | Description |
|---|---|---|
| `kick_share_band` | string | Share of the streamer's combined viewers on Kick |
| `simulcasters` | integer | Streamers in the band |

### `split_by_audience_size.csv` (4 rows)

Kick's share of combined viewers by the simulcaster's average combined audience.

| Column | Type | Description |
|---|---|---|
| `avg_combined_viewers_band` | string | Average combined viewers while simulcasting |
| `simulcasters` | integer | Streamers in the band |
| `kick_share_of_combined_viewers_pct` | number | Kick's share of the band's combined viewers |

### `top_channels_simulcasting.csv` (5 rows)

How many of each platform's most watched channels of the week simulcast on the other.

| Column | Type | Description |
|---|---|---|
| `top_n` | integer | The N most watched channels on the platform in the week |
| `twitch_channels_simulcasting_on_kick` | integer | Of Twitch's top N |
| `kick_channels_simulcasting_on_twitch_min` | integer | Of Kick's top N, a minimum (see limits) |

### `twitch_category_split.csv` (190 rows)

Every Twitch category with 10 or more simulcasters, ranked by combined viewing during simulcasts.

| Column | Type | Description |
|---|---|---|
| `rank_by_simulcast_viewing` | integer | 1 = the category with the most combined viewing during simulcasts |
| `twitch_category` | string | The simulcaster's main Twitch category |
| `simulcasters` | integer | Streamers whose main Twitch category this was |
| `kick_share_of_combined_viewers_pct` | number | Kick's share of those streamers' combined viewers |

### `kick_category_simulcast_share.csv` (12 rows)

For Kick's largest categories, the share of Kick viewing that came from simulcasts.

| Column | Type | Description |
|---|---|---|
| `rank_by_kick_viewing` | integer | 1 = the most watched Kick category of the week |
| `kick_category` | string | Kick category slug |
| `simulcast_share_of_category_viewing_min_pct` | number | Minimum share of the category's Kick viewing that came from simulcasting channels |

## How it was measured

Both samplers read every 15 minutes: the Kick sampler walks Kick's whole public live directory (201,145 channels in the week), the Twitch sampler reads every category and records up to 30 streams per category, the most watched first (388,927 channels in the week).

A simulcaster is a Kick channel and a Twitch channel with the same name (compared in lower case with hyphens and underscores removed) that were both live in the same 15-minute block for at least four blocks (one hour) in the week, in matching categories in at least half of those blocks. 11,782 names were live on both platforms at some point; 6,736 overlapped for an hour or more; 5,063 of those also matched on category.

Audience split: for each simulcaster, viewer counts on each platform summed over the blocks in which both streams were read, and Kick's sum divided by the total. Platform totals are sums over all simulcasters; the median is taken per streamer.

Robustness: repeating the split only in blocks where the Twitch category had fewer than 30 live streams (so every stream in it was read) gives Kick 16.6% of combined viewers against 16.7% overall.

## Limitations

- One week. Simulcasting follows events, contracts and individual streamers.
- Matching is by name, time and category. A streamer who uses different names on the two platforms is missed; a third party rebroadcasting under the same name would be counted.
- A Twitch stream is visible only while it is in the top 30 of its category, so every Kick-side figure is a minimum and Twitch figures describe streams that reached that level.
- Channel names are not published here; the files hold totals only.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Kick and Twitch simulcasting, week of 28 September 2026*. https://playersells.com/learn/kick-and-twitch-simulcasting-measured-where-viewers-watch. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
