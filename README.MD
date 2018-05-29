# Prerequisites

**The following environment variables must be defined:**

```
FACEBOOK_APP_ID            The app ID of your Facebook app
FACEBOOK_PAGE_ACCESS_TOKEN The access token of the page you're posting to. Needs manage_page/publish_page permission.
FACEBOOK_PAGE_ID           The ID of the page you're posting to. Normally the number at the end of the URL if you're not using custom.
TWITTER_CONSUMER_KEY       Available from apps.twitter.com under your app's tokens, etc.
TWITTER_CONSUMER_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_SECRET
DISCORD_APP_USER_TOKEN     Create a Discord app and a bot user for it. The bot user's token should be stored in this variable.
```

Running `main.py` will post across all three services with the data defined in `post`. The fields for this are used in Jekyll posts to [SLUGSoc/website](https://github.com/SLUGSoc/website), but you can and should define your own, along with text formats under `format_post`.
