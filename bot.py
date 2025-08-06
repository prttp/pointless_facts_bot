# -*- coding: utf-8 -*-
import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
FACTS_API_URL = os.getenv('FACTS_API_URL', 'https://uselessfacts.jsph.pl/api/v2/facts')

class FactsBot:
    def __init__(self):
        self.api_url = FACTS_API_URL
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        welcome_text = (
            "Hello! I'm a bot for getting useless facts!\n\n"
            "Available commands:\n"
            "/random - get a random fact\n"
            "/today - get today's fact\n"
            "/help - show help\n\n"
            "Or use the buttons below:"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("Random Fact", callback_data="random"),
                InlineKeyboardButton("Today's Fact", callback_data="today")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        help_text = (
            "**Bot Usage Guide:**\n\n"
            "**Commands:**\n"
            "• `/random` - get a random useless fact\n"
            "• `/today` - get today's fact\n"
            "• `/help` - show this help\n\n"
            "**Language:**\n"
            "• Facts are provided in English\n\n"
            "**API:**\n"
            "Bot uses API: https://uselessfacts.jsph.pl\n\n"
            "**Examples:**\n"
            "• `/random` - random fact in English\n"
            "• `/today` - today's fact in English"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def get_random_fact(self, update: Update, context: ContextTypes.DEFAULT_TYPE, language='en'):
        """Get random fact"""
        try:
            url = f"{self.api_url}/random"
            
            response = requests.get(url, headers={'Accept': 'application/json'})
            response.raise_for_status()
            
            fact_data = response.json()
            fact_text = fact_data.get('text', 'Fact not found')

            message = f"**Random Fact:**\n\n{fact_text}"
            
            if update.callback_query:
                await update.callback_query.answer()
                await update.callback_query.edit_message_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text(message, parse_mode='Markdown')
                
        except requests.RequestException as e:
            error_msg = f"❌ Error getting fact: {str(e)}"
            if update.callback_query:
                await update.callback_query.answer(error_msg, show_alert=True)
            else:
                await update.message.reply_text(error_msg)
        except Exception as e:
            logger.error(f"Error in get_random_fact: {e}")
            error_msg = "❌ Unexpected error occurred"
            if update.callback_query:
                await update.callback_query.answer(error_msg, show_alert=True)
            else:
                await update.message.reply_text(error_msg)
    
    async def get_today_fact(self, update: Update, context: ContextTypes.DEFAULT_TYPE, language='en'):
        """Get today's fact"""
        try:
            url = f"{self.api_url}/today"
            
            response = requests.get(url, headers={'Accept': 'application/json'})
            response.raise_for_status()
            
            fact_data = response.json()
            fact_text = fact_data.get('text', 'Today\'s fact not found')

            message = f"**Today's Fact:**\n\n{fact_text}"
            
            if update.callback_query:
                await update.callback_query.answer()
                await update.callback_query.edit_message_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text(message, parse_mode='Markdown')
                
        except requests.RequestException as e:
            error_msg = f"❌ Error getting today's fact: {str(e)}"
            if update.callback_query:
                await update.callback_query.answer(error_msg, show_alert=True)
            else:
                await update.message.reply_text(error_msg)
        except Exception as e:
            logger.error(f"Error in get_today_fact: {e}")
            error_msg = "❌ Unexpected error occurred"
            if update.callback_query:
                await update.callback_query.answer(error_msg, show_alert=True)
            else:
                await update.message.reply_text(error_msg)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Button click handler"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "random":
            await self.get_random_fact(update, context, 'en')
        elif query.data == "today":
            await self.get_today_fact(update, context, 'en')
    
    async def random_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Random command handler"""
        await self.get_random_fact(update, context, 'en')
    
    async def today_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Today command handler"""
        await self.get_today_fact(update, context, 'en')

def main():
    """Main function to start the bot"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment variables!")
        return
    
    # Create bot instance
    bot = FactsBot()
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("random", bot.random_command))
    application.add_handler(CommandHandler("today", bot.today_command))
    
    # Add button handler
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    
    # Start the bot
    logger.info("Bot started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 