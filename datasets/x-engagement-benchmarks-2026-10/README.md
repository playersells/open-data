# X (Twitter) engagement rate benchmarks and posting pattern effects, October 2026

Engagement rate percentiles for 152,187 measured X accounts, broken down by follower band, and 45 posting pattern effects (hour, weekday, length, hashtags, links, media) measured within accounts with 95% intervals.

**Measured:** Trailing 30-day windows ending 6 and 7 October 2026 (see the files)  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [What Is a Good Engagement Rate on X?](https://playersells.com/insights/engagement-rate-benchmarks)
- [X Engagement Insights](https://playersells.com/insights)
- [Machine-readable findings (JSON)](https://playersells.com/insights/data.json)

## Files

### `engagement_rate_percentiles.csv` (6 rows)

Engagement rate percentiles across all measured accounts.

| Column | Type | Description |
|---|---|---|
| `statistic` | string | p10, p25, p50, p75, p90 or mean |
| `engagement_rate_pct` | number | Median interactions per original post divided by followers, in percent |
| `accounts` | integer | Accounts in the measured population |
| `window_end` | date | Last day of the 30-day window |

### `engagement_rate_by_follower_band.csv` (8 rows)

Engagement rate quartiles by follower band. Bands with fewer than 30 accounts are not shown.

| Column | Type | Description |
|---|---|---|
| `follower_band` | string | Follower band |
| `accounts` | integer | Accounts in the band |
| `p25_engagement_rate_pct` | number | Lower quartile |
| `median_engagement_rate_pct` | number | Median |
| `p75_engagement_rate_pct` | number | Upper quartile |
| `window_end` | date | Last day of the 30-day window |

### `posting_pattern_effects.csv` (45 rows)

Within-account effect of a posting choice on engagement, with a distribution-free 95% interval.

| Column | Type | Description |
|---|---|---|
| `dimension` | string | hour_utc, dow, length_bucket, hashtag_count, link, media or video |
| `bucket` | string | The value of the dimension |
| `label` | string | Readable label |
| `effect_pct` | number | Median per-account change in engagement on posts in the bucket against the same accounts' other posts |
| `effect_lo_pct` | number | Lower end of the 95% interval |
| `effect_hi_pct` | number | Upper end of the 95% interval |
| `significant` | boolean | true when the effect survives a Benjamini-Hochberg multiple-testing correction across all findings and at least 30 accounts contribute. A raw 95% interval that excludes zero is not enough on its own |
| `accounts` | integer | Accounts contributing |
| `accounts_agreeing` | integer | Accounts whose own effect points the same way as the median |
| `posts` | integer | Posts in the bucket |
| `median_multiple` | number | Median of the per-account engagement multiples |
| `p90_multiple` | number | 90th percentile of the per-account multiples |
| `window_end` | date | Last day of the 30-day window |

## How it was measured

Engagement rate is the median number of interactions (likes, reposts, replies and quotes) on an account's original posts over a 30-day window, divided by the account's follower count. Replies and reposts by the account are excluded.

Percentiles are computed in the database over every account with at least 8 original posts in the window, with linear interpolation. The measured population held 152,187 accounts, from 985 to 242M followers with a median of 78K.

Posting pattern effects compare, within each account, the median engagement of posts in a bucket with the same account's other posts, giving one ratio per account. The effect is the median of those ratios with a distribution-free 95% interval, so account size cancels out and the unit of evidence is the account, not the post. A finding is marked significant only after a Benjamini-Hochberg correction for testing many buckets at once, so a few rows have a raw interval that excludes zero and are still reported as no measurable difference.

These figures are recomputed daily on playersells.com. This file is a snapshot; build.py --refresh takes a new one.

## Limitations

- The accounts are the ones the catalog has scanned deeply enough to produce a stable median. The catalog is scanned largest first, so this is not a random sample of X.
- Pooled percentiles mix very different account sizes. Compare an account with its own band.
- Effects are observational associations, not causal estimates.
- Interaction counts are read at collection time, not live.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *X (Twitter) engagement rate benchmarks and posting pattern effects, October 2026*. https://playersells.com/insights/engagement-rate-benchmarks. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
