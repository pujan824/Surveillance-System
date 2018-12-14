import cv2
from imutils.video.pivideosteam import PiVideoStream
import imutils
import time
import  numpy as np 

class Camera(object):
	def __init__(self, flip = False):
		self.vs = PiVideoStream().start()
		self.flip = flip 
		time.sleep(2.0)

	def __del__(self):
		self.vs.stop()

	def flip_if_needed(self, frame):
		if self.flip:
			return np.flip(frame,0)
		return frame

	def get_frame(self):
		frame = self.flip_if_needed(self.vs.read())
		ret, jpeg = cv2.imencode('.jpg',frame)
		return jpeg.tobytes()

	def get_object(self, classifier):
		found_object = False
		frame = self.flip_if_needed(self.vs.read()).copy()
		grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		objects = classifier.detectMultiScale(
			grey,
			scaleFactor = 1.1,
			minNeighbours = 5,
			minSize = (30,30),
			flags = cv2.CASCADE_SCALE_IMAGE
		)

		if len(objects) > 0:
			found_object = True
		
		for(x,y,w,h) in objects:
			cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

		ret, jpeg = cv2.imencode('.jpg', frame)
		return (jpeg.tobytes(), found_object)