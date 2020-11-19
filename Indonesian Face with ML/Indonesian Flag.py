import cv2

def detectFaces(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	face = cv2.CascadeClassifier('face2.xml')
	faceM = face.detectMultiScale(gray, 1.1, 5)
	for x,y,w,h in faceM:
		halfH = h//2
		cv2.rectangle(image, (x,y), (x+w, y+halfH), (10,10,250), -1)
		cv2.rectangle(image, (x,y+halfH), (x+w, y+h), (255,255,255), -1)
		cv2.putText(image, ('MERDEKA!!!!'), (x, y-20), cv2.FONT_HERSHEY_COMPLEX, 2, (10,10,255),1)
	return image

cap = cv2.VideoCapture(1)

while cap.isOpened:
	ret, frame = cap.read()
	frame = detectFaces(frame)
	cv2.imshow('anjay',frame)

	if cv2.waitKey(1) & 0xFF==ord('q'):
		break

cap.release()
cv2.destroyAllWindows()