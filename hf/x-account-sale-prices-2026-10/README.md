---
license: cc-by-4.0
pretty_name: "Prices X (Twitter) accounts sold for in completed escrow deals, 2026"
language:
- en
tags:
- twitter
- x
- account-prices
- social-media-accounts
- marketplace
- escrow
- creator-economy
- prices
size_categories:
- n<1K
configs:
- config_name: sale_prices_by_follower_band
  data_files: "sale_prices_by_follower_band.csv"
  default: true
- config_name: discount_vs_asking_price
  data_files: "discount_vs_asking_price.csv"
- config_name: asking_vs_sale_price
  data_files: "asking_vs_sale_price.csv"
- config_name: sell_through_by_asking_price
  data_files: "sell_through_by_asking_price.csv"
- config_name: sales_by_price_bracket
  data_files: "sales_by_price_bracket.csv"
- config_name: blue_check_by_follower_band
  data_files: "blue_check_by_follower_band.csv"
- config_name: price_by_account_age
  data_files: "price_by_account_age.csv"
---
# Prices X (Twitter) accounts sold for in completed escrow deals, 2026

What X (Twitter) accounts actually sold for in 187 completed PlayerSells escrow deals between 21 May and 19 October 2026: final prices paid, not asking prices. The median sale was $60 and half of all sales closed between $19 and $125. The median price per 1,000 followers fell from $35.48 at 1,000 to 2,500 followers to $6.93 at 20,000 and up. 69.5% of accounts sold at their asking price.

**Measured:** Completed sales 21 May to 19 October 2026, read 20 October 2026  
**Publisher:** PlayerSells (https://playersells.com)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Attribution:** Source: PlayerSells (https://playersells.com)

## Where the numbers are published

- [What X Accounts Actually Sell For: 187 Escrow Sales](https://playersells.com/learn/what-x-accounts-actually-sell-for-2026-escrow-data)
- [X (Twitter) account prices, updated from every completed sale](https://playersells.com/pricing/x-account-prices-2026)

## Files

### `sale_prices_by_follower_band.csv` (6 rows)

Completed sales by the account's follower count: median and middle 50% of the sale price, and the median price per 1,000 followers.

| Column | Type | Description |
|---|---|---|
| `follower_band` | string | Follower count recorded on the listing when it sold |
| `sales` | integer | Completed sales in the band |
| `median_usd` | number | Median final sale price, US dollars |
| `p25_usd` | number | 25th percentile sale price |
| `p75_usd` | number | 75th percentile sale price |
| `median_followers` | integer | Median follower count of the accounts sold |
| `median_usd_per_1000_followers` | number | Median across sales of price divided by followers, times 1,000 |

### `discount_vs_asking_price.csv` (6 rows)

Share of completed sales that closed below the listing's asking price, and the median discount of those.

| Column | Type | Description |
|---|---|---|
| `follower_band` | string | Follower count recorded on the listing |
| `sales` | integer | Completed sales in the band |
| `closed_below_ask_pct` | number | Share of sales whose final price was below the asking price |
| `median_discount_when_below_pct` | number | Median of (1 - sale price / asking price) among those, in percent |

### `asking_vs_sale_price.csv` (6 rows)

Median asking price of X accounts listed on 20 October 2026 against the median completed sale price, by follower count.

| Column | Type | Description |
|---|---|---|
| `follower_band` | string | Follower count on the listing |
| `live_listings` | integer | X accounts listed for sale on 20 October 2026 |
| `median_ask_usd` | number | Median asking price of those listings |
| `median_sale_usd` | number | Median completed sale price in the band |
| `ask_divided_by_sale` | number | Median ask divided by median sale |

### `sell_through_by_asking_price.csv` (5 rows)

Share of X listings that sold, by asking price, for listings live on or before 20 September 2026 (at least 30 days on the market).

| Column | Type | Description |
|---|---|---|
| `asking_price` | string | Current asking price of the listing |
| `listings` | integer | Listings that went live on or before 20 September 2026 |
| `sold` | integer | Of those, listings with a completed escrow sale by 19 October 2026 |
| `sold_pct` | number | Share sold |

### `sales_by_price_bracket.csv` (6 rows)

Completed sales by final price bracket.

| Column | Type | Description |
|---|---|---|
| `sale_price` | string | Final sale price bracket, US dollars |
| `sales` | integer | Completed sales in the bracket |
| `share_pct` | number | Share of all 187 sales |

### `blue_check_by_follower_band.csv` (4 rows)

Median sale price of accounts with and without a blue check, by follower count, independent sellers only; bands with fewer than 5 verified sales are left out.

| Column | Type | Description |
|---|---|---|
| `follower_band` | string | Follower count on the listing |
| `verified_sales` | integer | Sales of accounts that showed a blue check when listed |
| `verified_median_usd` | number | Their median sale price |
| `unverified_sales` | integer | Sales of accounts without one |
| `unverified_median_usd` | number | Their median sale price |

### `price_by_account_age.csv` (3 rows)

Sale price by account age, compared inside each follower band, independent sellers only.

| Column | Type | Description |
|---|---|---|
| `account_age` | string | Age of the X account when listed |
| `sales` | integer | Completed sales |
| `price_vs_band_median` | number | Median of (sale price / median sale of the account's follower band); 1.00 = typical for its size |
| `median_usd` | number | Median sale price, all sizes mixed |

## How it was measured

Every figure comes from the PlayerSells marketplace database, read on 20 October 2026. A sale is an escrow deal for an X account that reached completed status: the account was handed over and the payment was released to the seller. Cancelled and refunded deals never reach that status. Price is the final amount the buyer paid, in US dollars; the seller's escrow fee comes out of it.

Follower count, blue check, account age and asking price are the listing's own fields. While a listing is live they are refreshed from X; they stop updating when it sells.

70 internal records created to fill the seller leaderboard, between two PlayerSells staff accounts, are excluded, and one sale whose listing had no follower count is left out: 187 sales, one per listing, from 118 buyers and 90 sellers. The filters are the same as on the live X account prices page. Medians and percentiles are computed without trimming or weighting.

28 of the 187 sales were accounts sold by the PlayerSells store at set prices of $80 to $400. They are in the price, discount and bracket tables and left out of the blue check and account age tables, which compare each sale with the median sale of its follower band among independent sellers.

No account, handle, buyer or seller is included. The files hold aggregates only.

## Limitations

- 187 sales is a small sample; rows with 10 to 25 sales can move as more deals close.
- Prices from one escrow marketplace. Private deals and other marketplaces may close at different prices.
- Asking prices are read from the listing on 20 October 2026; a seller who edited the price during a negotiation shows as sold at the ask.
- Blue check and account age comparisons are observational and rest on small groups.
- Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. PlayerSells cannot separate real people from bots, embedded players or inflated counts.

## How to cite

PlayerSells (2026). *Prices X (Twitter) accounts sold for in completed escrow deals, 2026*. https://playersells.com/learn/what-x-accounts-actually-sell-for-2026-escrow-data. Licensed under CC BY 4.0.

When you reuse these numbers, credit "Source: PlayerSells (https://playersells.com)" with a link.

Rebuild from source: `python build.py --refresh` in the repository root.
