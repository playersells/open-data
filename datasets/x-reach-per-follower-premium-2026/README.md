# X (Twitter) views per follower by account size and Premium badge, 2026

How many views an X account's typical post gets relative to its follower count, by account size, and how accounts with the blue Premium badge compare with no-badge accounts of the same size. Premium accounts drew 1.6x to 1.8x the views per follower between 5,000 and 1 million followers. This is a correlation, not proof that Premium causes it.

**Measured:** Engagement records computed 19 August to 3 October 2026, each covering 30 days of posts  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [X Premium Linked to 1.6x-1.8x More Reach at the Same Size](https://playersells.com/learn/does-x-premium-increase-reach-60000-accounts-compared)

## Files

### `reach_by_follower_band.csv` (5 rows)

Median post views and engagement as a share of followers, by follower band.

| Column | Type | Description |
|---|---|---|
| `follower_band` | string | Follower band |
| `accounts` | integer | Accounts in the band |
| `median_followers` | integer | Median follower count inside the band |
| `median_views_per_post` | integer | Median of the accounts' median original-post views |
| `views_per_follower_pct` | number | Median views as a share of followers |
| `views_per_follower_p25_pct` | number | 25th percentile |
| `views_per_follower_p75_pct` | number | 75th percentile |
| `engagement_per_follower_pct` | number | Median likes, replies, reposts and quotes on the median post, as a share of followers |

### `premium_vs_no_badge.csv` (5 rows)

Views per follower for Premium and no-badge accounts of the same size.

| Column | Type | Description |
|---|---|---|
| `follower_band` | string | Follower band |
| `band_note` | string | Median follower counts of the two groups, as published |
| `premium_accounts` | integer | Accounts with the blue badge and no organisation badge |
| `no_badge_accounts` | integer | Accounts with no badge |
| `premium_views_per_follower_pct` | number | Median for Premium accounts |
| `no_badge_views_per_follower_pct` | number | Median for no-badge accounts |
| `ratio` | number | Premium divided by no badge; empty where there are too few accounts to compare |

### `premium_by_posting_rate.csv` (9 rows)

The Premium comparison split by how often accounts post.

| Column | Type | Description |
|---|---|---|
| `follower_band` | string | Follower band |
| `posts_per_day` | string | Posting-rate group |
| `premium_accounts` | integer | Premium accounts in the group |
| `no_badge_accounts` | integer | No-badge accounts in the group |
| `premium_views_per_follower_pct` | number | Median for Premium accounts |
| `no_badge_views_per_follower_pct` | number | Median for no-badge accounts |

## How it was measured

PlayerSells' X engine reads the recent public posts of accounts in its index and keeps one engagement record per account, covering the 30 days before it was computed. Records computed between 19 August and 3 October 2026 are used.

Accounts with at least 10 original posts in the window and at most 10% retweets are kept: 60,892 accounts. Reach is the median view count of the account's original posts divided by its follower count when the record was computed.

Premium means the blue badge and no organisation badge. 6,955 accounts with gold or grey organisation badges are left out of the comparison, leaving 53,937. The badge is read at the most recent crawl, a median of 7.2 days after the engagement record.

Every figure is a median.

## Limitations

- Correlation only. People who pay for Premium may differ in ways the data cannot see.
- Not a random sample of X: the engine reads accounts in size tiers, largest first, so each band is dense near its top. Use the median follower count of each band.
- Views are X's own impression counter and include people who do not follow the account.
- Badge status is current, not historical, and Premium and Premium+ cannot be told apart.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *X (Twitter) views per follower by account size and Premium badge, 2026*. https://playersells.com/learn/does-x-premium-increase-reach-60000-accounts-compared. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
