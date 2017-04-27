#!/usr/bin/python

import sys
import time

import six
from PIL import Image

from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

im = Image.open('mario.jpg')
small_im = im.resize((8, 8))

sense.set_pixels(list(small_im.getdata()))
rotation = 0

class LEDProgressBar(six.Iterator):

	def __init__(self, sense, items):	
		self.sense = sense
		sense.low_light = True	

		self.size = 64
		self._iter = 0

		self.sense.clear()

		self._items = iter(items)
		self._total = len(items)

	def __enter__(self):
		return self

	def __exit__(self):
		self.sense.clear()

	def __iter__(self):
		return self

	def __next__(self):
		try:
			rv = next(self._items)
		except StopIteration:
			self.__exit__()
			raise
		else:
			self.step()
			return rv

	def step(self):
		self._iter += 1

		pix = (float(self._iter) / self._total) * (self.size-1)
		x_pix = int(pix % 8)
		y_pix = pix // 8

		print(self._iter, x_pix, y_pix)
		self.sense.set_pixel(x_pix, y_pix, 0, 0, 10)


for item in LEDProgressBar(sense, range(500)):
    temp = round(1.8 * sense.get_temperature() + 32, 1)
    print("Temperature: ", temp)

    humidity = sense.get_humidity()  
    humidity = round(humidity, 1)  
    print("Humidity :",humidity)  

    pressure = sense.get_pressure()
    pressure = round(pressure, 1)
    print("Pressure:",pressure)

    #sense.show_message(str(temp) + "F", scroll_speed=(0.05), text_colour=[0, 0, 200], back_colour= [0,0,0])

    time.sleep(.1)

    #rotation = (rotation + 90) % 360
    #sense.set_rotation(rotation)    

