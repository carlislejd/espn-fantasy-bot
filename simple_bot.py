#!/usr/bin/env python3
"""
Simplified ESPN Fantasy Telegram Bot
"""

import os
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# ESPN API imports
try:
    from espn_api.football import League as FootballLeague
    ESPN_AVAILABLE = True
except ImportError:
    ESPN_AVAILABLE = False
    print("Warning: ESPN API not available")

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SimpleESPNBot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.league_id = int(os.getenv('ESPN_LEAGUE_ID', 0))
        self.year = int(os.getenv('ESPN_YEAR', 2024))
        self.espn_s2 = os.getenv('ESPN_S2')
        self.swid = os.getenv('ESPN_SWID')
        
        self.league = None
        
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set")
        if not self.chat_id:
            raise ValueError("TELEGRAM_CHAT_ID not set")
        if not self.league_id:
            raise ValueError("ESPN_LEAGUE_ID not set")
    
    def initialize_league(self):
        """Initialize the ESPN league connection"""
        if not ESPN_AVAILABLE:
            logger.error("ESPN API not available")
            return False
            
        try:
            if self.espn_s2 and self.swid:
                self.league = FootballLeague(
                    league_id=self.league_id,
                    year=self.year,
                    espn_s2=self.espn_s2,
                    swid=self.swid
                )
            else:
                self.league = FootballLeague(
                    league_id=self.league_id,
                    year=self.year
                )
                
            logger.info(f"Successfully connected to league: {self.league.settings.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize league: {e}")
            return False
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🏈 *ESPN Fantasy League Bot* 🏈

Welcome! This bot provides updates for your ESPN fantasy league.

*Available Commands:*
• `/scores` - Get current week scores
• `/standings` - Show league standings
• `/teams` - List all teams
• `/help` - Show this help message

Use `/help` for more information!
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Scores", callback_data="scores")],
            [InlineKeyboardButton("🏆 Standings", callback_data="standings")],
            [InlineKeyboardButton("👥 Teams", callback_data="teams")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
*ESPN Fantasy Bot Help*

*Commands:*
• `/start` - Start the bot and show main menu
• `/scores` - Get current week scores
• `/standings` - Show league standings
• `/teams` - List all teams with records
• `/help` - Show this help message

*League Info:*
• League: T-Town and Beyond
• Sport: Football
• Year: 2025
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def scores_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /scores command"""
        if not self.league:
            await update.message.reply_text("❌ League not initialized. Check your configuration.")
            return
        
        try:
            scores_text = self.get_current_scores()
            await update.message.reply_text(scores_text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Error getting scores: {e}")
            await update.message.reply_text("❌ Error retrieving scores. Please try again later.")
    
    async def standings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /standings command"""
        if not self.league:
            await update.message.reply_text("❌ League not initialized. Check your configuration.")
            return
        
        try:
            standings_text = self.get_standings()
            await update.message.reply_text(standings_text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Error getting standings: {e}")
            await update.message.reply_text("❌ Error retrieving standings. Please try again later.")
    
    async def teams_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /teams command"""
        if not self.league:
            await update.message.reply_text("❌ League not initialized. Check your configuration.")
            return
        
        try:
            teams_text = self.get_teams_info()
            await update.message.reply_text(teams_text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Error getting teams: {e}")
            await update.message.reply_text("❌ Error retrieving teams. Please try again later.")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "scores":
            await self.scores_command(update, context)
        elif query.data == "standings":
            await self.standings_command(update, context)
        elif query.data == "teams":
            await self.teams_command(update, context)
    
    def get_current_scores(self) -> str:
        """Get current week scores"""
        if not self.league:
            return "❌ League not initialized"
        
        try:
            current_week = self.league.current_week
            scores_text = f"🏈 *Week {current_week} Scores*\n\n"
            
            for matchup in self.league.scoreboard():
                team1 = matchup.home_team
                team2 = matchup.away_team
                
                # Format scores
                team1_score = f"{team1.score:.1f}" if team1.score else "0.0"
                team2_score = f"{team2.score:.1f}" if team2.score else "0.0"
                
                scores_text += f"*{team1.team_name}* {team1_score} vs {team2_score} *{team2.team_name}*\n"
                
                # Add matchup status
                if matchup.status == "FINAL":
                    scores_text += "✅ *Final*\n"
                elif matchup.status == "IN_PROGRESS":
                    scores_text += "🔄 *Live*\n"
                else:
                    scores_text += "⏰ *Scheduled*\n"
                
                scores_text += "\n"
            
            return scores_text
            
        except Exception as e:
            logger.error(f"Error getting scores: {e}")
            return "❌ Error retrieving scores"
    
    def get_standings(self) -> str:
        """Get league standings"""
        if not self.league:
            return "❌ League not initialized"
        
        try:
            standings_text = f"🏆 *League Standings*\n\n"
            
            for i, team in enumerate(self.league.standings(), 1):
                record = f"{team.wins}-{team.losses}"
                if hasattr(team, 'ties') and team.ties > 0:
                    record += f"-{team.ties}"
                
                standings_text += f"{i}. *{team.team_name}* ({record})\n"
                standings_text += f"   Points: {team.points_for:.1f} | Against: {team.points_against:.1f}\n\n"
            
            return standings_text
            
        except Exception as e:
            logger.error(f"Error getting standings: {e}")
            return "❌ Error retrieving standings"
    
    def get_teams_info(self) -> str:
        """Get detailed team information"""
        if not self.league:
            return "❌ League not initialized"
        
        try:
            teams_text = f"👥 *League Teams*\n\n"
            
            for team in self.league.teams:
                record = f"{team.wins}-{team.losses}"
                if hasattr(team, 'ties') and team.ties > 0:
                    record += f"-{team.ties}"
                
                teams_text += f"*{team.team_name}*\n"
                teams_text += f"Owner: {team.owner}\n"
                teams_text += f"Record: {record}\n"
                teams_text += f"Points: {team.points_for:.1f}\n\n"
            
            return teams_text
            
        except Exception as e:
            logger.error(f"Error getting teams: {e}")
            return "❌ Error retrieving teams"
    
    async def run_bot(self):
        """Run the Telegram bot"""
        # Initialize league connection
        if not self.initialize_league():
            logger.error("Failed to initialize league. Check your configuration.")
            return
        
        # Create application
        application = Application.builder().token(self.bot_token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("scores", self.scores_command))
        application.add_handler(CommandHandler("standings", self.standings_command))
        application.add_handler(CommandHandler("teams", self.teams_command))
        
        # Add callback query handler
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Start the bot
        logger.info("Starting Simple ESPN Fantasy Bot...")
        await application.run_polling(allowed_updates=Update.ALL_TYPES)

async def main():
    """Main function"""
    try:
        bot = SimpleESPNBot()
        await bot.run_bot()
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")

if __name__ == "__main__":
    asyncio.run(main())
