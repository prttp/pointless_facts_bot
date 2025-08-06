# -*- coding: utf-8 -*-
import logging
import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Class for managing database connections and translation caching"""
    
    def __init__(self, database_url):
        """Initialize database manager"""
        self.database_url = database_url
        self._test_connection()
    
    def _test_connection(self):
        """Test database connection and verify table existence"""
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
    
    def get_cached_translation(self, text):
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
    
    def save_translation_to_cache(self, original_text, translated_text, translator_used):
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
    
    def is_available(self):
        """Check database availability"""
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.fetchone()
            conn.close()
            return True
        except Exception:
            return False 