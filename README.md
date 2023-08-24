# gpt-4-telegram-bot

Your own Telegram bot, powered by GPT-4. Configure and run within minutes!

## What you need

* A basic Python environment
* [API Key](https://platform.openai.com/account/api-keys) for OpenAI GPT-4
* Telegram [Web client](https://web.telegram.org/) or [app](https://telegram.org/apps) along with a [token for your bot](https://medium.com/geekculture/generate-telegram-token-for-bot-api-d26faf9bf064)

## 1 – Setup your environment

* You need a basic Python 3 environment, on your laptop or in the cloud. I use a $5/month Linux server on [Linode (referral link)](https://www.linode.com/lp/refer/?r=e9c9e6a878358178850c339672e1cfec564e4e0c) for that.
* Clone the repository: `git clone https://github.com/u1i/gpt-4-telegram-bot`
* Create a virtual Python env for your project: `cd gpt-4-telegram-bot; virtualenv $PWD`
* Activate the environment: `. ./bin/activate`
* Install the required Python libraries `pip3 install -r requirements.txt`

## 2 – Create your bot 'personality'

* Your bot will speak with humans, this could be just yourself as a start. Find a name that you like, and use the @botfather in Telegram to create a new bot – along with a profile picture, a description and [a token](https://medium.com/geekculture/generate-telegram-token-for-bot-api-d26faf9bf064). The token will look like this "6232091381:AAFdcgkKLN92BnPLYikFi5ZYCSQyAz76zXY"
* Edit the file `context.json` and describe the scenario, add instructions of what language to use, what to avoid, and the start of the conversation – this is, in essence, the prompt engineering that is passed into GPT-4 to set the context, the tone, and give the bot that 'personality' that you want.

## 3 – Add API key and telegram token to config file

* create a copy of the file `config.ini-example` and call it `config.ini`
* add your API key for OpenAI
* add your bot token from Telegram

## 4 – Start your bot

* Run this command: `python3 gpt-bot.py`

## 5 – Initiate a conversation and add your ID

* Chat up your bot in Telegram
* As a safety measure, users need to be whitelisted in order to chat with your bot. It should respond with a message like "Hi Joe – unfortunately, I have no idea who you are. Please tell your friendly human to add ID 446815934 to the list of allowed users. Once this is done please enter /start again."
* Edit the file `users.ini` and add this numeric ID to the list `allowed_users`. Specifially, add a "," (comma), followed by the ID. No blank spaces.
* In Telegram `/start` your conversation again. The bot should now recognize you!

![](bot.jpg)