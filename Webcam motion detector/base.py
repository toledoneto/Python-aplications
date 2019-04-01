import cv2, time
from datetime import datetime
import pandas as pd

first_frame = None
status_list = [None, None] # marca o momento de virada de status de 0 pra 1 e vice versa
times = [] # armazena qdo ocorreram as mudanças de status
df = pd.DataFrame(columns = ["Start", "End"])

video = cv2.VideoCapture(0)

while True:
	check, frame = video.read()

	status = 0 # diz se está havendo movimento ou n
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21,21), 0) # melhorando a precisão com esse passo

	# capturando o 1º frame da câmera para checar se há movimento posterior
	if first_frame is None:
		first_frame = gray
		continue # envia para o começo do loop

	delta_frame = cv2.absdiff(first_frame, gray)
	thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
	thresh_frame = cv2.dilate(thresh_frame, 
		None, # array de câmeras
		iterations = 2 # qto maior, melhor a img será
		)

	(_, cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in cnts:
		if cv2.contourArea(contour) < 1000:
			continue
		status = 1
		(x, y, w, h) = cv2.boundingRect(contour)
		cv2.rectangle(frame, # arquivo de img
						(x,y), # ponto de início do retângulo
						(x+w, y+h), # limites do ret
						(0, 255, 0), # cor do ret
						3 # espessura do ret
						)

	status_list.append(status)

	status_list = status_list[-2:] # salvando apenas as duas útlimas entradas para economizar espaço na memória

	if status_list[-1] == 1 and status_list[-2] == 0:
		times.append(datetime.now())
	if status_list[-1] == 0 and status_list[-2] == 1:
		times.append(datetime.now())

	#cv2.imshow("Capturing", gray)
	cv2.imshow("Delta Frame", delta_frame)
	cv2.imshow("Threshold Frame", thresh_frame)
	cv2.imshow("Color Frame", frame)

	key = cv2.waitKey(1) # tempo em ms que a câmera irá capturar frames

	if key == ord('q'):
		if status == 1:
			times.append(datetime.now())
		break

for i in range(0, len(times), 2):
	df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index = True)

df.to_csv("Times.csv") # salva os dados recebidos em um arqv csv

video.release()
cv2.destroyAllWindows