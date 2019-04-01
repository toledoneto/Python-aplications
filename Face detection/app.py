import cv2

# haarcascade_frontalface é um arqv xml que define dimensões de faces
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# usamos o 2º parâmetro 0 para pegar a img em tons de cinza, fazendo o cv2 ser mais preciso
# img = cv2.imread("photo.jpg")
img = cv2.imread("photo2.png")

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# scaleFactor muda em 5% a escala para procurar rostos, fazendo o programa tentar achar rostos maiores até acabar a img
faces = face_cascade.detectMultiScale(gray_img, scaleFactor = 1.001, minNeighbors = 1)

# desenhando o retângulo
for x, y, w, h in faces:
	img = cv2.rectangle(img, # arquivo de img
						(x,y), # ponto de início do retângulo
						(x+w, y+h), # limites do ret
						(0, 255, 0), # cor do ret
						3 # espessura do ret
						)

# resized = cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3)))

# cv2.imshow("Gray", resized)
cv2.imshow("Gray", img)
cv2.waitKey(0)
cv2.destroyAllWindows()