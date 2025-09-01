#!/usr/bin/env python3
"""
Minimal ESPN Fantasy Telegram Bot
"""

import os
import logging
import requests
import time
from dotenv import load_dotenv

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

class MinimalESPNBot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.league_id = int(os.getenv('ESPN_LEAGUE_ID', 0))
        self.year = int(os.getenv('ESPN_YEAR', 2024))
        self.espn_s2 = os.getenv('ESPN_S2')
        self.swid = os.getenv('ESPN_SWID')
        
        # Team mappings - map Telegram usernames/phone numbers to team IDs
        self.team_mappings = {
            '@jcarlisle': 4,  # The Commish
            '+17707145874': 4,  # The Commish
            '+16363575742': 3,
            '+19087972342': 5,
            '+14806486544': 2,
            '+16503023377': 7,
        }
        
        self.league = None
        self.last_update_id = 0
        
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
    
    def send_message(self, text):
        """Send a message to Telegram"""
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return None
    
    def get_updates(self):
        """Get updates from Telegram"""
        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
        params = {
            'offset': self.last_update_id + 1,
            'timeout': 30
        }
        
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return None
    
    def handle_command(self, message):
        """Handle incoming commands"""
        text = message.get('text', '')
        chat_id = message.get('chat', {}).get('id')
        
        if not text.startswith('/'):
            return
        
        command = text.lower().split()[0]
        
        if command == '/start':
            welcome_text = """
🏈 *ESPN Fantasy League Bot* 🏈

Welcome! This bot provides updates for your ESPN fantasy league.

*Available Commands:*
• `/scores` - Get current week scores
• `/standings` - Show league standings
• `/teams` - List all teams
• `/starters` - Show all team starters
• `/rank` - Top performing players
• `/matchup` - Show your matchup (requires registration)
• `/matchup Team Name` - Specific matchup details
• `/myteam` - Show your team info
• `/register Team Name` - Register your team
• `/draft` - Draft countdown timer
• `/cap` - Salary cap information
• `/activity` - Show recent transactions
• `/payout` - Show payout structure
• `/help` - Show this help message

Use `/help` for more information!
            """
            self.send_message(welcome_text)
            
        elif command == '/help':
            help_text = """
*ESPN Fantasy Bot Help*

*Commands:*
• `/start` - Start the bot and show main menu
• `/scores` - Get current week scores
• `/standings` - Show league standings
• `/teams` - List all teams with records
• `/starters` - Show all team starters for current week
• `/rank` - Show top performing players this week
• `/matchup` - Show your matchup (requires registration)
• `/matchup Team Name` - Get specific matchup details
• `/myteam` - Show your team info (requires registration)
• `/register Team Name` - Register your team for personalized commands
• `/draft` - Show draft countdown timer
• `/cap` - Show salary cap information
• `/activity` - Show recent transactions & moves
• `/payout` - Show payout structure
• `/help` - Show this help message

*League Info:*
• League: T-Town and Beyond
• Sport: Football
• Year: 2025
            """
            self.send_message(help_text)
            
        elif command == '/scores':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                scores_text = self.get_current_scores()
                self.send_message(scores_text)
            except Exception as e:
                logger.error(f"Error getting scores: {e}")
                self.send_message("❌ Error retrieving scores. Please try again later.")
                
        elif command == '/standings':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                standings_text = self.get_standings()
                self.send_message(standings_text)
            except Exception as e:
                logger.error(f"Error getting standings: {e}")
                self.send_message("❌ Error retrieving standings. Please try again later.")
                
        elif command == '/teams':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                teams_text = self.get_teams_info()
                self.send_message(teams_text)
            except Exception as e:
                logger.error(f"Error getting teams: {e}")
                self.send_message("❌ Error retrieving teams. Please try again later.")
                
        elif command == '/payout':
            payout_text = """
💰 *League Payout Structure* 💰

**Champion: $515**
🏆 1st Place takes home the big prize!

**2nd Place: $230**
🥈 Runner-up gets a nice payout

**3rd Place: $120**
🥉 Third place still gets paid

**Regular Season Winner: $135**
📊 Best regular season record

*Total Prize Pool: $1000*
            """
            self.send_message(payout_text)
            
        elif command == '/activity':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                activity_text = self.get_recent_activity()
                self.send_message(activity_text)
            except Exception as e:
                logger.error(f"Error getting activity: {e}")
                self.send_message("❌ Error retrieving recent activity. Please try again later.")
                
        elif command == '/starters':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                starters_text = self.get_my_starters()
                self.send_message(starters_text)
            except Exception as e:
                logger.error(f"Error getting starters: {e}")
                self.send_message("❌ Error retrieving starters. Please try again later.")
                
        elif command == '/rank':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                rank_text = self.get_top_players()
                self.send_message(rank_text)
            except Exception as e:
                logger.error(f"Error getting rankings: {e}")
                self.send_message("❌ Error retrieving player rankings. Please try again later.")
                
        elif command.startswith('/matchup'):
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                # Extract team name from command
                team_name = command.replace('/matchup', '').strip()
                logger.info(f"Matchup command - team_name: '{team_name}'")
                
                if not team_name:
                    # No team specified, get user's team
                    user = message.get('from', {})
                    username = user.get('username')
                    phone = user.get('phone_number')
                    
                    logger.info(f"Matchup command - user: {user}, username: {username}, phone: {phone}")
                    
                    if username:
                        username = f"@{username}"
                    elif phone:
                        username = f"+{phone}" if not phone.startswith('+') else phone
                    else:
                        username = None
                    
                    logger.info(f"Matchup command - processed username: {username}")
                    
                    if not username:
                        self.send_message("❌ You're not registered! Use `/register Team Name` first, or specify a team: `/matchup Team Name`")
                        return
                    
                    # Get user's team name
                    team_id = self.team_mappings.get(username)
                    logger.info(f"Matchup command - team_id from mappings: {team_id}")
                    
                    if not team_id:
                        self.send_message("❌ You're not registered! Use `/register Team Name` first, or specify a team: `/matchup Team Name`")
                        return
                    
                    # Find team name from team ID
                    for team in self.league.teams:
                        if team.team_id == team_id:
                            team_name = team.team_name
                            break
                    else:
                        self.send_message("❌ Could not find your team. Please try `/register Team Name` again.")
                        return
                    
                    logger.info(f"Matchup command - found team_name: {team_name}")
                
                matchup_text = self.get_matchup_vs_team(team_name)
                self.send_message(matchup_text)
            except Exception as e:
                logger.error(f"Error getting matchup: {e}")
                self.send_message("❌ Error retrieving matchup. Please try again later.")
                
        elif command == '/myteam':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                # Get username or phone number from message
                user = message.get('from', {})
                username = user.get('username')
                phone = user.get('phone_number')
                
                if username:
                    username = f"@{username}"
                elif phone:
                    username = f"+{phone}" if not phone.startswith('+') else phone
                else:
                    username = None
                
                myteam_text = self.get_my_team_info(username)
                self.send_message(myteam_text)
            except Exception as e:
                logger.error(f"Error getting my team: {e}")
                self.send_message("❌ Error retrieving your team. Please try again later.")
                
        elif command.startswith('/register'):
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                # Extract team name from command
                team_name = command.replace('/register', '').strip()
                if not team_name:
                    self.send_message("❌ Please specify a team name: `/register Team Name`")
                    return
                
                # Find the team by name
                team_id = None
                for team in self.league.teams:
                    if team.team_name.lower() == team_name.lower():
                        team_id = team.team_id
                        break
                
                if not team_id:
                    self.send_message(f"❌ Team '{team_name}' not found. Available teams:\n" + \
                                    "\n".join([f"• {team.team_name}" for team in self.league.teams]))
                    return
                
                # Get username or phone number from message
                user = message.get('from', {})
                username = user.get('username')
                phone = user.get('phone_number')
                
                if username:
                    username = f"@{username}"
                    self.team_mappings[username] = team_id
                    self.send_message(f"✅ Registered! @{username} is now mapped to '{team_name}' (ID: {team_id})")
                elif phone:
                    phone = f"+{phone}" if not phone.startswith('+') else phone
                    self.team_mappings[phone] = team_id
                    self.send_message(f"✅ Registered! {phone} is now mapped to '{team_name}' (ID: {team_id})")
                else:
                    self.send_message("❌ Could not get your username or phone number. Make sure you have a username set in Telegram or share your phone number.")
            except Exception as e:
                logger.error(f"Error registering team: {e}")
                self.send_message("❌ Error registering team. Please try again later.")
                
        elif command == '/draft':
            try:
                draft_text = self.get_draft_countdown()
                self.send_message(draft_text)
            except Exception as e:
                logger.error(f"Error getting draft info: {e}")
                self.send_message("❌ Error retrieving draft information. Please try again later.")
                
        elif command == '/cap':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                cap_text = self.get_salary_cap_info()
                self.send_message(cap_text)
            except Exception as e:
                logger.error(f"Error getting salary cap: {e}")
                self.send_message("❌ Error retrieving salary cap information. Please try again later.")
                
        elif command == '/debug':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                # Get username or phone number from message
                user = message.get('from', {})
                username = user.get('username')
                phone = user.get('phone_number')
                
                if username:
                    username = f"@{username}"
                elif phone:
                    username = f"+{phone}" if not phone.startswith('+') else phone
                else:
                    username = None
                
                debug_text = self.debug_player_attributes(username)
                self.send_message(debug_text)
            except Exception as e:
                logger.error(f"Error in debug: {e}")
                self.send_message("❌ Error in debug. Please try again later.")
                
        elif command == '/teams_debug':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                debug_text = "🔍 *Team ID Debug Info*\n\n"
                debug_text += "*All Teams:*\n"
                
                for team in self.league.teams:
                    debug_text += f"• **{team.team_name}** (ID: {team.team_id})\n"
                
                debug_text += "\n*Current Mappings:*\n"
                for username, team_id in self.team_mappings.items():
                    debug_text += f"• {username} → Team ID {team_id}\n"
                
                self.send_message(debug_text)
            except Exception as e:
                logger.error(f"Error in teams debug: {e}")
                self.send_message("❌ Error in teams debug. Please try again later.")
                
        elif command == '/teams':
            if not self.league:
                self.send_message("❌ League not initialized. Check your configuration.")
                return
            
            try:
                teams_text = self.get_teams_info()
                self.send_message(teams_text)
            except Exception as e:
                logger.error(f"Error getting teams: {e}")
                self.send_message("❌ Error retrieving teams. Please try again later.")
    
    def get_draft_countdown(self) -> str:
        """Get draft countdown information"""
        try:
            # Draft date: Sunday, August 31, 2025 at 5:00 PM PST
            draft_date = "2025-08-31 17:00:00"
            draft_timezone = "US/Pacific"
            
            from datetime import datetime
            import pytz
            
            # Parse draft date
            pacific_tz = pytz.timezone(draft_timezone)
            draft_datetime = pacific_tz.localize(datetime.strptime(draft_date, "%Y-%m-%d %H:%M:%S"))
            
            # Get current time in Pacific timezone
            now = datetime.now(pacific_tz)
            
            # Calculate time difference
            time_diff = draft_datetime - now
            
            if time_diff.total_seconds() <= 0:
                return "🎯 *Draft Status*\n\n✅ **Draft has started!**\n\nGood luck to all teams!"
            
            # Calculate days, hours, minutes
            days = time_diff.days
            hours = time_diff.seconds // 3600
            minutes = (time_diff.seconds % 3600) // 60
            
            draft_text = "🎯 *Draft Countdown*\n\n"
            draft_text += f"📅 **Date:** Sunday, August 31, 2025\n"
            draft_text += f"⏰ **Time:** 5:00 PM PST\n\n"
            
            if days > 0:
                draft_text += f"⏳ **Time Remaining:** {days} days, {hours} hours, {minutes} minutes\n\n"
            elif hours > 0:
                draft_text += f"⏳ **Time Remaining:** {hours} hours, {minutes} minutes\n\n"
            else:
                draft_text += f"⏳ **Time Remaining:** {minutes} minutes\n\n"
            
            draft_text += "🏈 Get ready for the draft!\n"
            draft_text += "📋 Make sure your draft board is ready\n"
            draft_text += "💻 Test your draft software if needed"
            
            return draft_text
            
        except Exception as e:
            logger.error(f"Error calculating draft countdown: {e}")
            return "🎯 *Draft Information*\n\n📅 **Date:** Sunday, August 31, 2025\n⏰ **Time:** 5:00 PM PST"
    
    def get_salary_cap_info(self) -> str:
        """Get salary cap information for all teams"""
        if not self.league:
            return "❌ League not initialized"
        
        try:
            cap_text = "💰 *Salary Cap Status*\n\n"
            
            # Check if this is a salary cap league
            if hasattr(self.league, 'settings') and hasattr(self.league.settings, 'salary_cap'):
                total_cap = self.league.settings.salary_cap
                cap_text += f"**Total Cap:** ${total_cap:,}\n\n"
            else:
                cap_text += "**Total Cap:** $200 (Standard)\n\n"
            
            cap_text += "*Team Cap Usage:*\n"
            
            for team in self.league.teams:
                team_name = team.team_name
                
                # Try to get team's salary cap info
                if hasattr(team, 'salary_cap_used'):
                    cap_used = team.salary_cap_used
                    cap_remaining = total_cap - cap_used if 'total_cap' in locals() else 200 - cap_used
                    cap_text += f"• **{team_name}:** ${cap_used:,} used, ${cap_remaining:,} remaining\n"
                else:
                    cap_text += f"• **{team_name}:** Cap info not available\n"
            
            cap_text += "\n💡 *Note:* Salary cap information may not be available for all leagues."
            
            return cap_text
            
        except Exception as e:
            logger.error(f"Error getting salary cap info: {e}")
            return "❌ Error retrieving salary cap information."
    
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
                
                teams_text += f"*{team.team_name}* (ID: {team.team_id})\n"
                if hasattr(team, 'owner') and team.owner:
                    teams_text += f"Owner: {team.owner}\n"
                teams_text += f"Record: {record}\n"
                teams_text += f"Points: {team.points_for:.1f}\n\n"
            
            return teams_text
            
        except Exception as e:
            logger.error(f"Error getting teams: {e}")
            return "❌ Error retrieving teams"
    
    def get_my_starters(self) -> str:
        """Get current week starters for all teams"""
        if not self.league:
            return "❌ League not initialized"
        
        try:
            current_week = self.league.current_week
            starters_text = f"🏈 *Week {current_week} Starters*\n\n"
            
            for team in self.league.teams:
                starters_text += f"*{team.team_name}*\n"
                
                # Check if starters attribute exists
                if hasattr(team, 'starters') and team.starters:
                    for player in team.starters:
                        position = player.position
                        name = player.name
                        
                        # Try multiple possible projected points attributes
                        projected = "N/A"
                        if hasattr(player, 'projected_points') and player.projected_points:
                            projected = f"{player.projected_points:.1f}"
                        elif hasattr(player, 'projected') and player.projected:
                            projected = f"{player.projected:.1f}"
                        elif hasattr(player, 'proj_points') and player.proj_points:
                            projected = f"{player.proj_points:.1f}"
                        
                        actual = f"{player.points:.1f}" if hasattr(player, 'points') and player.points else "0.0"
                        
                        starters_text += f"  {position}: {name} ({projected} proj, {actual} pts)\n"
                else:
                    # Fallback to roster if starters not available
                    starters_text += "  *Roster:*\n"
                    for player in team.roster:
                        position = player.position
                        name = player.name
                        
                        # Try multiple possible projected points attributes
                        projected = "N/A"
                        if hasattr(player, 'projected_points') and player.projected_points:
                            projected = f"{player.projected_points:.1f}"
                        elif hasattr(player, 'projected') and player.projected:
                            projected = f"{player.projected:.1f}"
                        elif hasattr(player, 'proj_points') and player.proj_points:
                            projected = f"{player.proj_points:.1f}"
                        
                        actual = f"{player.points:.1f}" if hasattr(player, 'points') and player.points else "0.0"
                        
                        starters_text += f"  {position}: {name} ({projected} proj, {actual} pts)\n"
                
                starters_text += "\n"
            
            return starters_text
            
        except Exception as e:
            logger.error(f"Error getting starters: {e}")
            return "❌ Error retrieving starters"
    
    def get_top_players(self) -> str:
        """Get top performing players this week"""
        if not self.league:
            return "❌ League not initialized"
        
        try:
            current_week = self.league.current_week
            rank_text = f"🏆 *Week {current_week} Top Performers*\n\n"
            
            all_players = []
            
            # Collect all players from all teams
            for team in self.league.teams:
                for player in team.roster:
                    if hasattr(player, 'points') and player.points:
                        all_players.append({
                            'name': player.name,
                            'position': player.position,
                            'team': player.pro_team if hasattr(player, 'pro_team') else 'N/A',
                            'points': player.points,
                            'owner': team.team_name
                        })
            
            # Sort by points and get top 15
            all_players.sort(key=lambda x: x['points'], reverse=True)
            top_players = all_players[:15]
            
            for i, player in enumerate(top_players, 1):
                rank_text += f"**{i}.** {player['name']} ({player['position']})\n"
                rank_text += f"    {player['team']} | {player['points']:.1f} pts | {player['owner']}\n\n"
            
            return rank_text
            
        except Exception as e:
            logger.error(f"Error getting rankings: {e}")
            return "❌ Error retrieving player rankings"
    
    def get_matchup_vs_team(self, team_name: str) -> str:
        """Get matchup details vs a specific team"""
        if not self.league:
            return "❌ League not initialized"
        
        try:
            current_week = self.league.current_week
            
            # Find the team
            target_team = None
            for team in self.league.teams:
                if team.team_name.lower() == team_name.lower():
                    target_team = team
                    break
            
            if not target_team:
                return f"❌ Team '{team_name}' not found. Available teams:\n" + \
                       "\n".join([f"• {team.team_name}" for team in self.league.teams])
            
            # Find the matchup
            matchup = None
            for game in self.league.scoreboard():
                if (game.home_team.team_name == target_team.team_name or 
                    game.away_team.team_name == target_team.team_name):
                    matchup = game
                    break
            
            if not matchup:
                return f"❌ No matchup found for {target_team.team_name} in Week {current_week}"
            
            # Build matchup text
            home_team = matchup.home_team
            away_team = matchup.away_team
            
            matchup_text = f"🏈 *Week {current_week} Matchup*\n\n"
            matchup_text += f"*{home_team.team_name}* vs *{away_team.team_name}*\n\n"
            
            # Scores
            home_score = f"{home_team.score:.1f}" if hasattr(home_team, 'score') and home_team.score else "0.0"
            away_score = f"{away_team.score:.1f}" if hasattr(away_team, 'score') and away_team.score else "0.0"
            matchup_text += f"Score: {home_score} - {away_score}\n"
            
            # Status
            if matchup.status == "FINAL":
                matchup_text += "✅ *Final*\n"
            elif matchup.status == "IN_PROGRESS":
                matchup_text += "🔄 *Live*\n"
            else:
                matchup_text += "⏰ *Scheduled*\n"
            
            # Projected scores if available
            if hasattr(home_team, 'projected_points') and home_team.projected_points:
                home_proj = f"{home_team.projected_points:.1f}"
                away_proj = f"{away_team.projected_points:.1f}" if hasattr(away_team, 'projected_points') and away_team.projected_points else "N/A"
                matchup_text += f"Projected: {home_proj} - {away_proj}\n"
            
            return matchup_text
            
        except Exception as e:
            logger.error(f"Error getting matchup: {e}")
            return "❌ Error retrieving matchup"
    
    def debug_player_attributes(self, username: str) -> str:
        """Debug method to see what attributes are available on player objects"""
        if not self.league:
            return "❌ League not initialized"
        
        try:
            # Find the team for this user
            team_id = self.team_mappings.get(username)
            if not team_id:
                return f"❌ You're not registered! Use `/register Team Name` to register your team."
            
            # Find the team in the league by ID
            user_team = None
            for team in self.league.teams:
                if team.team_id == team_id:
                    user_team = team
                    break
            
            if not user_team:
                return f"❌ Team ID {team_id} not found in league."
            
            debug_text = f"🔍 *Debug: {user_team.team_name} Player Attributes*\n\n"
            
            # Check first few players
            for i, player in enumerate(user_team.roster[:3]):
                debug_text += f"**Player {i+1}: {player.name}**\n"
                debug_text += f"Available attributes: {[attr for attr in dir(player) if not attr.startswith('_')]}\n"
                
                # Check specific projection attributes
                for attr in ['projected_points', 'projected', 'proj_points', 'points']:
                    if hasattr(player, attr):
                        value = getattr(player, attr)
                        debug_text += f"{attr}: {value}\n"
                    else:
                        debug_text += f"{attr}: Not available\n"
                debug_text += "\n"
            
            return debug_text
            
        except Exception as e:
            logger.error(f"Error in debug: {e}")
            return f"❌ Error in debug: {e}"

    def get_my_team_info(self, username: str) -> str:
        """Get information for a specific user's team"""
        if not self.league:
            return "❌ League not initialized"
        
        try:
            # Find the team for this user
            team_id = self.team_mappings.get(username)
            if not team_id:
                return f"❌ You're not registered! Use `/register Team Name` to register your team.\n\nAvailable teams:\n" + \
                       "\n".join([f"• {team.team_name} (ID: {team.team_id})" for team in self.league.teams])
            
            # Find the team in the league by ID
            user_team = None
            for team in self.league.teams:
                if team.team_id == team_id:
                    user_team = team
                    break
            
            if not user_team:
                return f"❌ Team ID {team_id} not found in league."
            
            # Build team info
            current_week = self.league.current_week
            team_text = f"🏈 *{user_team.team_name}* (Week {current_week})\n\n"
            
            # Record
            record = f"{user_team.wins}-{user_team.losses}"
            if hasattr(user_team, 'ties') and user_team.ties > 0:
                record += f"-{user_team.ties}"
            team_text += f"Record: {record}\n"
            team_text += f"Points For: {user_team.points_for:.1f}\n"
            team_text += f"Points Against: {user_team.points_against:.1f}\n\n"
            
            # Try to get projected points from current week matchup
            projected_team_score = None
            try:
                for game in self.league.scoreboard():
                    if (game.home_team.team_id == team_id or game.away_team.team_id == team_id):
                        if game.home_team.team_id == team_id:
                            projected_team_score = game.home_team.projected_points if hasattr(game.home_team, 'projected_points') else None
                        else:
                            projected_team_score = game.away_team.projected_points if hasattr(game.away_team, 'projected_points') else None
                        break
            except:
                pass
            
            # Current week starters - check if starters attribute exists
            team_text += "*This Week's Starters:*\n"
            if hasattr(user_team, 'starters') and user_team.starters:
                for player in user_team.starters:
                    position = player.position
                    name = player.name
                    
                    # Try multiple possible projected points attributes
                    projected = "N/A"
                    if hasattr(player, 'projected_points') and player.projected_points:
                        projected = f"{player.projected_points:.1f}"
                    elif hasattr(player, 'projected') and player.projected:
                        projected = f"{player.projected:.1f}"
                    elif hasattr(player, 'proj_points') and player.proj_points:
                        projected = f"{player.proj_points:.1f}"
                    
                    actual = f"{player.points:.1f}" if hasattr(player, 'points') and player.points else "0.0"
                    
                    team_text += f"  {position}: {name} ({projected} proj, {actual} pts)\n"
            else:
                # Fallback to roster if starters not available
                team_text += "  *Roster:*\n"
                for player in user_team.roster:
                    position = player.position
                    name = player.name
                    
                    # Try multiple possible projected points attributes
                    projected = "N/A"
                    if hasattr(player, 'projected_points') and player.projected_points:
                        projected = f"{player.projected_points:.1f}"
                    elif hasattr(player, 'projected') and player.projected:
                        projected = f"{player.projected:.1f}"
                    elif hasattr(player, 'proj_points') and player.proj_points:
                        projected = f"{player.proj_points:.1f}"
                    
                    actual = f"{player.points:.1f}" if hasattr(player, 'points') and player.points else "0.0"
                    
                    team_text += f"  {position}: {name} ({projected} proj, {actual} pts)\n"
            
            team_text += "\n"
            
            # Current week score and projected
            if hasattr(user_team, 'score') and user_team.score:
                current_score = f"{user_team.score:.1f}"
                team_text += f"*Current Week Score: {current_score}*"
            else:
                team_text += "*Current Week Score: Not available*"
            
            if projected_team_score:
                team_text += f"\n*Projected Week Score: {projected_team_score:.1f}*"
            
            return team_text
            
        except Exception as e:
            logger.error(f"Error getting my team info: {e}")
            return "❌ Error retrieving your team information."
    
    def get_recent_activity(self) -> str:
        """Get recent league activity"""
        if not self.league:
            return "❌ League not initialized"
        
        try:
            # Get recent activity (last 10 items)
            activities = self.league.recent_activity()
            
            if not activities:
                return "📊 *Recent Activity*\n\nNo recent activity found."
            
            activity_text = "📊 *Recent League Activity*\n\n"
            
            for i, activity in enumerate(activities[:10], 1):  # Show last 10 activities
                # Format the activity based on type
                if hasattr(activity, 'type') and activity.type:
                    activity_type = activity.type
                else:
                    activity_type = "Transaction"
                
                # Get team name if available
                team_name = "Unknown Team"
                if hasattr(activity, 'team') and activity.team:
                    team_name = activity.team.team_name
                
                # Get description if available
                description = "No description available"
                if hasattr(activity, 'description') and activity.description:
                    description = activity.description
                
                # Format timestamp if available
                timestamp = ""
                if hasattr(activity, 'timestamp') and activity.timestamp:
                    timestamp = f" ({activity.timestamp})"
                
                activity_text += f"**{i}.** {activity_type}\n"
                activity_text += f"👤 {team_name}\n"
                activity_text += f"📝 {description}{timestamp}\n\n"
            
            return activity_text
            
        except Exception as e:
            logger.error(f"Error getting recent activity: {e}")
            return "❌ Error retrieving recent activity."
    
    def run(self):
        """Run the bot"""
        # Initialize league connection
        if not self.initialize_league():
            logger.error("Failed to initialize league. Check your configuration.")
            return
        
        # Send startup message
        self.send_message("🤖 ESPN Fantasy Bot is now running and ready to respond!")
        logger.info("Bot started successfully!")
        
        while True:
            try:
                # Get updates
                updates = self.get_updates()
                
                if updates and updates.get('ok'):
                    for update in updates.get('result', []):
                        self.last_update_id = update.get('update_id', self.last_update_id)
                        
                        if 'message' in update:
                            message = update['message']
                            self.handle_command(message)
                
                # Small delay to avoid hitting rate limits
                time.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(5)  # Wait before retrying

def main():
    """Main function"""
    try:
        bot = MinimalESPNBot()
        bot.run()
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")

if __name__ == "__main__":
    main()
