import time
from datetime import datetime as dt

hosts_temp = "hosts"
hosts_path = r"C:\Windows\System32\drivers\etc"
redirect = "127.0.0.1"
websites_list = ["www.facebook.com","facebook.com"] # cada site listado aqui irá add uma linha no documento host
													# que impedirá acessar o respectivo site

inicio_exped = 8
fim_exped = 16

while True:

	if dt(dt.now().year, dt.now().month, dt.now().day, inicio_exped) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, fim_exped):
	# se estiver em horário de trabalho, executa-se o trecho do if
		with open(hosts_path, 'r+') as file:
			content = file.read() # lê o conteúdo do doc hosts
			for website in websites_list:
				if website in content: # se o site já estiver no doc hosts, quer dizer que já está bloqueado
					pass			   # continua execução sem fazer nada
				else:
					file.write(redirect + " " + website + "\n")

	else:
	# em horário de folga
		with open(hosts_path, 'r+') as file:
			content = file.read() # lê o conteúdo do doc hosts
			file.seek(0) # leva o ponteiro de leitura para o começo do doc hosts
			# vamos criar um novo doc hosts verificando se os nomes bloqueados estão naquela linha:
			#	caso sim: ignoramos a linha
			#	caso não: escrevemos aquela linha no novo doc
			for line in content:
				if not any(website in line for website in websites_list):
					file.write(line)

	time.sleep(5)