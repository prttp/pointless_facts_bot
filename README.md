# 🤖 Telegram Bot for Pointless Facts

Telegram bot that fetches pointless facts via HTTP API and sends them to users with high-quality translation support.

## 🚀 Features

- Get random pointless facts
- Get today's fact
- **Multi-language support** (English and Russian)
- **High-quality translation** using DeepL API (with Google Translate fallback)
- **Translation caching** - saves API calls by storing translations in SQLite database
- Interactive buttons for easy use
- Error handling and logging
- Markdown formatting support
- Docker support

## 📋 Requirements

- Python 3.8+
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- DeepL API Key (optional, for premium translation quality)
- PostgreSQL database

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/prttp/pointless_facts_bot
   cd pointless_facts_bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `config.env.example` to `.env`
   ```bash
   cp config.env.example .env
   ```
   - Fill in your configuration (see [Environment Variables](#environment-variables) table below)

## 🌍 Translation Features

### **Translation Quality:**
- **DeepL Translator** (Premium) - Highest quality translation when API key is provided
- **Google Translator** (Fallback) - Free alternative when DeepL is not available

### **Language Support:**
- **Interface**: English and Russian
- **Facts**: Automatically translated from English to target language
- **Fallback**: If translation fails, original English text is shown

## 🚀 Running

### Option 1: Direct Python
```bash
python bot.py
```

### Option 2: Docker (Recommended)
```bash
# Build and run with Docker Compose
docker compose up -d

# View logs
docker compose logs -f

# Stop the bot
docker compose down

# Rebuild after code changes
docker compose down --rmi all && docker compose build --no-cache && docker compose up -d
```

## 📱 Usage

### Bot Commands:

- `/start` - Start working with the bot
- `/help` - Show help and usage guide
- `/random` - Get a random fact
- `/today` - Get today's fact

### Interactive Buttons:

- 🎲 **Random Fact** - get a random fact
- 📅 **Today's Fact** - get today's fact

## 🔧 API Endpoints

The bot uses the following API endpoints:

- `GET /api/v2/facts/random` - get a random fact
- `GET /api/v2/facts/today` - get today's fact
- `?language=en` - specify language (English by default)
- `Accept: application/json` - get response in JSON format

## 📁 Project Structure

```
pointless_facts_bot/
├── bot.py              # Main bot file with Telegram handlers
├── database.py         # Database manager for translation caching
├── translations.py     # Interface translations
├── requirements.txt    # Python dependencies
├── config.env.example  # Configuration example
├── .env               # Environment variables file (create)
├── init_db.sql        # PostgreSQL initialization script
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose setup
├── .dockerignore      # Docker ignore file
└── README.md          # Documentation
```

## 🔒 Security

- Never publish your `TELEGRAM_BOT_TOKEN` or `DEEPL_API_KEY`
- Add `.env` to `.gitignore`
- Use HTTPS for API requests
- API keys are stored in environment variables

## 🐛 Logging

The bot logs all operations including:
- Translation service being used (DeepL/Google)
- Translation attempts and results
- API requests and responses
- Database connection status and operations
- Cache hits and misses
- Error handling and recovery

### **Log Levels:**
- **INFO** - Normal operations, cache hits, successful translations
- **WARNING** - Database connection issues, translation fallbacks
- **ERROR** - Critical failures, API errors

### **Log Sources:**
- **`bot.py`** - Telegram interactions and fact retrieval
- **`database.py`** - Database operations and caching
- **Translation services** - DeepL and Google Translate operations

Logs are output to console with INFO level and can be viewed in Docker with `docker compose logs -f`.

## 📝 Response Examples

### Random Fact (Russian):
```
**Случайный факт:**

Мед никогда не портится. Археологи нашли горшки с медом в древнеегипетских гробницах, которым более 3000 лет, и они все еще съедобны.
```

### Today's Fact (English):
```
**Today's Fact:**

Bananas are berries, but strawberries aren't. In botanical terms, a berry is a fruit produced from the ovary of a single flower with seeds embedded in the flesh.
```

## 🏗️ Architecture

The project follows a modular architecture with clear separation of concerns:

### **Core Components:**

1. **`bot.py`** - Main Telegram bot application
   - Handles Telegram API interactions
   - Manages user commands and callbacks
   - Coordinates translation and fact retrieval
   - Uses `DatabaseManager` for caching operations

2. **`database.py`** - Database management layer
   - `DatabaseManager` class for PostgreSQL operations
   - Translation caching with hash-based lookups
   - Connection pooling and error handling
   - Automatic retry logic for database connections

3. **`translations.py`** - Interface localization
   - Multi-language support for bot interface
   - Centralized text management

### **Architecture Benefits:**
- **Separation of Concerns** - Database logic isolated from bot logic
- **Reusability** - `DatabaseManager` can be used in other parts of the project
- **Testability** - Each component can be tested independently
- **Maintainability** - Clear structure makes code easier to understand and modify
- **Scalability** - Modular design allows for easy expansion

## 🔧 Configuration Options

### Environment Variables: {#environment-variables}

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | - | Your Telegram bot token |
| `LANGUAGE` | ❌ No | `en` | Bot language (`en`/`ru`) |
| `FACTS_API_URL` | ❌ No | API URL | Facts API endpoint |
| `DEEPL_API_KEY` | ❌ No | - | DeepL API key for premium translation |
| `DATABASE_URL` | ❌ No | PostgreSQL | Database connection string |

### Translation Priority:
1. **Cache** (if translation exists)
2. **DeepL** (if API key provided)
3. **Google Translate** (fallback)
4. **Original text** (if translation fails)

## 💾 Translation Caching

The bot automatically caches translations in PostgreSQL database using the `DatabaseManager` class to save API calls and improve performance.

### Cache Features:
- **Automatic caching** - translations are saved after first use
- **Hash-based lookup** - fast retrieval using MD5 hash of original text
- **Translator tracking** - stores which translator was used (DeepL/Google)
- **Timestamp tracking** - records when translations were created
- **PostgreSQL database** - production-ready, scalable storage
- **Indexed queries** - optimized for fast lookups
- **Connection management** - robust database connection handling with retry logic
- **Error resilience** - bot continues working even if database operations fail

### Cache Management:

For advanced cache management, you can connect directly to the PostgreSQL database:

```bash
# Connect to database container
docker exec -it facts_bot_db psql -U postgres -d facts_bot

# Show cache statistics
SELECT COUNT(*) as total_translations FROM translation_cache;
SELECT translator_used, COUNT(*) FROM translation_cache GROUP BY translator_used;

# Show recent translations
SELECT original_text, translated_text, translator_used, created_at 
FROM translation_cache ORDER BY created_at DESC LIMIT 10;

# Clear all cached translations
DELETE FROM translation_cache;
```

### Cache Benefits:
- **Cost savings** - reduces DeepL API calls
- **Speed improvement** - instant retrieval of cached translations
- **Consistency** - same fact always gets same translation

## 🧪 Development & Testing

### **Running Tests:**
```bash
# Test API connectivity
python test_api.py

# Test database connection
python -c "from database import DatabaseManager; db = DatabaseManager('postgresql://postgres:postgres@localhost:5432/facts_bot'); print('Database available:', db.is_available())"
```

### **Code Structure:**
- **`bot.py`** - Contains `FactsBot` class with Telegram handlers
- **`database.py`** - Contains `DatabaseManager` class for database operations
- **`translations.py`** - Contains `get_text()` function for localization

### **Key Classes:**
- **`FactsBot`** - Main bot class handling Telegram interactions
- **`DatabaseManager`** - Database operations and translation caching
- **`GoogleTranslator`/`DeeplTranslator`** - Translation services

## 🤝 Contributing

1. Fork the repository
2. Create a branch for new feature
3. Make changes following the modular architecture
4. Test your changes
5. Create Pull Request

## 📄 License

This project is distributed under MIT license.

## 🔗 Useful Links

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [Useless Facts API](https://uselessfacts.jsph.pl/)
- [DeepL API](https://www.deepl.com/pro-api)
- [@BotFather](https://t.me/BotFather) - Telegram bot creation 
