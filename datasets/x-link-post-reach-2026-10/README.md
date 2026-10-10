# Views on X (Twitter) posts with a link against the same account's posts without one, 2026

How many views X (Twitter) posts with a link drew compared with the same account's posts without a link, measured on 6,447,046 original posts from 285,579 accounts published between 15 July and 7 October 2026. For the median account, text posts with a link drew 10.4% fewer views; for accounts with over 1 million followers, 30.4% fewer; for accounts under 1,000 followers, 16.6% more.

**Measured:** Original posts published 15 July to 7 October 2026, views read at least 48 hours after posting  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [Does X Still Penalize Links? 6.4 Million Posts Measured](https://playersells.com/learn/does-x-still-penalize-links-we-measured-6-million-posts)

## Files

### `link_gap_overall.csv` (2 rows)

The within-account view gap for link posts, text-only posts and posts with an image or video.

| Column | Type | Description |
|---|---|---|
| `post_type` | string | Text only, or with image or video |
| `accounts` | integer | Accounts with at least three link posts and three link-free posts of this type |
| `views_change_pct` | number | Median across accounts of (median views of link posts / median views of link-free posts) minus 1, in percent |
| `accounts_with_fewer_views_pct` | number | Share of those accounts whose link posts got fewer views |

### `link_gap_by_follower_band.csv` (5 rows)

The same gap by the account's follower count.

| Column | Type | Description |
|---|---|---|
| `follower_band` | string | Follower band, from the median follower count recorded when the account's posts were read |
| `text_accounts` | integer | Accounts in the text-only comparison |
| `text_views_change_pct` | number | Median view change on text posts with a link |
| `media_accounts` | integer | Accounts in the image or video comparison |
| `media_views_change_pct` | number | Median view change on image or video posts with a link |

### `link_gap_by_category.csv` (12 rows)

The same gap by account topic, for topics with at least 100 accounts in the text comparison.

| Column | Type | Description |
|---|---|---|
| `account_category` | string | Topic from the PlayerSells account classifier, or none assigned |
| `text_accounts` | integer | Accounts in the text-only comparison |
| `text_views_change_pct` | number | Median view change on text posts with a link |
| `media_accounts` | integer | Accounts in the image or video comparison |
| `media_views_change_pct` | number | Median view change on image or video posts with a link |

### `link_gap_by_period.csv` (3 rows)

The same gap in three periods of 2026: before Elon Musk's late July statement that X had not penalized links for over a year, after it, and after X's 8 September creator payout change.

| Column | Type | Description |
|---|---|---|
| `period_2026` | string | Publication dates of the posts |
| `text_accounts` | integer | Accounts in the text-only comparison inside the period |
| `text_views_change_pct` | number | Median view change on text posts with a link |
| `media_accounts` | integer | Accounts in the image or video comparison inside the period |
| `media_views_change_pct` | number | Median view change on image or video posts with a link |

### `engagement_per_view_change.csv` (4 rows)

Change in likes, replies, reposts and bookmarks per view on link posts against the same account's link-free posts.

| Column | Type | Description |
|---|---|---|
| `measure` | string | Engagement measure per view |
| `text_change_pct` | number | Median change for text posts with a link, from each group's totals |
| `media_change_pct` | number | Median change for image or video posts with a link |

### `link_placement.csv` (4 rows)

Views on posts with the link in the post and posts with the link only in the author's own reply, against the same account's posts with no link.

| Column | Type | Description |
|---|---|---|
| `link_location` | string | In the post, or in the author's own reply |
| `post_type` | string | Text only, or with image or video |
| `accounts` | integer | Accounts with at least three link-in-reply posts and three posts in the group |
| `views_change_vs_no_link_pct` | number | Median view change against the same account's posts with no link |

## How it was measured

PlayerSells' X crawler reads public posts of the accounts in its directory. Every original post it had read that was published between 15 July and 7 October 2026 is used: 6,447,046 posts from 285,579 accounts. Reposts, quote posts, replies and thread continuations are excluded. Only posts whose view counter was read at least 48 hours after publication are kept.

A link post is one for which X reports at least one URL. Uploaded photos and videos are not links. Posts are split into text only and posts with an image or video.

For each account with at least three link posts and three link-free posts of the same type, the median views of its link posts are divided by the median views of its link-free posts. Tables report the median of those ratios across accounts, as a percent change. 68,604 accounts had at least three posts with a link and three without.

A link-in-reply post is an original post without a link whose author replied to it with a post that carries a link.

## Limitations

- Observational: comparing an account with itself removes differences between accounts, not differences between the posts an account chooses to link.
- The figures describe outcomes. They cannot show whether X applies a rule to links.
- The crawler reads the largest accounts first, so small accounts are fewer in the sample.
- Views are X's own impression counter, taken as published.
- No post data from before July 2026 is included.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Views on X (Twitter) posts with a link against the same account's posts without one, 2026*. https://playersells.com/learn/does-x-still-penalize-links-we-measured-6-million-posts. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
