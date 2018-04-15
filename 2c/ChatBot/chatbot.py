from flask import Flask, request, render_template
import urllib
import json
import codecs
import random
import coinmarketcap

app = Flask(__name__)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
recentMessages = []

from coinmarketcap import Market
coinmarketcap = Market()

follow_up = []

currencies = {"BITCOIN": {"ticker": "Bitcoin", "shortTicker": " BTC"}, "ETHER": {"ticker": "Ethereum", "shortTicker": " ETH"}, "LITECOIN": {"ticker": "Litecoin", "shortTicker": " LTC"}, "MONERO": {"ticker": "Monero", "shortTicker": " XMR"}}

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@app.route('/')
def my_form():
    return render_template('input-form.html')

########## When input-form.html gets an input, this method makes sure that the input gets processed and then calls makes input-form.html print the bot's response.
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    recentMessages.append(['you', text.upper()])
    processedText = process(text.upper())
    recentMessages.append(['bot', processedText])
    return render_template('input-form.html', recentMessages = recentMessages)

def process(text):
	if len(follow_up) != 0:
		if follow_up[0][0] == "currency_request":
			return currencyRequest(text)
	greeting = isGreeting(text)
	if greeting != None:
		return greeting
	currencyPrice = isPriceRequest(text)
	if currencyPrice != None:
		return currencyPrice
	currency_request = isCurrencyRequest(text)
	if currency_request != None:
		return currency_request
	else:
		return "WHAT YOU ARE SAYING DOESN'T MAKE SENSE TO MY HUMBLE BRAIN."

########## GREETINGS  ##########
basic_greetings = ["HEY", "HEY, MAN", "HI", "HELLO"] #Should return a similar response
polite_greetings = ["GOOD TO SEE YOU", "NICE TO SEE YOU", "IT'S NICE TO MEET YOU", "PLEASED TO MEET YOU"] #Should return an equal response, but with "TOO" added to the end.
nostalgic_greetings = ["LONG TIME NO SEE", "IT'S BEEN A WHILE"] #Should return a similar response
question_greetings = ["WHAT'S UP", "WHAT's NEW", "WHAT'S GOING ON"] #Questions to which the answer is "I'M A BOT, SO NOT MUCH"
personal_question_greetings = ["HOW'S IT GOING", "HOW ARE YOU", "HOW'RE YOU", "HOW'S EVERYTHING", "HOW ARE THINGS", "HOW'S LIFE", "HOW'S YOUR DAY", "HOW'S YOUR DAY GOING", "HOW HAVE YOU BEEN", "HOW DO YOU DO", "HIYA"] #Questions to which the answer is "FINE, THANK YOU"
time_greetings = ["GOOD MORNING", "GOOD AFTERNOON", "GOOD EVENING"] #Should return an equal response
yes_no_question_greetings = ["ARE YOU OK", "YOU ALRIGHT", "ALRIGHT MATE"] #Should return "YES"
slang_greetings = ["YO", "HOWDY", "SUP", "WHAZZUP", "G'DAY"] #Should return an equal response

def isGreeting(text):
	for greeting in basic_greetings:
		if greeting in text and "THING" not in text:
			return random.choice(basic_greetings) + "."
	for greeting in polite_greetings:
		if greeting in text:
			return greeting + "TOO."
	for greeting in nostalgic_greetings:
		if greeting in text:
			return random.choice(nostalgic_greetings) + "."
	for greeting in question_greetings:
		if greeting in text:
			return "I'M A BOT, SO NOT MUCH."
	for greeting in personal_question_greetings:
		if greeting in text:
			return "I'M FINE, THANK YOU."
	for greeting in time_greetings:
		if greeting in text:
			return greeting + "."
	for greeting in yes_no_question_greetings:
		if greeting in text:
			return "YES."
	for greeting in slang_greetings:
		if greeting in text:
			return greeting + "."
	return None

