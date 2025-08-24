# ESPN Fantasy League Telegram Bot

A Telegram bot that provides real-time updates for your ESPN fantasy league, including scores, standings, waiver activity, and player news.

## Features

- 🏈 **Real-time Score Updates** - Get live score updates during games
- 🏆 **League Standings** - View current standings and team records
- 👥 **Team Information** - Detailed team and owner information
- 📝 **Waiver Activity** - Track waiver wire pickups and drops
- 📰 **Player News** - Latest player news and injury updates
- ⚙️ **Configurable Updates** - Customize update frequency and types
- 🎯 **Interactive Commands** - Easy-to-use bot commands and buttons

## Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)
- ESPN Fantasy League account
- Telegram Bot Token

## Installation

### Local Development

#### 1. Clone the repository

```bash
git clone <your-repo-url>
cd espn-fantasy-telegram-bot
```

#### 2. Install Poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### 3. Install dependencies

```bash
poetry install
```

#### 4. Set up environment variables

Copy the example configuration file:

```bash
cp config.example.env .env
```

Edit the `.env` file with your configuration:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# ESPN Fantasy League Configuration
ESPN_LEAGUE_ID=your_league_id_here
ESPN_YEAR=2025
ESPN_SPORT=football

# Optional: ESPN Login (for private leagues)
# To find these values, log into ESPN fantasy on Chrome, then:
# 1. Right-click and "Inspect"
# 2. Go to Application tab
# 3. Under Storage > Cookies > http://fantasy.espn.com
# 4. Find the values for 'swid' and 'espn_s2'
ESPN_S2=your_espn_s2_cookie_value
ESPN_SWID=your_swid_cookie_value

# Bot Configuration
UPDATE_INTERVAL=300  # seconds between updates
ENABLE_SCORE_UPDATES=true
ENABLE_WAIVER_UPDATES=true
ENABLE_NEWS_UPDATES=true
```

### Deployment

#### Render (Recommended)

1. **Fork this repository** to your GitHub account
2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Click "New" → "Background Service"
   - Connect your GitHub repository
3. **Configure the service**:
   - **Name**: `espn-fantasy-bot`
   - **Environment**: `Python`
   - **Build Command**: `pip install poetry && poetry install`
   - **Start Command**: `poetry run python simple_bot.py`
4. **Add Environment Variables**:
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `TELEGRAM_CHAT_ID`: Your chat ID
   - `ESPN_LEAGUE_ID`: Your league ID
   - `ESPN_S2`: Your ESPN S2 cookie (optional)
   - `ESPN_SWID`: Your ESPN SWID cookie (optional)
5. **Deploy** and your bot will run 24/7!

#### Alternative: Heroku

1. **Install Heroku CLI**
2. **Deploy**:
   ```bash
   heroku create your-bot-name
   heroku config:set TELEGRAM_BOT_TOKEN=your_token
   heroku config:set TELEGRAM_CHAT_ID=your_chat_id
   heroku config:set ESPN_LEAGUE_ID=your_league_id
   git push heroku main
   ```

## Configuration

### Getting Your Telegram Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Copy the token provided

### Getting Your Chat ID

1. Add your bot to a group or start a conversation
2. Send a message to the bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for the `chat_id` in the response

### Finding Your ESPN League ID

1. Go to your ESPN fantasy league
2. Look at the URL: `https://fantasy.espn.com/football/league?leagueId=123456`
3. The number after `leagueId=` is your league ID

## Usage

### Running the Bot

```bash
# Using Poetry
poetry run espn-bot

# Or using Python module
poetry run python -m espn_fantasy_bot
```

### Bot Commands

- `/start` - Start the bot and show main menu
- `/scores` - Get current week scores
- `/standings` - Show league standings
- `/teams` - List all teams with records
- `/waivers` - Show recent waiver activity
- `/help` - Show help information

### Automatic Updates

The bot automatically checks for updates every 5 minutes (configurable) and posts:

- Score changes during live games
- Waiver wire activity
- Player news and injury updates

## Development

### Project Structure

```
espn-fantasy-telegram-bot/
├── espn_fantasy_bot/
│   ├── __init__.py
│   ├── __main__.py
│   └── bot.py
├── tests/
├── pyproject.toml
├── README.md
└── config.example.env
```

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black .
poetry run flake8 .
poetry run mypy .
```

### Adding New Features

1. Create a new branch for your feature
2. Add tests for new functionality
3. Update documentation
4. Submit a pull request

## Supported Sports

Currently supports:
- 🏈 **Fantasy Football** (NFL)
- 🏀 **Fantasy Basketball** (NBA)

Coming soon:
- 🏒 **Fantasy Hockey** (NHL)
- ⚾ **Fantasy Baseball** (MLB)

## Troubleshooting

### Common Issues

**League not initialized error:**
- Check your ESPN league ID is correct
- Ensure your league is public or provide ESPN credentials
- Verify the league year is correct

**Telegram bot not responding:**
- Verify your bot token is correct
- Check that the bot has been added to the chat
- Ensure the chat ID is correct

**No updates being posted:**
- Check that automatic updates are enabled in your config
- Verify the update interval is reasonable
- Check the bot logs for errors

### Debug Mode

Enable debug mode by setting the environment variable:

```env
DEBUG=true
```

This will provide more detailed logging information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [ESPN API](https://github.com/cwendt94/espn-api) - For providing the ESPN fantasy API
- [python-telegram-bot](https://python-telegram-bot.org/) - For the Telegram bot framework

## Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#troubleshooting)
2. Search existing [issues](../../issues)
3. Create a new issue with detailed information

---

**Note:** This bot is not affiliated with ESPN or Telegram. Use at your own risk and in accordance with ESPN's terms of service.
