#!/usr/bin/python

import datetime
import logging
logger = logging.getLogger(__name__)
import sys
import time

import numpy as np
import six
from PIL import Image

from sense_hat import SenseHat
from data_client.DataClient import DataClient

sense = SenseHat()
sense.clear()

#im = Image.open('mario.jpg')
#small_im = im.resize((8, 8))

#sense.set_pixels(list(small_im.getdata()))
#rotation = 0

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

        self.sense.set_pixel(x_pix, y_pix, 0, 0, 10)


def make_measurements(number=10, pause=.01):
    """Perform measurements over a time-range to make a composite measurement

    Parameters
    ----------
    number: int, optional
        Number of sub-measurements to make.
    pause: float, int, optional
        Number of seconds to pause between measurements..

    Returns
    -------
    stats: dict
        composite measurements.
    """

    stats = {"temperature": [],
             "humidity": [],
             "pressure": []
             }

    count = 0
    while count < number:
        stats["temperature"].append(round(1.8 * sense.get_temperature() + 32, 2))
        stats["humidity"].append(round(sense.get_humidity(), 2))
        stats["pressure"].append(round(sense.get_pressure(), 2))

        count += 1
        time.sleep(pause)

    for key in stats:
        stats[key] = np.mean(stats[key])

    return stats


logging.basicConfig(filename="/home/pi/codebase/raspberry_weather/weather_monitor.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

for item in LEDProgressBar(sense, range(100)):

    now = str(datetime.datetime.now())
    stats = make_measurements(10, .05)

    logger.info("temp: {}".format(stats["temperature"]))
    logger.info("humidity: {}".format(stats["humidity"]))
    logger.info("pressure: {}".format(stats["pressure"]))

    #sense.show_message(str(temp) + "F", scroll_speed=(0.05), text_colour=[0, 0, 200], back_colour= [0,0,0])

    time.sleep(1)

    #rotation = (rotation + 90) % 360
    #sense.set_rotation(rotation)    

certdir = '/home/pi/go/src/github.com/deciphernow/gm-data-fabric/pki/'
d = DataClient("https://192.168.1.5", 8080, certdir + 'server.cert.pem',
               certdir + 'server.key.pem', False,
               "C=US,ST=Virginia,L=Alexandria,O=Decipher Technology Studios,OU=Engineering,CN=localuser", "0din",
               logfile="pi_data_test.log")

d.upload_file("weather_monitor.log", "/files/weather_monitor.log")

