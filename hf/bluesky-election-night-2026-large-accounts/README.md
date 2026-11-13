---
license: cc-by-4.0
pretty_name: "Bluesky's 2026 US midterm election night spike among accounts with 10,000+ followers"
language:
- en
tags:
- bluesky
- social-media
- elections
- us-midterms-2026
- posting-activity
- at-protocol
size_categories:
- n<1K
configs:
- config_name: daily_posts
  data_files: "daily_posts.csv"
  default: true
- config_name: by_topic_group
  data_files: "by_topic_group.csv"
- config_name: by_topic_label
  data_files: "by_topic_label.csv"
- config_name: by_language
  data_files: "by_language.csv"
- config_name: by_follower_band
  data_files: "by_follower_band.csv"
- config_name: by_join_date
  data_files: "by_join_date.csv"
- config_name: weekly_net_new_followers
  data_files: "weekly_net_new_followers.csv"
- config_name: x_very_large_accounts
  data_files: "x_very_large_accounts.csv"
---
# Bluesky's 2026 US midterm election night spike among accounts with 10,000+ followers

Daily posting by a fixed panel of 34,033 Bluesky accounts with 10,000 or more followers, from 6 October to 11 November 2026. On 4 November 2026 (UTC), the night the US midterm results came in, the panel posted 59.5% more than on the same weekday in the four weeks before; four days later the excess was 5.4%. Over election week the panel wrote 23.5% more than in a normal week. Breakdowns by topic label, profile language, follower band and account creation date, plus weekly net new followers.

**Measured:** Daily readings of public profile counters, 6 October to 11 November 2026 (UTC), read 13 November 2026  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [Bluesky's Election Night Spike Faded in Four Days](https://playersells.com/learn/how-long-did-blueskys-election-night-spike-last-34033-accounts-measured)

## Files

### `daily_posts.csv` (11 rows)

Posts and replies written by the panel on each UTC day from 1 to 11 November 2026, against the same weekday average of the four baseline weeks.

| Column | Type | Description |
|---|---|---|
| `day_utc` | date | UTC day |
| `weekday` | string | Day of the week |
| `posts` | integer | Posts and replies by the 34,033 accounts (reposts are not counted) |
| `baseline_same_weekday` | integer | Average of the same weekday, 6 October to 2 November 2026 |
| `difference_pct` | number | Posts against the baseline, percent |

### `by_topic_group.csv` (4 rows)

Politics, news, other labelled topics and unlabelled accounts.

| Column | Type | Description |
|---|---|---|
| `account_group` | string | Topic group (label from keywords in the profile bio) |
| `accounts` | integer | Accounts in the group |
| `baseline_posts_per_account_per_day` | number | Posts per account per day in the baseline |
| `peak_day_pct` | number | 4 November against the group's own baseline, percent |
| `election_week_pct` | number | 3 to 9 November against the group's average baseline week, percent |
| `nov_10_11_pct` | number | 10 and 11 November against the same weekdays of the baseline, percent |
| `share_of_extra_posts_pct` | number | Share of the panel's net extra posts of election week |

### `by_topic_label.csv` (14 rows)

Single topic labels with at least 300 accounts in the panel.

| Column | Type | Description |
|---|---|---|
| `topic_label` | string | Topic label |
| `accounts` | integer | Accounts with the label |
| `peak_day_pct` | number | 4 November against the group's own baseline, percent |
| `election_week_pct` | number | 3 to 9 November against the group's average baseline week, percent |

### `by_language.csv` (8 rows)

English against all other detected profile languages, and single languages with at least 300 accounts.

| Column | Type | Description |
|---|---|---|
| `profile_language` | string | Language detected from the profile text |
| `accounts` | integer | Accounts |
| `peak_day_pct` | number | 4 November against the group's own baseline, percent |
| `election_week_pct` | number | 3 to 9 November against the group's average baseline week, percent |

### `by_follower_band.csv` (4 rows)

The panel split by follower count on 6 October 2026.

| Column | Type | Description |
|---|---|---|
| `followers_on_oct_6` | string | Follower band |
| `accounts` | integer | Accounts |
| `baseline_posts_per_account_per_day` | number | Posts per account per day in the baseline |
| `peak_day_pct` | number | 4 November against the band's own baseline, percent |
| `election_week_pct` | number | 3 to 9 November against the band's average baseline week, percent |

### `by_join_date.csv` (4 rows)

The panel split by account creation date, with the share that did not post in the 28 baseline days.

| Column | Type | Description |
|---|---|---|
| `account_created` | string | Creation period |
| `accounts` | integer | Accounts |
| `silent_28_days_before_pct` | number | Share whose post counter did not change from 6 October to 2 November 2026 |
| `peak_day_pct` | number | 4 November against the group's own baseline, percent |
| `election_week_pct` | number | 3 to 9 November against the group's average baseline week, percent |

### `weekly_net_new_followers.csv` (5 rows)

Net change in the panel's combined follower count, Tuesday to Monday weeks.

| Column | Type | Description |
|---|---|---|
| `week_2026` | string | Week (UTC) |
| `net_new_followers` | integer | Net new followers across the panel |
| `change_on_previous_week_pct` | number | Change on the previous week, percent (empty for the first week) |

### `x_very_large_accounts.csv` (4 rows)

Context only: the same test on a separate sample of very large X accounts (median 3,813,048 followers). Not a platform comparison.

| Column | Type | Description |
|---|---|---|
| `x_account_group` | string | Group of X accounts |
| `accounts` | integer | Accounts |
| `peak_day_pct` | number | 4 November against the group's own baseline, percent |
| `election_week_pct` | number | 3 to 9 November against the group's average baseline week, percent |

## How it was measured

Source: the PlayerSells Bluesky directory reads the public profile counters (followers, posts) of every account above 10,000 followers about once a day (median 24.4 hours between readings).

For each account the post counter at every midnight UTC was estimated by linear interpolation between the readings on either side; a day's posts are the difference between consecutive midnights.

Panel: accounts with 10,000+ followers on 6 October 2026 and a reading on both sides of every midnight with no gap above 50 hours (34,290 accounts), minus 257 accounts that averaged more than 100 posts a day in the baseline or whose counter fell by 100 or more between two readings: 34,033 accounts.

Baseline: the four Tuesday to Monday weeks from 6 October to 2 November 2026; each day is compared with the average of the same weekday. Election week is 3 to 9 November 2026.

Topic labels come from keywords in the profile bio; language is detected from the profile text. No account name, handle or identifier is included. Aggregates only.

## Limitations

- Accounts with 10,000+ followers only: smaller accounts and people who joined during the election are not covered.
- One reading a day: day boundaries are blurred, which lowers the peak day and raises its neighbours.
- The post counter is net of deletions and counts posts and replies, not reposts or likes.
- The look a week later covers two days (10 and 11 November 2026).
- The X file describes much larger accounts and a counter that includes reposts; it is context, not a comparison.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Bluesky's 2026 US midterm election night spike among accounts with 10,000+ followers*. https://playersells.com/learn/how-long-did-blueskys-election-night-spike-last-34033-accounts-measured. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
