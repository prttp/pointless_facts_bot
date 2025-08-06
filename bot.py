# -*- coding: utf-8 -*-
import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from translations import get_text

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
LANGUAGE = os.getenv('LANGUAGE', 'en')
SUPPORTED_LANGUAGES = ['ru', 'en']
if LANGUAGE not in SUPPORTED_LANGUAGES:
    logger.warning(f"Unsupported language: {LANGUAGE}, using default 'en'")
    LANGUAGE = 'en'

class FactsBot:
    def __init__(self):
        self.api_url = FACTS_API_URL
    
    def escape_markdown(self, text):
        """Escape special characters for Markdown"""
        # Only escape characters that can break Markdown parsing
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '=', '|', '{', '}']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        welcome_text = (
            f"{get_text('welcome', LANGUAGE)}\n\n"
            f"{get_text('available_commands', LANGUAGE)}\n"
            f"{get_text('random_command', LANGUAGE)}\n"
            f"{get_text('today_command', LANGUAGE)}\n"
            f"{get_text('help_command', LANGUAGE)}\n\n"
            f"{get_text('use_buttons', LANGUAGE)}"
        )
        
        keyboard = [
            [
                InlineKeyboardButton(f"🎲 {get_text('random_fact_button', LANGUAGE)}", callback_data="random"),
                InlineKeyboardButton(f"📅 {get_text('today_fact_button', LANGUAGE)}", callback_data="today")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        help_text = (
            f"{get_text('help_title', LANGUAGE)}\n\n"
            f"{get_text('commands_section', LANGUAGE)}\n"
            f"{get_text('random_command', LANGUAGE)}\n"
            f"{get_text('today_command', LANGUAGE)}\n"
            f"{get_text('help_command', LANGUAGE)}\n\n"
            f"{get_text('language_section', LANGUAGE)}\n"
            f"{get_text('language_info', LANGUAGE)}"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def get_random_fact(self, update: Update, context: ContextTypes.DEFAULT_TYPE, language='en'):
        """Get random fact"""
        try:
            url = f"{self.api_url}/random"
            
            response = requests.get(url, headers={'Accept': 'application/json'})
            response.raise_for_status()
            
            fact_data = response.json()
            fact_text = fact_data.get('text', get_text('fact_not_found', LANGUAGE))
            
            # Escape special characters in fact text only
            escaped_fact = self.escape_markdown(fact_text)
            
            message = f"{get_text('random_fact_title', LANGUAGE)}\n\n{escaped_fact}"
            
            if update.callback_query:
                await update.callback_query.answer()
                await update.callback_query.edit_message_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text(message, parse_mode='Markdown')
                
        except requests.RequestException as e:
            error_msg = f"{get_text('error_getting_fact', LANGUAGE)} {str(e)}"
            if update.callback_query:
                await update.callback_query.answer(error_msg, show_alert=True)
            else:
                await update.message.reply_text(error_msg)
        except Exception as e:
            logger.error(f"Error in get_random_fact: {e}")
            error_msg = get_text('unexpected_error', LANGUAGE)
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
            fact_text = fact_data.get('text', get_text('today_fact_not_found', LANGUAGE))
            
            # Escape special characters in fact text only
            escaped_fact = self.escape_markdown(fact_text)
            
            message = f"{get_text('today_fact_title', LANGUAGE)}\n\n{escaped_fact}"
            
            if update.callback_query:
                await update.callback_query.answer()
                await update.callback_query.edit_message_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text(message, parse_mode='Markdown')
                
        except requests.RequestException as e:
            error_msg = f"{get_text('error_getting_today_fact', LANGUAGE)} {str(e)}"
            if update.callback_query:
                await update.callback_query.answer(error_msg, show_alert=True)
            else:
                await update.message.reply_text(error_msg)
        except Exception as e:
            logger.error(f"Error in get_today_fact: {e}")
            error_msg = get_text('unexpected_error', LANGUAGE)
            if update.callback_query:
                await update.callback_query.answer(error_msg, show_alert=True)
            else:
                await update.message.reply_text(error_msg)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Button click handler"""
        query = update.callback_query
        await query.answer()

        if query.data == "random":
            await self.get_random_fact(update, context)
        elif query.data == "today":
            await self.get_today_fact(update, context)
    
    async def random_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Random command handler"""
        await self.get_random_fact(update, context)
    
    async def today_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Today command handler"""
        await self.get_today_fact(update, context)

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