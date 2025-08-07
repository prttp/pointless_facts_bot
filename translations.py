# -*- coding: utf-8 -*-
"""
Translation system for the bot interface
"""

import logging

logger = logging.getLogger(__name__)

# Interface text translations
INTERFACE_TEXTS = {
    'en': {
        'welcome': "Hello! I'm a bot for getting useless facts!",
        'available_commands': "Available commands:",
        'random_command': "/random - get a random fact",
        'today_command': "/today - get today's fact", 
        'help_command': "/help - show help",
        'use_buttons': "Or use the buttons below:",
        'help_title': "**Bot Usage Guide:**",
        'commands_section': "**Commands:**",
        'language_section': "**Language:**",
        'language_info': "• Facts are provided in English",
        'random_fact_title': "**Random Fact:**",
        'today_fact_title': "**Today's Fact:**",
        'error_getting_fact': "❌ Error getting fact:",
        'error_getting_today_fact': "❌ Error getting today's fact:",
        'unexpected_error': "❌ Unexpected error occurred",
        'fact_not_found': "Fact not found",
        'today_fact_not_found': "Today's fact not found",
        'random_fact_button': "Random Fact",
        'today_fact_button': "Today's Fact"
    },
    'ru': {
        'welcome': "Привет! Я бот для получения бесполезных фактов!",
        'available_commands': "Доступные команды:",
        'random_command': "/random - получить случайный факт",
        'today_command': "/today - получить факт дня",
        'help_command': "/help - показать справку",
        'use_buttons': "Или используйте кнопки ниже:",
        'help_title': "**Справка по использованию бота:**",
        'commands_section': "**Команды:**",
        'language_section': "**Язык:**",
        'language_info': "• Факты переведены с английского языка",
        'random_fact_title': "**Случайный факт:**",
        'today_fact_title': "**Факт дня:**",
        'error_getting_fact': "❌ Ошибка при получении факта:",
        'error_getting_today_fact': "❌ Ошибка при получении факта дня:",
        'unexpected_error': "❌ Произошла непредвиденная ошибка",
        'fact_not_found': "Факт не найден",
        'today_fact_not_found': "Факт дня не найден",
        'random_fact_button': "Случайный факт",
        'today_fact_button': "Факт дня"
    }
}

def get_text(key, language='en'):
    """Get interface text in specified language"""
    return INTERFACE_TEXTS.get(language, INTERFACE_TEXTS['en']).get(key, key) 