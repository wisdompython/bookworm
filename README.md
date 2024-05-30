# Bookworm Project

Bookworm is a Document-Based Q&A solution designed to work with Telegram bots. It leverages retrieval augmented generation (RAG) combined with llama-index to read documents and provide accurate answers to user queries. This bot helps users get the information they need from any document quickly and efficiently.


 

## Progress

So far, the following features have been implemented:

1. Simple authentication system with Django.
2. Process to create custom bot instances.
3. Collection and data source creation process.
4. Endpoint to start the bot.


### Prerequisites

- [Python3](https://www.python.org/)
- [Django](https://www.djangoproject.com/)

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [llama-index](https://docs.llamaindex.ai/en/stable/)

## How to run
 - clone this repo
 - get your bot api_key from [botfather](https://t.me/BotFather)

 - run : ``` python manage.py runserver ```
 - register via postman on ```http://localhost:8000/register```
 - login to get access token ```http://localhost:8000/login```
 - create collection ```http://localhost:8000/collection/```
 - add a datasource to collection ```http://localhost:8000/create_datasource/```
 - create a bot instance on db ```http://localhost:8000/bot/```
 - start bot ``` http://localhost:8000/startbot/```
 - interact with bot on telegram
