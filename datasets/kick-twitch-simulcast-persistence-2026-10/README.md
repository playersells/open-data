# Do streamers keep simulcasting? Kick and Twitch simulcasters over four weeks, 2026

The same Kick and Twitch streamers followed for four weeks, 28 September to 26 October 2026. 10,328 streamers were live on both platforms at once, under the same name and in the same category, for at least an hour in at least one week. 49.3% did it in only one week and 15.4% in all four; from one week to the next, 42.3% stopped. The streamers who simulcast every week carried 71.8% of all simulcast viewing.

**Measured:** 15-minute live samples, weeks of 28 September to 26 October 2026 (UTC), read 27 October 2026  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [Do Streamers Keep Simulcasting? 10,328 Tracked for 4 Weeks](https://playersells.com/learn/do-streamers-keep-simulcasting-kick-and-twitch-four-weeks-measured)

## Files

### `weekly_series.csv` (4 rows)

Simulcasters and the audience split in each of the four weeks.

| Column | Type | Description |
|---|---|---|
| `week_2026` | string | The 7-day week, UTC |
| `simulcasters` | integer | Streamers live on Kick and Twitch at once for at least an hour in the week, same name, matching category |
| `kick_share_of_combined_viewers_pct` | number | Kick viewers as a share of Kick plus Twitch viewers, summed over the blocks live on both |
| `median_streamer_kick_share_pct` | number | Median across simulcasters of their own Kick share |
| `hours_live_on_both` | integer | Hours live on both platforms, all simulcasters |
| `kick_channels_live_2h_that_simulcast_pct` | number | Share of Kick channels live 2 hours or more in the week that were simulcasters |

### `week_to_week.csv` (3 rows)

How many of a week's simulcasters simulcast again the following week.

| Column | Type | Description |
|---|---|---|
| `weeks_2026` | string | The first week, then the following week |
| `simulcasters_first_week` | integer | Simulcasters in the first week |
| `simulcast_again_pct` | number | Share who met the same definition in the following week |
| `stopped_pct` | number | Share who did not |
| `new_in_second_week` | integer | Simulcasters of the following week who were not simulcasters in the first |
| `new_share_of_second_week_pct` | number | The same as a share of the following week's simulcasters |
| `first_week_viewing_that_continued_pct` | number | Share of the first week's simulcast viewer hours that belonged to streamers who continued |

### `persistence_by_group.csv` (10 rows)

Share who simulcast again the next week, by hours simulcast, audience size and Kick verified badge in the first week (three steps pooled), with a check in fully read Twitch categories.

| Column | Type | Description |
|---|---|---|
| `group` | string | Group in the first week |
| `simulcaster_weeks` | integer | Weekly simulcasters in the group, three week-to-week steps pooled |
| `simulcast_again_next_week_pct` | number | Share who simulcast again the following week |
| `fully_read_check_streamers` | integer | Oct 13 to 19 simulcasters live on Kick for at least 2 hours the next week in blocks where every Twitch stream of the matching category was read |
| `fully_read_check_seen_simulcasting_pct` | number | Share of those seen live on Twitch for at least an hour of those blocks |

### `persistence_by_kick_share.csv` (4 rows)

Share who simulcast again the next week by the streamer's Kick share of combined viewers, overall and within bands of hours simulcast.

| Column | Type | Description |
|---|---|---|
| `kick_share_of_combined_viewers` | string | The streamer's Kick share in the first week |
| `simulcaster_weeks` | integer | Weekly simulcasters in the band, three steps pooled |
| `simulcast_again_all_pct` | number | Share who simulcast again |
| `simulcast_again_under_2h_pct` | number | The same, streamers who simulcast under 2 hours that week |
| `simulcast_again_2_to_10h_pct` | number | The same, 2 to 10 hours |
| `simulcast_again_10_to_30h_pct` | number | The same, 10 to 30 hours |
| `simulcast_again_30h_plus_pct` | number | The same, 30 hours or more |
| `fully_read_check_seen_simulcasting_pct` | number | Fully read check as in persistence_by_group.csv |

### `weeks_simulcasting.csv` (4 rows)

Streamers who simulcast at least once in the four weeks, by the number of weeks they did.

| Column | Type | Description |
|---|---|---|
| `weeks_simulcasting_of_4` | integer | Weeks in which the streamer met the simulcast definition |
| `streamers` | integer | Streamers |
| `share_of_streamers_pct` | number | Share of the streamers who simulcast at least once |
| `share_of_simulcast_viewing_pct` | number | Share of all Kick plus Twitch viewer hours while live on both, four weeks |
| `median_hours_simulcast_per_week` | number | Median over the streamers' simulcasting weeks |
| `median_kick_share_pct` | number | Median Kick share of combined viewers over the same weeks |

### `after_stopping.csv` (4 rows)

What streamers did in the week after they stopped simulcasting (three steps pooled).

| Column | Type | Description |
|---|---|---|
| `following_week` | string | Status in the following week |
| `times` | integer | Cases |
| `share_pct` | number | Share of cases |
| `share_of_their_earlier_simulcast_viewing_pct` | number | Share of the stopped streamers' simulcast viewer hours in the week before |

### `same_streamer_test.csv` (3 rows)

Same streamer, category and 3-hour window of the day: viewers in simulcast hours against single-platform hours, Oct 13 to 19 and Oct 20 to 26, 2026.

| Column | Type | Description |
|---|---|---|
| `comparison` | string | What is compared |
| `median_change_oct13_19_pct` | number | Median change across channels, Oct 13 to 19 |
| `channels_oct13_19` | integer | Channels in the comparison, Oct 13 to 19 |
| `median_change_oct20_26_pct` | number | Median change across channels, Oct 20 to 26 |
| `channels_oct20_26` | integer | Channels in the comparison, Oct 20 to 26 |

## How it was measured

Two PlayerSells samplers run every 15 minutes. The Kick sampler reads Kick's whole live directory with each channel's viewer count and category. The Twitch sampler reads the top 30 live streams of every Twitch category, because Twitch's public API stops paging there.

A streamer is a simulcaster in a week when the Kick channel name and the Twitch login match after lower-casing and removing '-' and '_', both are live in the same 15-minute block in at least 4 blocks (an hour), and the categories match in at least half of those blocks. A simulcaster 'simulcast again' when the same name met the definition the following week.

Weeks: 28 September to 4 October, 6 to 12 October, 13 to 19 October and 20 to 26 October 2026, UTC. Raw samples are kept for about 8 days, so the first three weeks were rebuilt from the per-channel outputs saved when each week was first measured; the counts match the articles published then.

The fully read check uses only blocks where the same-named Twitch category had fewer than 30 live streams, so a missing Twitch stream is a real absence. No channel name, handle or identifier is included. The files hold aggregates only.

## Limitations

- Twitch is read only for the top 30 streams of each category, so some streamers counted as stopping were still live on Twitch; the fully read check covers one step only.
- Streamers using different names on Kick and Twitch are missed, and a change of name looks like stopping.
- Four weeks only; 5 October 2026 is not covered.
- Behaviour only: no Partner status, contracts, payouts or reasons for stopping.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Do streamers keep simulcasting? Kick and Twitch simulcasters over four weeks, 2026*. https://playersells.com/learn/do-streamers-keep-simulcasting-kick-and-twitch-four-weeks-measured. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
