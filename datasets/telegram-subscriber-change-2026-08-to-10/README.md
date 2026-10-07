# Telegram channel subscriber change by topic, August to October 2026

Which Telegram channels gained or lost subscribers between early August and early October 2026, by topic and starting size. 85.6% of 814 crypto channels lost subscribers, against 64.6% of all 14,874 channels in the panel.

**Measured:** First reading 1 to 7 August 2026, last reading 26 September to 2 October 2026  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [Crypto Telegram Channels Are Shrinking: 86% Lost Subscribers](https://playersells.com/learn/crypto-telegram-channels-are-losing-subscribers-measured)

## Files

### `subscriber_change_by_category.csv` (7 rows)

Share of channels that lost or gained subscribers, and the median change, by topic.

| Column | Type | Description |
|---|---|---|
| `category` | string | Topic label from a keyword classifier, or Not classified, or All channels |
| `channels` | integer | Channels in the panel with that label |
| `lost_subscribers_pct` | number | Share of those channels whose last reading was lower than their first |
| `gained_subscribers_pct` | number | Share whose last reading was higher |
| `median_change_pct` | number | Median percentage change in subscribers between the two readings |

### `shrink_rate_by_size.csv` (12 rows)

Share of channels that lost subscribers, by starting size and topic.

| Column | Type | Description |
|---|---|---|
| `starting_size_band` | string | Subscribers at the first reading |
| `category` | string | Topic label |
| `channels` | integer | Channels in the cell; empty when too few to publish |
| `lost_subscribers_pct` | number | Share that lost subscribers; empty when too few to publish |

## How it was measured

PlayerSells' crawler stores a daily subscriber reading for the Telegram channels it tracks closely. For each channel the first reading between 1 and 7 August 2026 was compared with the last reading between 26 September and 2 October 2026, a median of 62 days later.

Only broadcast channels with at least 1,000 subscribers at the first reading are included; groups are excluded. That leaves 14,874 channels.

Topic labels come from a keyword classifier over each channel's name and description. 3,471 of the 14,874 channels carry a label; the rest are Not classified. Topics with fewer than 150 channels are not shown.

Every central figure is a median.

## Limitations

- The panel is made of large channels: only 27 of the 14,874 started below 10,000 subscribers and the median channel started with 121,871.
- The panel is not a random sample of Telegram. Private channels and channels nobody links to are missing.
- Topic labels are approximate and about three quarters of the panel has none.
- Nine weeks is short, and the data does not say why channels lost subscribers.
- PlayerSells collects these numbers with its own crawlers. They describe what those crawlers read, not a census of any platform.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Telegram channel subscriber change by topic, August to October 2026*. https://playersells.com/learn/crypto-telegram-channels-are-losing-subscribers-measured. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
