#!/usr/bin/env python

import logging, os, openai, uuid, configparser, json
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Read config.ini and context.ini
config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config.get('openai', 'api_key')
telegram_token = config.get('telegram', 'token')

with open('context.json', 'r') as json_file:
    start_convo = json.load(json_file)

completion = openai.Completion()

def is_this_user_allowed(user_id):
    whitelist = configparser.ConfigParser()
    whitelist.read('users.ini')
    users_str = whitelist.get('whitelist', 'allowed_users')
    users = users_str.split(",")
    if str(user_id) in users:
        return True
    else:
        return False    

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_convo
    prompt = chat_log + [{"role": "user", "content": question}]
    try:
        response = openai.ChatCompletion.create(model="gpt-4", messages= prompt)
        answer = response.choices[0].message.content.strip()
    except:
        answer = "Sorry. Some error occured. Probably a rate limit or something..."
    return answer

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_convo
    return chat_log + [ {"role": "user", "content": question}, {"role": "assistant", "content": answer}]

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:

	user = update.effective_user
	user_id=user["id"]
	username=user["username"]

	if is_this_user_allowed(user_id) == False:
		update.message.reply_text('Hi ' + str(user.first_name) + ' – unfortunately, I have no idea who you are. Please tell your friendly human to add ID ' +str(user_id) + ' to the list of allowed users. Once this is done please enter /start again.')
		logger.info("Unauthorized chat request from %s", username)
		return

	context.user_data['chat_log'] = None
	context.user_data['sessionid'] = str(uuid.uuid4())
	update.message.reply_text('Hi, ' + str(user.first_name) + " what's up?")
	logger.info("New session with  %s", username)

def talk(update: Update, context: CallbackContext) -> None:

	user = update.effective_user
	user_id=user["id"]
	username=user["username"]

	try:
		dummy = context.user_data['chat_log']
	except:
		return
		
	q = update.message.text
	logger.info("%s said: %s", username, q)

	a = ask(q, context.user_data['chat_log'])

	context.user_data['chat_log'] = append_interaction_to_chat_log(q,a, context.user_data['chat_log'])
	update.message.reply_text(a)

	logger.info("AI response to %s: %s", username, a)
	sessionid = context.user_data['sessionid']

def main() -> None:

    # Create the Updater and pass it your bot's token.
    updater = Updater(telegram_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, talk))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
