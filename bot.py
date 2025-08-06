# -*- coding: utf-8 -*-
import os
import logging
import requests
import hashlib
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from translations import get_text
from deep_translator import GoogleTranslator, DeeplTranslator

# Database imports
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Disable frequent HTTP logs from httpx and telegram
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('telegram.ext').setLevel(logging.WARNING)

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
FACTS_API_URL = os.getenv('FACTS_API_URL', 'https://uselessfacts.jsph.pl/api/v2/facts')
LANGUAGE = os.getenv('LANGUAGE', 'en')
SUPPORTED_LANGUAGES = ['ru', 'en']
if LANGUAGE not in SUPPORTED_LANGUAGES:
    logger.warning(f"Unsupported language: {LANGUAGE}, using default 'en'")
    LANGUAGE = 'en'

# DeepL API key
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/facts_bot')

class FactsBot:
    def __init__(self):
        self.api_url = FACTS_API_URL
        self.database_url = DATABASE_URL
        
        # Test database connection
        self._test_db_connection()
        
        # Try DeepL first, fallback to Google
        try:
            self.translator = DeeplTranslator(source='en', target=LANGUAGE, api_key=DEEPL_API_KEY)
            logger.info("Using DeepL Translator")
        except Exception as e:
            logger.warning(f"DeepL initialization failed: {e}")
            self.translator = GoogleTranslator(source='en', target=LANGUAGE)
            logger.info("Using Google Translator")
    

    
    def _test_db_connection(self):
        """Test database connection and verify table exists"""
        max_retries = 5
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                conn = psycopg2.connect(self.database_url)
                cursor = conn.cursor()
                
                # Test basic connection
                cursor.execute('SELECT 1')
                cursor.fetchone()
                
                # Check if translation_cache table exists
                cursor.execute('''
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'translation_cache'
                    )
                ''')
                table_exists = cursor.fetchone()[0]
                
                conn.close()
                
                if table_exists:
                    logger.info("Database connection successful - translation_cache table found")
                    return
                else:
                    logger.warning("Database connected but translation_cache table not found")
                    # Table will be created by init_db.sql, so this is expected on first run
                    return
                    
            except Exception as e:
                logger.warning(f"Database connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error(f"Failed to connect to database after {max_retries} attempts")
                    logger.warning("Bot will continue without translation caching")
                    # Don't raise exception - bot can work without cache
    
    def _get_fact_hash(self, text):
        """Generate hash for fact text"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _get_cached_translation(self, text):
        """Get cached translation if exists"""
        try:
            fact_hash = self._get_fact_hash(text)
            
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            cursor.execute(
                'SELECT translated_text, translator_used FROM translation_cache WHERE fact_hash = %s',
                (fact_hash,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                translated_text, translator_used = result
                logger.info(f"Cache hit: {translator_used} translation found")
                return translated_text
            return None
        except Exception as e:
            logger.warning(f"Failed to read from cache: {e}")
            return None
    
    def _save_translation_to_cache(self, original_text, translated_text, translator_used):
        """Save translation to cache"""
        try:
            fact_hash = self._get_fact_hash(original_text)
            
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO translation_cache (fact_hash, original_text, translated_text, translator_used) VALUES (%s, %s, %s, %s) ON CONFLICT (fact_hash) DO UPDATE SET translated_text = EXCLUDED.translated_text, translator_used = EXCLUDED.translator_used, created_at = CURRENT_TIMESTAMP',
                (fact_hash, original_text, translated_text, translator_used)
            )
            conn.commit()
            conn.close()
            
            logger.info(f"Translation saved to cache: {translator_used}")
        except Exception as e:
            logger.warning(f"Failed to save to cache: {e}")
            # Don't raise the exception - just log it and continue
            # This prevents the bot from crashing if cache operations fail
    
    def escape_markdown(self, text):
        """Escape special characters for Markdown"""
        # Only escape characters that can break Markdown parsing
        special_chars = ['_', '*', '[', ']', '~', '`', '>', '#', '+', '=', '|', '{', '}']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text
    
    def translate_fact(self, text):
        """Translate fact text to target language with caching"""
        if LANGUAGE == 'en':
            return text
        
        if not text or text.strip() == '':
            return text
        
        # Check cache first
        cached_translation = self._get_cached_translation(text)
        if cached_translation:
            return cached_translation
        
        # Translate and cache the result
        try:
            translated = self.translator.translate(text)
            translator_name = "DeepL" if isinstance(self.translator, DeeplTranslator) else "Google"
            
            # Save to cache
            self._save_translation_to_cache(text, translated, translator_name)
            
            logger.info(f"Translated: '{text}' -> '{translated}' ({translator_name})")
            return translated
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text  # Return original text if translation fails
    
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
            
            # Translate the fact
            translated_fact = self.translate_fact(fact_text)
            
            # Escape special characters in translated text
            escaped_translated = self.escape_markdown(translated_fact)
            
            message = f"{get_text('random_fact_title', LANGUAGE)}\n\n{escaped_translated}"
            
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
            
            # Translate the fact
            translated_fact = self.translate_fact(fact_text)
            
            # Escape special characters in translated text
            escaped_translated = self.escape_markdown(translated_fact)
            
            message = f"{get_text('today_fact_title', LANGUAGE)}\n\n{escaped_translated}"
            
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