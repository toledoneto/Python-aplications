import json
import difflib
from difflib import SequenceMatcher # usado para achar seq de char para sugestões de buscas
from difflib import get_close_matches # usado para achar seq de char para sugestões de buscas

data = json.load(open("data.json",'r')) # carrega o arquivo json com as palavras

# mostra que o tipo de dados é um dicionário
# print(type(data))

def translate(word):
	
	word = word.lower() # coloca tudo em minúscula como o programa exige

	# varificando se a palavra está nos dados
	if word in data:
		return data[word]
	elif w.title() in data: #if user entered "texas" this will check for "Texas" as well.
        return data[w.title()]
    elif w.upper() in data: #in case user enters words like USA or NATO
        return data[w.upper()]
	elif len(get_close_matches(word, data.keys())) > 0:
		yn = input("Did you mean -> %s <- instead? Enter Y for yes or N for no: " % get_close_matches(word, data.keys())[0])
		yn = yn.upper()
		if yn == "Y":
			return data[get_close_matches(word, data.keys())[0]]
		elif yn == "N":
			return "The word doesn't exist. Please double check it!"
		else:
			return "We didn't understand you entry."
	else:
		return "The word doesn't exist. Please double check it!"

word = input("Enter word: ")

output = translate(word)

if type(output) == list:
	for item in output:
		print item
else:
	print(output)