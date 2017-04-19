#!/usr/bin/python

import sys
import time

from PIL import Image

from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

im = Image.open('mario.jpg')
small_im = im.resize((8, 8))

sense.set_pixels(list(small_im.getdata()))
rotation = 0

while True:
    temp = round(1.8 * sense.get_temperature() + 32, 1)
    print("Temperature: ", temp)

    humidity = sense.get_humidity()  
    humidity = round(humidity, 1)  
    print("Humidity :",humidity)  

    pressure = sense.get_pressure()
    pressure = round(pressure, 1)
    print("Pressure:",pressure)

    #sense.show_message(str(temp) + "F", scroll_speed=(0.05), text_colour=[0, 0, 200], back_colour= [0,0,0])

    time.sleep(.5)

    rotation = (rotation + 90) % 360
    sense.set_rotation(rotation)    

