# 🤖 Telegram Bot for Useless Facts

Telegram bot that fetches useless facts via HTTP API and sends them to users.

## 🚀 Features

- Get random useless facts
- Get today's fact
- English language support
- Interactive buttons for easy use
- Error handling and logging

## 📋 Requirements

- Python 3.8+
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
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
   - Fill in `TELEGRAM_BOT_TOKEN` with your bot token

   ```bash
   cp config.env.example .env
   ```

4. **Edit the `.env` file:**
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   FACTS_API_URL=https://uselessfacts.jsph.pl/api/v2/facts
   ```

## 🚀 Running

```bash
python bot.py
```

## 📱 Usage

### Bot Commands:

- `/start` - Start working with the bot
- `/help` - Show help
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
├── requirements.txt    # Python dependencies
├── config.env.example  # Configuration example
├── .env               # Environment variables file (create)
└── README.md          # Documentation
```

## 🔒 Security

- Never publish your `TELEGRAM_BOT_TOKEN`
- Add `.env` to `.gitignore`
- Use HTTPS for API requests

## 🐛 Logging

The bot logs all operations. Logs are output to console with INFO level.

## 📝 Response Examples

### Random Fact:
```
**Random Fact:**

Bananas are berries, but strawberries aren't.
```

### Today's Fact:
```
**Today's Fact:**

Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.
```

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
- [@BotFather](https://t.me/BotFather) - Telegram bot creation 
