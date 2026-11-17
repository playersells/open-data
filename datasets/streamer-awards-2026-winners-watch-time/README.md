# Streamer Awards 2026 winners against Kick and Twitch watch time and follower growth

For the 28 categories of the 2026 Streamer Awards that put single streamers against each other (110 nominees), the Kick and Twitch watch time of every nominee while fan voting was open (16 to 31 October 2026), the rank of each category's winner, and how often the top-ranked nominee won under five ranking measures. The most-watched nominee won 6 of 28 categories, against 6.3 expected from a random draw; ranking by followers or average viewers picked 11. Also: median Twitch follower growth of award winners and other nominees in the four days before and after the ceremony of 12 November 2026.

**Measured:** Kick and Twitch live samples every 15 minutes, 1 September to 16 November 2026 (UTC), read 17 November 2026  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [Streamer Awards 2026: Most-Watched Nominee Won 6 of 28](https://playersells.com/learn/did-the-most-watched-nominee-win-streamer-awards-2026-measured)

## Files

### `category_results.csv` (28 rows)

One row per category: the winner's rank by Kick and Twitch hours watched during the vote, and the hours of the winner and of the most-watched nominee. Streamer names are not included.

| Column | Type | Description |
|---|---|---|
| `category` | string | Award category |
| `nominees` | integer | Nominees in the category |
| `winner_rank_by_hours_watched` | integer | Winner's rank by hours watched, 1 = most watched (competition ranking) |
| `winner_hours_watched` | integer | Winner's hours watched on Twitch and verified Kick channels, 16 to 31 October 2026 |
| `most_watched_nominee_hours_watched` | integer | Hours watched of the category's most-watched nominee, same window |
| `most_watched_nominee_won` | string | yes if the most-watched nominee won the category |

### `ranking_measures.csv` (5 rows)

How often the top-ranked and the lowest-ranked nominee won, by ranking measure, and the winners' average percentile (50 = what a random draw gives).

| Column | Type | Description |
|---|---|---|
| `ranking_measure` | string | Measure used to rank the nominees of each category |
| `categories_won_by_top_ranked` | integer | Categories won by the nominee ranked first on the measure |
| `categories` | integer | Categories |
| `categories_won_by_lowest_ranked` | integer | Categories won by a nominee strictly last on the measure |
| `winner_average_percentile` | number | Average percentile of the winner within its category (ties count half) |

### `follower_growth.csv` (2 rows)

Median Twitch follower growth over three four-day stretches around the ceremony (12 November 2026), award winners against nominees who won nothing.

| Column | Type | Description |
|---|---|---|
| `group` | string | Won an award (any award at the 2026 show) or nominated and won nothing |
| `twitch_channels` | integer | Twitch channels with a follower count on 4, 8, 12 and 16 November 2026 |
| `median_growth_nov_4_to_8_pct` | number | Median follower growth, 4 to 8 November, percent |
| `median_growth_nov_8_to_12_pct` | number | Median follower growth, 8 to 12 November, percent |
| `median_growth_nov_12_to_16_pct` | number | Median follower growth, 12 to 16 November, percent |
| `channels_faster_after_ceremony` | integer | Channels that grew faster from 12 to 16 November than from 8 to 12 November |

## How it was measured

Winners and nominees: the Wikipedia page of the 2026 Streamer Awards (read 17 November 2026). Kept: the 28 categories in which each nominee is a single streamer and more than one was nominated.

Channels: each nominee matched to a Twitch channel by login or display name (100 nominees, 3 through a close variant) and to a Kick channel only on an exact name match with a verified channel (17); 8 nominees had neither.

Watch time: the PlayerSells samplers read Kick's whole live directory and the 30 most-watched live streams of every Twitch category every 15 minutes; hours watched = viewers at each reading x 0.25 hours, summed over 16 to 31 October 2026 (UTC), the fan voting window.

Chance: if each nominee in a category were equally likely to win, the top-ranked nominee would win 6.3 of 28 categories on average (exact Poisson binomial).

Followers: daily Twitch follower counts recorded by the PlayerSells directory; a missing day takes the previous day's count. Aggregates only; no streamer is named in the files.

## Limitations

- YouTube and TikTok are not measured: winners who stream mainly there look smaller than they are.
- On Twitch a stream is counted only while it is among the 30 most-watched of its category; small channels are a lower bound.
- Votes are not public, and fans voted with a 30% panel weight: the data shows how far apart votes and watch time are, not whether the vote was fair.
- The follower comparison covers four days and Twitch only and cannot separate the award from the attention of the broadcast.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Streamer Awards 2026 winners against Kick and Twitch watch time and follower growth*. https://playersells.com/learn/did-the-most-watched-nominee-win-streamer-awards-2026-measured. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