########## CURRENCY PRICES ##########
def isPriceRequest(text):
	if "PRICE" in text:
		for currency in currencies:
			if currency in text or currencies[currency]["shortTicker"] in text:
				if "AUD" in text or "AUSTRALIAN DOLLAR" in text or "CAYMAN ISLANDS DOLLAR" in text or "DINAR" in text or "FRANK" in text or "GBP" in text or "KRONE" in text or "POUND" in text or "RIAL" in text or "YEN" in text:
					return "I'M NOT SURE, BUT FOR WHAT IT'S WORTH, THE CURRENT US DOLLAR PRICE OF " + currency + " IS $" + str(getPrice(currencies[currency]["ticker"], "price_usd")) + "."
				elif "EUR" in text:
					return "THE CURRENT PRICE OF " + currency + " IS £" + str(getPrice(currencies[currency]["ticker"], "price_eur")) + "."
				elif "USD" in text or "DOLLAR" in text:
					return "THE CURRENT PRICE OF " + currency + " IS $" + str(getPrice(currencies[currency]["ticker"], "price_usd")) + "."
				else:
					return "THE CURRENT PRICE OF " + currency + " IS $" + str(getPrice(currencies[currency]["ticker"], "price_usd")) + "."
		return None

def isCurrencyRequest(text):
	for currency in currencies:
			if currency in text or currencies[currency]["shortTicker"] in text:
				if ("PRICE" not in text and "MARKETCAP" not in text and "MARKET CAP" not in text):
					follow_up.append(["currency_request", currency])
					return "WHAT DO YOU WANT TO KNOW ABOUT " + currency + "?"
	return None

def currencyRequest(text):
	currency = follow_up[0][1]
	return_string = ""
	if "PRICE" in text:
		if "AUD" in text or "AUSTRALIAN DOLLAR" in text or "CAYMAN ISLANDS DOLLAR" in text or "DINAR" in text or "FRANK" in text or "GBP" in text or "KRONE" in text or "POUND" in text or "RIAL" in text or "YEN" in text:
			return_string += "I'M NOT SURE, BUT FOR WHAT IT'S WORTH, THE CURRENT US DOLLAR PRICE OF " + currency + " IS $" + str(getPrice(currencies[currency]["ticker"], "price_usd")) + ". "
		elif "EUR" in text:
			return_string += "THE CURRENT PRICE OF " + currency + " IS £" + str(getPrice(currencies[currency]["ticker"], "price_eur")) + ". "
		elif "USD" in text or "DOLLAR" in text:
			return_string += "THE CURRENT PRICE OF " + currency + " IS $" + str(getPrice(currencies[currency]["ticker"], "price_usd")) + ". "
		else:
			return_string += "THE CURRENT PRICE OF " + currency + " IS $" + str(getPrice(currencies[currency]["ticker"], "price_usd")) + ". "
	if "MARKETCAP" in text or "MARKET CAP" in text:
		if "AUD" in text or "AUSTRALIAN DOLLAR" in text or "CAYMAN ISLANDS DOLLAR" in text or "DINAR" in text or "FRANK" in text or "GBP" in text or "KRONE" in text or "POUND" in text or "RIAL" in text or "YEN" in text:
			return_string += "I'M NOT SURE, BUT FOR WHAT IT'S WORTH, THE CURRENT US DOLLAR MARKET CAPITALIZATION OF " + currency + " IS $" + str(getPrice(currencies[currency]["ticker"], "market_cap_usd")) + "."
		elif "EUR" in text:
			return_string += "THE CURRENT MARKET CAPITALIZATION OF " + currency + " IS £" + str(getPrice(currencies[currency]["ticker"], "market_cap_eur")) + "."
		elif "USD" in text or "DOLLAR" in text:
			return_string += "THE CURRENT MARKET CAPITALIZATION OF " + currency + " IS $" + str(getPrice(currencies[currency]["ticker"], "market_cap_usd")) + "."
		else:
			return_string += "THE CURRENT MARKET CAPITALIZATION OF " + currency + " IS $" + str(getPrice(currencies[currency]["ticker"], "market_cap_usd")) + "."
	if len(return_string) == 0:
		return_string += "I'M NOT SURE IF I UNDERSTAND WHAT YOU WANT TO KNOW ABOUT " + currency + ", BUT ANYWAYS, " + currency + "'S CURRENT PRICE IS $" + str(getPrice(currencies[currency]["ticker"], "price_usd")) + " AND ITS CURRENT MARKET CAPITALIZATION IS $" +  str(getPrice(currencies[currency]["ticker"], "market_cap_usd")) + "."
	for element in follow_up:
		follow_up.remove(element)
	return return_string

def getPrice(cryptoCurrency, fiatCurrency = None):
	success = False
	while success == False: #Sometimes the CoinmarketCap API is a bit unreliable.
		try:
			return float(coinmarketcap.ticker(cryptoCurrency, limit=3, convert = 'EUR')[0][fiatCurrency])
		except:
			pass

if __name__ == "__main__":
	app.run(debug=True)