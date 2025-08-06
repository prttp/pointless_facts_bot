-- Initialize translation cache table
CREATE TABLE IF NOT EXISTS translation_cache (
    fact_hash VARCHAR(32) PRIMARY KEY,
    original_text TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    translator_used VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_translation_cache_created_at ON translation_cache(created_at);
CREATE INDEX IF NOT EXISTS idx_translation_cache_translator ON translation_cache(translator_used);

-- Add comments
COMMENT ON TABLE translation_cache IS 'Cache for translated facts to save API calls';
COMMENT ON COLUMN translation_cache.fact_hash IS 'MD5 hash of original text for fast lookup';
COMMENT ON COLUMN translation_cache.translator_used IS 'Which translator was used (DeepL/Google)'; 