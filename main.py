#!/usr/bin/env python3

from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

# Farben definieren
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

while False:
	acceleration = sense.get_accelerometer_raw()
	x = acceleration['x']
	y = acceleration['y']
	z = acceleration['z']

	x = abs(x)
	y = abs(y)
	z = abs(z)

	if x > 2 or y > 2 or z > 2:
		sense.show_letter("!", red)
	else:
		sense.clear()

#print()
#print("Luftfeuchtigkeit:")
#humidity = sense.get_humidity()
#print(humidity)

while True:
	print()
	print("Temperatur:")
	temp = sense.get_temperature()
	print(temp)

	print()
	print("Druck:")
	pressure = sense.get_pressure()
	print(pressure)

	print()
	print("Luftfeuchtigkeit:")
	humidity = sense.get_humidity()
	print(humidity)

	sense.set_rotation(180)
	sense.show_message("%.1f degree" % temp, scroll_speed=0.01, text_colour=blue)
	sense.show_message("%.1f ke ahnig" % pressure, scroll_speed=0.01, text_colour=green)
	sense.show_message("%.1f percent" % humidity, scroll_speed=0.01, text_colour=red)
