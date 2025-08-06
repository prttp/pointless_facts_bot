# 🤖 Telegram Bot for Pointless Facts

Telegram bot that fetches pointless facts via HTTP API and sends them to users with high-quality translation support.

## 🚀 Features

- Get random pointless facts
- Get today's fact
- **Multi-language support** (English and Russian)
- **High-quality translation** using DeepL API (with Google Translate fallback)
- Interactive buttons for easy use
- Error handling and logging
- Markdown formatting support
- Docker support

## 📋 Requirements

- Python 3.8+
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- DeepL API Key (optional, for premium translation quality)
- Internet access

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
   - Fill in your configuration

4. **Edit the `.env` file:**
   ```env
   # Required
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   
   # Optional - Bot language (en/ru)
   LANGUAGE=ru
   
   # Optional - API URL (default is used if not set)
   FACTS_API_URL=https://uselessfacts.jsph.pl/api/v2/facts
   
   # Optional - DeepL API Key for premium translation quality
   DEEPL_API_KEY=your_deepl_api_key_here
   ```

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
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
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
├── bot.py              # Main bot file
├── translations.py     # Interface translations
├── requirements.txt    # Python dependencies
├── config.env.example  # Configuration example
├── .env               # Environment variables file (create)
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
- Error handling

Logs are output to console with INFO level.

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

## 🔧 Configuration Options

### Environment Variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | - | Your Telegram bot token |
| `LANGUAGE` | ❌ No | `en` | Bot language (`en`/`ru`) |
| `FACTS_API_URL` | ❌ No | API URL | Facts API endpoint |
| `DEEPL_API_KEY` | ❌ No | - | DeepL API key for premium translation |

### Translation Priority:
1. **DeepL** (if API key provided)
2. **Google Translate** (fallback)
3. **Original text** (if translation fails)

## 🤝 Contributing

1. Fork the repository
2. Create a branch for new feature
3. Make changes
4. Create Pull Request

## 📄 License

This project is distributed under MIT license.

## 🔗 Useful Links

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [Useless Facts API](https://uselessfacts.jsph.pl/)
- [DeepL API](https://www.deepl.com/pro-api)
- [@BotFather](https://t.me/BotFather) - Telegram bot creation 
