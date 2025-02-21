# FAQ Bot Plus

## Overview

**FAQ Bot Plus** is a conversational bot that provides answers to a set of predefined questions and answers. The bot uses fuzzy regular expressions to match user queries and identify the intent behind them. If the bot cannot determine the user's intent, it leverages spaCy's Named Entity Recognition (NER), noun chunks, and speech act classification to provide fallback responses, making the bot appear more human-like. The bot can also generate links to external resources like Google Maps and Wikipedia based on recognized entities.

The project consists of three phases:

1. **Phase 1**: Basic FAQ bot with fuzzy regex matching.
2. **Phase 2**: Advanced FAQ bot with spaCy integration for linguistic analysis and fallback responses.
3. **Phase 3**: A Discord bot implementation to make it interactive.

## Features

- **Fuzzy Regular Expression Matching**: The bot matches user queries with predefined question-answer pairs using fuzzy regex, allowing for some typo tolerance.
- **Named Entity Recognition (NER)**: The bot recognizes named entities (e.g., locations, organizations) using spaCy and offers relevant external links (Google Maps, Wikipedia).
- **Noun Chunk Recognition**: The bot identifies noun chunks when it cannot recognize the intent to provide more context-based fallback responses.
- **Speech Act Classification**: The bot classifies the user's intent (question, command, or statement) to provide appropriate responses.
- **Discord Integration**: The bot runs on Discord, providing FAQ responses directly in chat.

## Installation & Setup

### 1. Clone the repository

2. Install Dependencies
Make sure Python 3.x is installed, then install the required dependencies:

pip install -r requirements.txt
3. Set up spaCy
If spaCy is not already installed, install the English language model:

python -m spacy download en_core_web_sm
4. Add your Discord Bot Token
To keep your bot token secure, use GitHub Repository Secrets or environment variables. Do not hardcode your bot token directly in the code.

# In the terminal, set the token as an environment variable:
export DISCORD_TOKEN="your-bot-token"
5. Run the Bot
To start the bot, use the following command:

python discord_faq_bot.py

