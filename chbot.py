import telebot
import apiai, json

bot = telebot.TeleBot('Хэш вашего бота')

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

@bot.message_handler(content_types=['text'])
def send_text(message):
	import dialogflow_v2 as dialogflow	
	session_client = dialogflow.SessionsClient.from_service_account_file('./key.json') #путь к хэшу вашего аккаунта DialogFlow
	session = session_client.session_path('Имя сессии', 'Номер сессии')
	print('Session path: {}\n'.format(session))
	text_input = dialogflow.types.TextInput(
		text=message.text, 
		language_code='ru')
	query_input = dialogflow.types.QueryInput(text=text_input)
	response = session_client.detect_intent(
		session=session, query_input=query_input)
	if response:
		bot.send_message(message.chat.id, response.query_result.fulfillment_text)
	else:
		bot.send_message(message.chat.id, 'Я Вас не совсем понял...')
	
bot.polling()
