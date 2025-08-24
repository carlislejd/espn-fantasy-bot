# Quick Start Guide

Get your ESPN Fantasy Telegram Bot running in 5 minutes!

## Prerequisites

- Python 3.8+
- Poetry (install with: `curl -sSL https://install.python-poetry.org | python3 -`)
- ESPN Fantasy League
- Telegram Bot Token

## 1. Install Dependencies

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

## 2. Get Your Telegram Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot`
3. Follow the instructions to create your bot
4. Copy the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## 3. Get Your Chat ID

1. Start a conversation with your bot
2. Send any message to it
3. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find the `chat_id` in the response (it's a number like `123456789`)

## 4. Find Your ESPN League ID

1. Go to your ESPN fantasy league
2. Look at the URL: `https://fantasy.espn.com/football/league?leagueId=123456`
3. The number after `leagueId=` is your league ID

## 5. Configure the Bot

```bash
# Set up environment file
poetry run python cli.py setup

# Edit the .env file with your details
nano .env
```

Your `.env` file should look like this:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
ESPN_LEAGUE_ID=123456
ESPN_YEAR=2024
ESPN_SPORT=football
```

## 6. Test the Connection

```bash
# Test ESPN connection
poetry run python cli.py test
```

## 7. Run the Bot

```bash
# Start the bot
poetry run espn-bot
```

## 8. Use Your Bot

1. Send `/start` to your bot on Telegram
2. Use the interactive buttons or commands:
   - `/scores` - Get current scores
   - `/standings` - View standings
   - `/teams` - List teams
   - `/help` - Show help

## Troubleshooting

**Bot not responding?**
- Check your bot token is correct
- Make sure you've started a conversation with the bot
- Verify the chat ID is correct

**ESPN connection failed?**
- Check your league ID is correct
- Make sure your league is public or provide ESPN credentials
- Verify the league year is correct

**Need help?**
- Run `poetry run python cli.py status` to check configuration
- Check the full [README.md](README.md) for detailed documentation

## Next Steps

- Customize update frequency in `.env`
- Add ESPN credentials for private leagues
- Set up automatic deployment
- Join our community for support!

---

🎉 **You're all set!** Your bot will now automatically post updates about scores, standings, and more to your Telegram chat.
