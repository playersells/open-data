"""
Descriptions of every dataset in this repository.

build.py writes the CSV files, then renders three documents per dataset from
the entries below: the dataset README, the Hugging Face dataset card and the
Kaggle dataset-metadata.json. Keeping the words in one place means the three
platforms cannot drift apart.

House rules for the text: plain English, no em dashes, no claims about size or
superiority, and every number must be one that is published on playersells.com.
"""

SITE = "https://playersells.com"
ATTRIBUTION = "Source: PlayerSells (https://playersells.com)"
LICENSE_NAME = "CC BY 4.0"
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"

COMMON_LIMITS = [
    "PlayerSells collects these numbers with its own crawlers. They describe what those crawlers "
    "read, not a census of any platform.",
    "Counts shown by the platforms (followers, subscribers, views, viewers) are taken as displayed. "
    "PlayerSells cannot separate real people from bots, embedded players or inflated counts.",
]

DATASETS = [
    # ------------------------------------------------------------------
    {
        "slug": "social-follower-percentiles-2026-10",
        "title": "Follower count percentiles on seven social platforms (October 2026)",
        "kaggle_title": "Follower Count Percentiles, 7 Platforms 2026",
        "subtitle": "Followers or subscribers at every percentile for X, Bluesky, Telegram and more",
        "summary": (
            "How many followers or subscribers an account needs to reach each percentile on X (Twitter), "
            "Bluesky, Telegram, TikTok, YouTube, Kick and Twitch, measured on 5 October 2026 over the "
            "accounts in the PlayerSells index."
        ),
        "measured": "5 October 2026",
        "method_urls": [
            ("X (Twitter) follower rank", SITE + "/tools/twitter-follower-rank"),
            ("Bluesky follower rank", SITE + "/tools/bluesky-follower-rank"),
            ("Telegram channel rank", SITE + "/tools/telegram-channel-rank"),
            ("TikTok follower rank", SITE + "/tools/tiktok-follower-rank"),
            ("YouTube subscriber rank", SITE + "/tools/youtube-subscriber-rank"),
            ("Kick follower rank", SITE + "/tools/kick-follower-rank"),
            ("Twitch follower rank", SITE + "/tools/twitch-follower-rank"),
        ],
        "keywords": ["social media", "followers", "percentiles", "twitter", "telegram", "youtube",
                     "tiktok", "twitch", "kick", "bluesky", "creator economy"],
        "files": [
            {
                "name": "follower_percentiles.csv",
                "description": "One row per platform and percentile: the follower or subscriber count at that percentile.",
                "columns": [
                    ("platform", "string", "x, bluesky, telegram, tiktok, youtube, kick or twitch"),
                    ("percentile", "number", "0 to 99 in steps of 1, then the extra top-1% breakpoints (99.5, 99.8, 99.9, 99.95, 99.99) where the sample is large enough"),
                    ("value", "integer", "Followers (subscribers on Telegram and YouTube) at that percentile"),
                    ("metric", "string", "followers or subscribers"),
                    ("measured_on", "date", "Date the percentile ladder was measured"),
                ],
            },
            {
                "name": "platforms.csv",
                "description": "One row per platform: what was measured, how many accounts, and how far the numbers generalise.",
                "columns": [
                    ("platform", "string", "Platform key used in follower_percentiles.csv"),
                    ("label", "string", "Platform name"),
                    ("unit", "string", "What one row of the index is (account, channel, creator)"),
                    ("metric", "string", "followers or subscribers"),
                    ("framing", "string", "population: the index has a long tail of small accounts; tracked: the catalog covers a selected part of the platform and percentiles describe that part only"),
                    ("sample_size", "integer", "Accounts the percentiles were computed over"),
                    ("indexed_total", "integer", "Accounts in the PlayerSells index for that platform when measured"),
                    ("measured_on", "date", "Date the percentiles were measured"),
                    ("coverage_note", "string", "What the sample does and does not represent"),
                    ("method_url", "string", "Page on playersells.com that publishes and explains these numbers"),
                ],
            },
        ],
        "method": [
            "For each platform PlayerSells computes a 101-point ladder of the follower or subscriber count "
            "(percentile_disc at every whole percentile) over the accounts in its index. On X, Bluesky and "
            "Telegram the ladder is computed over a sample of the index (459,415 of 22,837,969 X accounts, "
            "970,889 of 4,173,274 Bluesky accounts, 1,020,191 of 3,384,503 Telegram channels). TikTok, "
            "YouTube and Twitch are measured whole. On Kick the ladder covers the 328,559 channels whose "
            "follower count has been read, out of 458,657 in the catalog, because Kick's live directory "
            "does not return follower counts and a separate per-channel pass fills them in.",
            "Inside the top 1% a single step from p99 to p100 spans several orders of magnitude, so extra "
            "breakpoints are measured at 99.5, 99.8, 99.9, 99.95 and 99.99 where the sample holds enough "
            "accounts above them. TikTok and YouTube stop at 99.9.",
            "p100, the single largest account in each sample, is left out: it is one account, not a "
            "distribution, and on a sampled platform it is not even the largest account in the index.",
            "These are the same ladders the rank tools on playersells.com use to place an account.",
        ],
        "limits": [
            "Percentiles describe the accounts in the PlayerSells index, which is built by crawling public "
            "profiles. Accounts nobody links to, private accounts and deleted accounts are missing.",
            "TikTok and YouTube are tracked catalogs seeded from larger creators (median 5,738 TikTok "
            "followers and 63,500 YouTube subscribers), so a small creator placing low there has learned "
            "something about the catalog, not about the platform.",
            "Kick and Twitch hold channels PlayerSells has recorded going live, not every registered "
            "account. Read their percentiles as a place among channels that actually stream.",
            "The streaming catalogs grow every week, so their ladders date quickly.",
        ],
    },
    # ------------------------------------------------------------------
    {
        "slug": "kick-twitch-category-viewing-2026-09-26",
        "title": "Kick and Twitch share of viewing by category, week of 26 September 2026",
        "kaggle_title": "Kick vs Twitch Viewing by Category, Sep 2026",
        "subtitle": "Share of concurrent viewers per category, gambling included, same week",
        "summary": (
            "Share of concurrent viewing that each streaming category took on Kick and on Twitch from "
            "26 September to 2 October 2026, daily and for the whole week, measured with one method on "
            "both platforms. Gambling took 7.2% of Kick viewing and 1.7% of Twitch viewing on these readings."
        ),
        "measured": "26 September 2026 00:00 UTC to 3 October 2026 00:00 UTC",
        "method_urls": [
            ("How Much of Kick Is Gambling? One Week vs Twitch",
             SITE + "/learn/how-much-of-kick-is-gambling-one-week-measured-against-twitch"),
        ],
        "keywords": ["kick", "twitch", "live streaming", "gambling", "slots", "viewership", "categories"],
        "files": [
            {
                "name": "category_viewing_share.csv",
                "description": "Share of concurrent viewing per category, per platform, per day and for the whole week.",
                "columns": [
                    ("platform", "string", "kick or twitch"),
                    ("period", "string", "A UTC date (YYYY-MM-DD) or week for the whole seven days"),
                    ("category", "string", "Kick category slug or Twitch category name, as the platforms publish them. One row per period groups every category with fewer than 5 channels"),
                    ("share_of_viewing_pct", "number", "Viewers in the category as a percentage of all viewers on the platform in that period"),
                    ("channels", "integer", "Distinct channels seen live in the category during the period. On Twitch this counts only streams that reached the top 30 of their category"),
                    ("is_gambling", "boolean", "true for the categories counted as gambling: Kick slots, poker and sports-betting; Twitch Slots, Poker and Virtual Casino"),
                ],
            },
            {
                "name": "gambling_share_week.csv",
                "description": "The gambling comparison table as published, for the whole week.",
                "columns": [
                    ("category", "string", "Gambling category or the total"),
                    ("kick_share_of_viewing_pct", "number", "Share of Kick viewing; empty where Kick has no such category"),
                    ("twitch_share_of_viewing_pct", "number", "Share of Twitch viewing; empty where Twitch has no such category"),
                ],
            },
            {
                "name": "rank_comparison_30d.csv",
                "description": "Channels by average concurrent viewers while live, Twitch against Kick, 30 days to 3 October 2026.",
                "columns": [
                    ("measure", "string", "What is counted"),
                    ("twitch", "integer", "Value on Twitch"),
                    ("kick", "integer", "Value on Kick"),
                ],
            },
        ],
        "method": [
            "Kick: a sampler walks Kick's whole public live directory page by page and records every live "
            "channel's viewer count and category. Over the week it recorded 201,070 channels.",
            "Twitch: Twitch's public interface does not let a crawler page through the full live list, so "
            "the sampler reads every category every 15 minutes and records up to 30 streams per category, "
            "the most watched first. Over the week it recorded 385,643 channels.",
            "Share of viewing: one reading per channel per 15-minute block (the average if there were "
            "several), viewers summed by category and divided by the platform total for the period. This is "
            "the share of concurrent viewers, not of hours watched.",
            "A spot check on 3 October 2026 found the Twitch sampler holding about 62% of the viewers "
            "Twitch's own counters showed in Slots, Virtual Casino and Poker, against about 70% in other "
            "large categories. Adjusted for that, Twitch's gambling share is about 1.9%. The Kick sampler "
            "held about 95% to 97% of Kick's own counters.",
            "The rank comparison counts channels live at least once in the 10 days to 3 October 2026, "
            "ranked by average concurrent viewers while live over the 30 days to that date.",
        ],
        "limits": [
            "One week. Gambling viewing moves with events and individual streamers.",
            "Category labels are the streamers' own. A slots stream filed under Just Chatting counts as "
            "Just Chatting.",
            "The Twitch sampler sees only the top 30 streams of each category at a time, so Twitch channel "
            "counts are floors and Twitch shares in very large categories miss the long tail.",
            "No absolute viewer or hours-watched totals are published, because the samplers measure shares "
            "more reliably than totals.",
        ],
    },
    # ------------------------------------------------------------------
    {
        "slug": "kick-twitch-simulcasting-2026-09-28",
        "title": "Kick and Twitch simulcasting, week of 28 September 2026",
        "kaggle_title": "Kick and Twitch Simulcasting, Sep-Oct 2026",
        "subtitle": "5,063 streamers live on both at once and where their viewers watched",
        "summary": (
            "Streamers who broadcast on Kick and Twitch at the same time from 28 September to 4 October "
            "2026, and how their concurrent viewers split between the two platforms. Twitch drew 83.3% of "
            "the combined viewers and Kick 16.7%."
        ),
        "measured": "28 September 2026 00:00 UTC to 5 October 2026 00:00 UTC",
        "method_urls": [
            ("Kick and Twitch Simulcasts: 83% of Viewers Watch on Twitch",
             SITE + "/learn/kick-and-twitch-simulcasting-measured-where-viewers-watch"),
        ],
        "keywords": ["kick", "twitch", "simulcasting", "multistreaming", "live streaming", "viewership"],
        "files": [
            {
                "name": "summary.csv",
                "description": "Headline measures of the week, including the sensitivity checks.",
                "columns": [
                    ("measure", "string", "What is measured"),
                    ("value", "number", "The value"),
                    ("unit", "string", "count, hours or percent"),
                    ("note", "string", "How to read it"),
                ],
            },
            {
                "name": "kick_share_distribution.csv",
                "description": "Simulcasters grouped by the share of their combined viewers that watched on Kick.",
                "columns": [
                    ("kick_share_band", "string", "Share of the streamer's combined viewers on Kick"),
                    ("simulcasters", "integer", "Streamers in the band"),
                ],
            },
            {
                "name": "split_by_audience_size.csv",
                "description": "Kick's share of combined viewers by the simulcaster's average combined audience.",
                "columns": [
                    ("avg_combined_viewers_band", "string", "Average combined viewers while simulcasting"),
                    ("simulcasters", "integer", "Streamers in the band"),
                    ("kick_share_of_combined_viewers_pct", "number", "Kick's share of the band's combined viewers"),
                ],
            },
            {
                "name": "top_channels_simulcasting.csv",
                "description": "How many of each platform's most watched channels of the week simulcast on the other.",
                "columns": [
                    ("top_n", "integer", "The N most watched channels on the platform in the week"),
                    ("twitch_channels_simulcasting_on_kick", "integer", "Of Twitch's top N"),
                    ("kick_channels_simulcasting_on_twitch_min", "integer", "Of Kick's top N, a minimum (see limits)"),
                ],
            },
            {
                "name": "twitch_category_split.csv",
                "description": "Every Twitch category with 10 or more simulcasters, ranked by combined viewing during simulcasts.",
                "columns": [
                    ("rank_by_simulcast_viewing", "integer", "1 = the category with the most combined viewing during simulcasts"),
                    ("twitch_category", "string", "The simulcaster's main Twitch category"),
                    ("simulcasters", "integer", "Streamers whose main Twitch category this was"),
                    ("kick_share_of_combined_viewers_pct", "number", "Kick's share of those streamers' combined viewers"),
                ],
            },
            {
                "name": "kick_category_simulcast_share.csv",
                "description": "For Kick's largest categories, the share of Kick viewing that came from simulcasts.",
                "columns": [
                    ("rank_by_kick_viewing", "integer", "1 = the most watched Kick category of the week"),
                    ("kick_category", "string", "Kick category slug"),
                    ("simulcast_share_of_category_viewing_min_pct", "number", "Minimum share of the category's Kick viewing that came from simulcasting channels"),
                ],
            },
        ],
        "method": [
            "Both samplers read every 15 minutes: the Kick sampler walks Kick's whole public live directory "
            "(201,145 channels in the week), the Twitch sampler reads every category and records up to 30 "
            "streams per category, the most watched first (388,927 channels in the week).",
            "A simulcaster is a Kick channel and a Twitch channel with the same name (compared in lower case "
            "with hyphens and underscores removed) that were both live in the same 15-minute block for at "
            "least four blocks (one hour) in the week, in matching categories in at least half of those "
            "blocks. 11,782 names were live on both platforms at some point; 6,736 overlapped for an hour "
            "or more; 5,063 of those also matched on category.",
            "Audience split: for each simulcaster, viewer counts on each platform summed over the blocks in "
            "which both streams were read, and Kick's sum divided by the total. Platform totals are sums "
            "over all simulcasters; the median is taken per streamer.",
            "Robustness: repeating the split only in blocks where the Twitch category had fewer than 30 live "
            "streams (so every stream in it was read) gives Kick 16.6% of combined viewers against 16.7% "
            "overall.",
        ],
        "limits": [
            "One week. Simulcasting follows events, contracts and individual streamers.",
            "Matching is by name, time and category. A streamer who uses different names on the two "
            "platforms is missed; a third party rebroadcasting under the same name would be counted.",
            "A Twitch stream is visible only while it is in the top 30 of its category, so every Kick-side "
            "figure is a minimum and Twitch figures describe streams that reached that level.",
            "Channel names are not published here; the files hold totals only.",
        ],
    },
    # ------------------------------------------------------------------
    {
        "slug": "telegram-subscriber-change-2026-08-to-10",
        "title": "Telegram channel subscriber change by topic, August to October 2026",
        "kaggle_title": "Telegram Channel Subscriber Change 2026",
        "subtitle": "Share of 14,874 Telegram channels that lost subscribers, by topic and size",
        "summary": (
            "Which Telegram channels gained or lost subscribers between early August and early October "
            "2026, by topic and starting size. 85.6% of 814 crypto channels lost subscribers, against 64.6% "
            "of all 14,874 channels in the panel."
        ),
        "measured": "First reading 1 to 7 August 2026, last reading 26 September to 2 October 2026",
        "method_urls": [
            ("Crypto Telegram Channels Are Shrinking: 86% Lost Subscribers",
             SITE + "/learn/crypto-telegram-channels-are-losing-subscribers-measured"),
        ],
        "keywords": ["telegram", "channels", "subscribers", "crypto", "audience growth"],
        "files": [
            {
                "name": "subscriber_change_by_category.csv",
                "description": "Share of channels that lost or gained subscribers, and the median change, by topic.",
                "columns": [
                    ("category", "string", "Topic label from a keyword classifier, or Not classified, or All channels"),
                    ("channels", "integer", "Channels in the panel with that label"),
                    ("lost_subscribers_pct", "number", "Share of those channels whose last reading was lower than their first"),
                    ("gained_subscribers_pct", "number", "Share whose last reading was higher"),
                    ("median_change_pct", "number", "Median percentage change in subscribers between the two readings"),
                ],
            },
            {
                "name": "shrink_rate_by_size.csv",
                "description": "Share of channels that lost subscribers, by starting size and topic.",
                "columns": [
                    ("starting_size_band", "string", "Subscribers at the first reading"),
                    ("category", "string", "Topic label"),
                    ("channels", "integer", "Channels in the cell; empty when too few to publish"),
                    ("lost_subscribers_pct", "number", "Share that lost subscribers; empty when too few to publish"),
                ],
            },
        ],
        "method": [
            "PlayerSells' crawler stores a daily subscriber reading for the Telegram channels it tracks "
            "closely. For each channel the first reading between 1 and 7 August 2026 was compared with the "
            "last reading between 26 September and 2 October 2026, a median of 62 days later.",
            "Only broadcast channels with at least 1,000 subscribers at the first reading are included; "
            "groups are excluded. That leaves 14,874 channels.",
            "Topic labels come from a keyword classifier over each channel's name and description. 3,471 of "
            "the 14,874 channels carry a label; the rest are Not classified. Topics with fewer than 150 "
            "channels are not shown.",
            "Every central figure is a median.",
        ],
        "limits": [
            "The panel is made of large channels: only 27 of the 14,874 started below 10,000 subscribers and "
            "the median channel started with 121,871.",
            "The panel is not a random sample of Telegram. Private channels and channels nobody links to "
            "are missing.",
            "Topic labels are approximate and about three quarters of the panel has none.",
            "Nine weeks is short, and the data does not say why channels lost subscribers.",
        ],
    },
    # ------------------------------------------------------------------
    {
        "slug": "telegram-reach-benchmarks-2026-10",
        "title": "Telegram channel reach per post by size and niche, October 2026 edition",
        "kaggle_title": "Telegram Reach Benchmarks, October 2026",
        "subtitle": "Views per subscriber for 139,115 Telegram channels, by size and niche",
        "summary": (
            "How many views a Telegram channel's average post gets per subscriber, for every public "
            "broadcast channel with at least 1,000 subscribers whose page PlayerSells read in the 60 days "
            "to 3 October 2026. The typical channel with 1,000 to 5,000 subscribers reaches 27.5% of its "
            "subscribers per post; above 500,000 it is 3.1%."
        ),
        "measured": "3 October 2026 (pages read 4 August to 3 October 2026)",
        "method_urls": [
            ("What is a good Telegram engagement rate?", SITE + "/telegram-engagement-rate"),
        ],
        "keywords": ["telegram", "engagement rate", "reach", "benchmarks", "views per subscriber"],
        "files": [
            {
                "name": "reach_by_size.csv",
                "description": "Distribution of views per subscriber in each subscriber band, plus an all-channels row.",
                "columns": [
                    ("band", "string", "Subscriber band, or all"),
                    ("min_subscribers", "integer", "Lower bound of the band (inclusive)"),
                    ("max_subscribers", "integer", "Upper bound of the band (exclusive); empty for the top band"),
                    ("channels", "integer", "Channels measured in the band"),
                    ("p10_reach_pct", "number", "10th percentile of average views per post divided by subscribers, in percent"),
                    ("p25_reach_pct", "number", "25th percentile"),
                    ("median_reach_pct", "number", "Median"),
                    ("p75_reach_pct", "number", "75th percentile"),
                    ("p90_reach_pct", "number", "90th percentile"),
                    ("median_views_per_post", "integer", "Median average views per post"),
                ],
            },
            {
                "name": "reach_by_niche.csv",
                "description": "Median views per subscriber by niche, channels with 5,000 to 100,000 subscribers.",
                "columns": [
                    ("niche", "string", "Topic label from a keyword classifier"),
                    ("channels", "integer", "Channels measured"),
                    ("median_reach_pct", "number", "Median average views per post divided by subscribers, in percent"),
                ],
            },
        ],
        "method": [
            "For every public channel it tracks, PlayerSells reads the subscriber count and the view counts "
            "of the most recent posts from the channel's public t.me preview. Reach per post is the average "
            "view count divided by the subscriber count.",
            "The table counts every qualifying channel with no sampling: broadcast channels with at least "
            "1,000 subscribers, a view count above zero and a public page read between 4 August and "
            "3 October 2026. 139,115 channels, measured on 3 October 2026 at 14:29 UTC.",
            "Across all of them the median is 14.5%, and 10.1% of channels average more views per post than "
            "they have subscribers.",
            "The niche table holds channels with 5,000 to 100,000 subscribers that the classifier assigned a "
            "niche, in niches with at least 200 such channels.",
        ],
        "limits": [
            "Private and invite-only channels, and groups, cannot be measured this way.",
            "Average views include posts that are still collecting views, so channels that post many times a "
            "day can read lower than their settled reach.",
            "Views per subscriber above 100% come from forwards, cross-posts or paid promotion.",
            "This is a dated edition, re-measured once a quarter.",
        ],
    },
    # ------------------------------------------------------------------
    {
        "slug": "x-reach-per-follower-premium-2026",
        "title": "X (Twitter) views per follower by account size and Premium badge, 2026",
        "kaggle_title": "X Views per Follower and Premium Badge 2026",
        "subtitle": "Post views per follower for 60,892 X accounts, Premium vs no badge",
        "summary": (
            "How many views an X account's typical post gets relative to its follower count, by account "
            "size, and how accounts with the blue Premium badge compare with no-badge accounts of the same "
            "size. Premium accounts drew 1.6x to 1.8x the views per follower between 5,000 and 1 million "
            "followers. This is a correlation, not proof that Premium causes it."
        ),
        "measured": "Engagement records computed 19 August to 3 October 2026, each covering 30 days of posts",
        "method_urls": [
            ("X Premium Linked to 1.6x-1.8x More Reach at the Same Size",
             SITE + "/learn/does-x-premium-increase-reach-60000-accounts-compared"),
        ],
        "keywords": ["twitter", "x", "premium", "reach", "views", "engagement", "verification"],
        "files": [
            {
                "name": "reach_by_follower_band.csv",
                "description": "Median post views and engagement as a share of followers, by follower band.",
                "columns": [
                    ("follower_band", "string", "Follower band"),
                    ("accounts", "integer", "Accounts in the band"),
                    ("median_followers", "integer", "Median follower count inside the band"),
                    ("median_views_per_post", "integer", "Median of the accounts' median original-post views"),
                    ("views_per_follower_pct", "number", "Median views as a share of followers"),
                    ("views_per_follower_p25_pct", "number", "25th percentile"),
                    ("views_per_follower_p75_pct", "number", "75th percentile"),
                    ("engagement_per_follower_pct", "number", "Median likes, replies, reposts and quotes on the median post, as a share of followers"),
                ],
            },
            {
                "name": "premium_vs_no_badge.csv",
                "description": "Views per follower for Premium and no-badge accounts of the same size.",
                "columns": [
                    ("follower_band", "string", "Follower band"),
                    ("band_note", "string", "Median follower counts of the two groups, as published"),
                    ("premium_accounts", "integer", "Accounts with the blue badge and no organisation badge"),
                    ("no_badge_accounts", "integer", "Accounts with no badge"),
                    ("premium_views_per_follower_pct", "number", "Median for Premium accounts"),
                    ("no_badge_views_per_follower_pct", "number", "Median for no-badge accounts"),
                    ("ratio", "number", "Premium divided by no badge; empty where there are too few accounts to compare"),
                ],
            },
            {
                "name": "premium_by_posting_rate.csv",
                "description": "The Premium comparison split by how often accounts post.",
                "columns": [
                    ("follower_band", "string", "Follower band"),
                    ("posts_per_day", "string", "Posting-rate group"),
                    ("premium_accounts", "integer", "Premium accounts in the group"),
                    ("no_badge_accounts", "integer", "No-badge accounts in the group"),
                    ("premium_views_per_follower_pct", "number", "Median for Premium accounts"),
                    ("no_badge_views_per_follower_pct", "number", "Median for no-badge accounts"),
                ],
            },
        ],
        "method": [
            "PlayerSells' X engine reads the recent public posts of accounts in its index and keeps one "
            "engagement record per account, covering the 30 days before it was computed. Records computed "
            "between 19 August and 3 October 2026 are used.",
            "Accounts with at least 10 original posts in the window and at most 10% retweets are kept: "
            "60,892 accounts. Reach is the median view count of the account's original posts divided by its "
            "follower count when the record was computed.",
            "Premium means the blue badge and no organisation badge. 6,955 accounts with gold or grey "
            "organisation badges are left out of the comparison, leaving 53,937. The badge is read at the "
            "most recent crawl, a median of 7.2 days after the engagement record.",
            "Every figure is a median.",
        ],
        "limits": [
            "Correlation only. People who pay for Premium may differ in ways the data cannot see.",
            "Not a random sample of X: the engine reads accounts in size tiers, largest first, so each band "
            "is dense near its top. Use the median follower count of each band.",
            "Views are X's own impression counter and include people who do not follow the account.",
            "Badge status is current, not historical, and Premium and Premium+ cannot be told apart.",
        ],
    },
    # ------------------------------------------------------------------
    {
        "slug": "x-engagement-benchmarks-2026-10",
        "title": "X (Twitter) engagement rate benchmarks and posting pattern effects, October 2026",
        "kaggle_title": "X Engagement Rate Benchmarks, October 2026",
        "subtitle": "Engagement rate by follower band, plus timing, media and link effects",
        "summary": (
            "Engagement rate percentiles for 152,291 measured X accounts, broken down by follower band, and "
            "45 posting pattern effects (hour, weekday, length, hashtags, links, media) measured within "
            "accounts with 95% intervals."
        ),
        "measured": "Trailing 30-day windows ending 6 and 7 October 2026 (see the files)",
        "method_urls": [
            ("What Is a Good Engagement Rate on X?", SITE + "/insights/engagement-rate-benchmarks"),
            ("X Engagement Insights", SITE + "/insights"),
            ("Machine-readable findings (JSON)", SITE + "/insights/data.json"),
        ],
        "keywords": ["twitter", "x", "engagement rate", "benchmarks", "best time to post", "hashtags"],
        "files": [
            {
                "name": "engagement_rate_percentiles.csv",
                "description": "Engagement rate percentiles across all measured accounts.",
                "columns": [
                    ("statistic", "string", "p10, p25, p50, p75, p90 or mean"),
                    ("engagement_rate_pct", "number", "Median interactions per original post divided by followers, in percent"),
                    ("accounts", "integer", "Accounts in the measured population"),
                    ("window_end", "date", "Last day of the 30-day window"),
                ],
            },
            {
                "name": "engagement_rate_by_follower_band.csv",
                "description": "Engagement rate quartiles by follower band. Bands with fewer than 30 accounts are not shown.",
                "columns": [
                    ("follower_band", "string", "Follower band"),
                    ("accounts", "integer", "Accounts in the band"),
                    ("p25_engagement_rate_pct", "number", "Lower quartile"),
                    ("median_engagement_rate_pct", "number", "Median"),
                    ("p75_engagement_rate_pct", "number", "Upper quartile"),
                    ("window_end", "date", "Last day of the 30-day window"),
                ],
            },
            {
                "name": "posting_pattern_effects.csv",
                "description": "Within-account effect of a posting choice on engagement, with a distribution-free 95% interval.",
                "columns": [
                    ("dimension", "string", "hour_utc, dow, length_bucket, hashtag_count, link, media or video"),
                    ("bucket", "string", "The value of the dimension"),
                    ("label", "string", "Readable label"),
                    ("effect_pct", "number", "Median per-account change in engagement on posts in the bucket against the same accounts' other posts"),
                    ("effect_lo_pct", "number", "Lower end of the 95% interval"),
                    ("effect_hi_pct", "number", "Upper end of the 95% interval"),
                    ("significant", "boolean", "true when the effect survives a Benjamini-Hochberg multiple-testing correction across all findings and at least 30 accounts contribute. A raw 95% interval that excludes zero is not enough on its own"),
                    ("accounts", "integer", "Accounts contributing"),
                    ("accounts_agreeing", "integer", "Accounts whose own effect points the same way as the median"),
                    ("posts", "integer", "Posts in the bucket"),
                    ("median_multiple", "number", "Median of the per-account engagement multiples"),
                    ("p90_multiple", "number", "90th percentile of the per-account multiples"),
                    ("window_end", "date", "Last day of the 30-day window"),
                ],
            },
        ],
        "method": [
            "Engagement rate is the median number of interactions (likes, reposts, replies and quotes) on an "
            "account's original posts over a 30-day window, divided by the account's follower count. "
            "Replies and reposts by the account are excluded.",
            "Percentiles are computed in the database over every account with at least 8 original posts in "
            "the window, with linear interpolation. The measured population held 152,291 accounts, from 985 "
            "to 242M followers with a median of 78K.",
            "Posting pattern effects compare, within each account, the median engagement of posts in a "
            "bucket with the same account's other posts, giving one ratio per account. The effect is the "
            "median of those ratios with a distribution-free 95% interval, so account size cancels out and "
            "the unit of evidence is the account, not the post. A finding is marked significant only after "
            "a Benjamini-Hochberg correction for testing many buckets at once, so a few rows have a raw "
            "interval that excludes zero and are still reported as no measurable difference.",
            "These figures are recomputed daily on playersells.com. This file is a snapshot; build.py "
            "--refresh takes a new one.",
        ],
        "limits": [
            "The accounts are the ones the catalog has scanned deeply enough to produce a stable median. The "
            "catalog is scanned largest first, so this is not a random sample of X.",
            "Pooled percentiles mix very different account sizes. Compare an account with its own band.",
            "Effects are observational associations, not causal estimates.",
            "Interaction counts are read at collection time, not live.",
        ],
    },
    # ------------------------------------------------------------------
    {
        "slug": "x-link-post-reach-2026-10",
        "title": "Views on X (Twitter) posts with a link against the same account's posts without one, 2026",
        "kaggle_title": "X Link Posts vs Link-Free Posts, Views 2026",
        "subtitle": "Within-account view gap for link posts on X, by size, topic and link placement",
        "summary": (
            "How many views X (Twitter) posts with a link drew compared with the same account's posts without "
            "a link, measured on 6,447,046 original posts from 285,579 accounts published between 15 July and "
            "7 October 2026. For the median account, text posts with a link drew 10.4% fewer views; for "
            "accounts with over 1 million followers, 30.4% fewer; for accounts under 1,000 followers, 16.6% more."
        ),
        "measured": "Original posts published 15 July to 7 October 2026, views read at least 48 hours after posting",
        "method_urls": [
            ("Does X Still Penalize Links? 6.4 Million Posts Measured",
             SITE + "/learn/does-x-still-penalize-links-we-measured-6-million-posts"),
        ],
        "keywords": ["twitter", "x", "links", "reach", "views", "algorithm", "engagement", "social media"],
        "files": [
            {
                "name": "link_gap_overall.csv",
                "description": "The within-account view gap for link posts, text-only posts and posts with an image or video.",
                "columns": [
                    ("post_type", "string", "Text only, or with image or video"),
                    ("accounts", "integer", "Accounts with at least three link posts and three link-free posts of this type"),
                    ("views_change_pct", "number", "Median across accounts of (median views of link posts / median views of link-free posts) minus 1, in percent"),
                    ("accounts_with_fewer_views_pct", "number", "Share of those accounts whose link posts got fewer views"),
                ],
            },
            {
                "name": "link_gap_by_follower_band.csv",
                "description": "The same gap by the account's follower count.",
                "columns": [
                    ("follower_band", "string", "Follower band, from the median follower count recorded when the account's posts were read"),
                    ("text_accounts", "integer", "Accounts in the text-only comparison"),
                    ("text_views_change_pct", "number", "Median view change on text posts with a link"),
                    ("media_accounts", "integer", "Accounts in the image or video comparison"),
                    ("media_views_change_pct", "number", "Median view change on image or video posts with a link"),
                ],
            },
            {
                "name": "link_gap_by_category.csv",
                "description": "The same gap by account topic, for topics with at least 100 accounts in the text comparison.",
                "columns": [
                    ("account_category", "string", "Topic from the PlayerSells account classifier, or none assigned"),
                    ("text_accounts", "integer", "Accounts in the text-only comparison"),
                    ("text_views_change_pct", "number", "Median view change on text posts with a link"),
                    ("media_accounts", "integer", "Accounts in the image or video comparison"),
                    ("media_views_change_pct", "number", "Median view change on image or video posts with a link"),
                ],
            },
            {
                "name": "link_gap_by_period.csv",
                "description": "The same gap in three periods of 2026: before Elon Musk's late July statement that X had not penalized links for over a year, after it, and after X's 8 September creator payout change.",
                "columns": [
                    ("period_2026", "string", "Publication dates of the posts"),
                    ("text_accounts", "integer", "Accounts in the text-only comparison inside the period"),
                    ("text_views_change_pct", "number", "Median view change on text posts with a link"),
                    ("media_accounts", "integer", "Accounts in the image or video comparison inside the period"),
                    ("media_views_change_pct", "number", "Median view change on image or video posts with a link"),
                ],
            },
            {
                "name": "engagement_per_view_change.csv",
                "description": "Change in likes, replies, reposts and bookmarks per view on link posts against the same account's link-free posts.",
                "columns": [
                    ("measure", "string", "Engagement measure per view"),
                    ("text_change_pct", "number", "Median change for text posts with a link, from each group's totals"),
                    ("media_change_pct", "number", "Median change for image or video posts with a link"),
                ],
            },
            {
                "name": "link_placement.csv",
                "description": "Views on posts with the link in the post and posts with the link only in the author's own reply, against the same account's posts with no link.",
                "columns": [
                    ("link_location", "string", "In the post, or in the author's own reply"),
                    ("post_type", "string", "Text only, or with image or video"),
                    ("accounts", "integer", "Accounts with at least three link-in-reply posts and three posts in the group"),
                    ("views_change_vs_no_link_pct", "number", "Median view change against the same account's posts with no link"),
                ],
            },
        ],
        "method": [
            "PlayerSells' X crawler reads public posts of the accounts in its directory. Every original post "
            "it had read that was published between 15 July and 7 October 2026 is used: 6,447,046 posts from "
            "285,579 accounts. Reposts, quote posts, replies and thread continuations are excluded. Only posts "
            "whose view counter was read at least 48 hours after publication are kept.",
            "A link post is one for which X reports at least one URL. Uploaded photos and videos are not links. "
            "Posts are split into text only and posts with an image or video.",
            "For each account with at least three link posts and three link-free posts of the same type, the "
            "median views of its link posts are divided by the median views of its link-free posts. Tables "
            "report the median of those ratios across accounts, as a percent change. 68,604 accounts had at "
            "least three posts with a link and three without.",
            "A link-in-reply post is an original post without a link whose author replied to it with a post "
            "that carries a link.",
        ],
        "limits": [
            "Observational: comparing an account with itself removes differences between accounts, not "
            "differences between the posts an account chooses to link.",
            "The figures describe outcomes. They cannot show whether X applies a rule to links.",
            "The crawler reads the largest accounts first, so small accounts are fewer in the sample.",
            "Views are X's own impression counter, taken as published.",
            "No post data from before July 2026 is included.",
        ],
    },
]
