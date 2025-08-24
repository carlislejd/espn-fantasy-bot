# ESPN Fantasy League Telegram Bot

A Telegram bot that provides real-time updates and information for your ESPN fantasy football league.

## Features

- **Live Scores**: Get current week scores and matchup status
- **Standings**: View league standings and team records
- **Team Information**: Detailed team stats and roster information
- **Player Rankings**: Top performing players across the league
- **Recent Activity**: Transaction history, waiver moves, and FAAB bids
- **Personalized Commands**: Register your team for personalized updates
- **Matchup Details**: Get specific matchup information
- **Prize Structure**: View league payout information

## Commands

- `/start` - Welcome message and command list
- `/scores` - Get current week scores
- `/standings` - Show league standings
- `/teams` - List all teams with IDs
- `/starters` - Show all team starters for current week
- `/rank` - Show top performing players this week
- `/matchup Team Name` - Get specific matchup details
- `/myteam` - Show your team info (requires registration)
- `/register Team Name` - Register your team for personalized commands
- `/activity` - Show recent transactions & moves
- `/payout` - Show payout structure
- `/help` - Show help information

## Setup

### Prerequisites

- Python 3.8+
- ESPN Fantasy League access
- Telegram Bot Token

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ttown_espn_tg
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
ESPN_LEAGUE_ID=your_league_id_here
ESPN_YEAR=2025
ESPN_SPORT=football
ESPN_S2=your_espn_s2_cookie_here
ESPN_SWID=your_espn_swid_cookie_here
```

### Running Locally

```bash
python minimal_bot.py
```

## Deployment on Render

1. Push your code to GitHub
2. Create a new Background Service on Render
3. Connect your GitHub repository
4. Set the following environment variables in Render:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `ESPN_LEAGUE_ID`
   - `ESPN_YEAR` (2025)
   - `ESPN_SPORT` (football)
   - `ESPN_S2`
   - `ESPN_SWID`
5. Set the build command: `pip install -r requirements.txt`
6. Set the start command: `python start.py`

## ESPN Authentication

For private leagues, you'll need your ESPN cookies:
1. Log into ESPN Fantasy Football
2. Open browser developer tools (F12)
3. Go to Application/Storage → Cookies → fantasy.espn.com
4. Find and copy the values for `swid` and `espn_s2`

## Team Registration

Users can register their teams using `/register Team Name`. Once registered, they can use `/myteam` to get personalized team information.

## License

MIT License
