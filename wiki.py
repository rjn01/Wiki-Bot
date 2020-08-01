import wikipedia

def search(user_input):
	try:
		send = wikipedia.summary(user_input, sentences = 5)
	except:
		#send = wikipedia.search(user_input)
		send = "No Results Found"
	return send

