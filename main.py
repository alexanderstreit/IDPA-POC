#!/usr/bin/env python3

from sense_hat import SenseHat
import time    
import csv

sense = SenseHat()
sense.clear()
sense.set_imu_config(True, True, True)

with open('data.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Temperatur', 'Druck', 'Luftfeuchtigkeit', 'Orientierung (Degrees)', 'Kompass (Norden)', 'Beschl. X', 'Beschl. Y', 'Beschl. Z', 'Temperatur (Feuchtigkeit)', 'Druck 2', 'Luftfeuchtigkeit 2', 'Temparatur (Druck)'])

# Farben definieren
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

def writeToCsv(temp, press, hum, pos_deg, pos_comp, acc_x, acc_y, acc_z, temp2, press2, humm2, temp3):
    with open('data.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([temp, press, hum, pos_deg, pos_comp, acc_x, acc_y, acc_z, temp2, press2, humm2, temp3])
    print('csv geschrieben')
        
while True:
    temp = sense.get_temperature()
    press = sense.get_pressure()
    hum = sense.get_humidity()
    acceleration = sense.get_accelerometer_raw()
    acc_x = acceleration['x']
    acc_y = acceleration['y']
    acc_z = acceleration['z']
    
    pos_deg = sense.get_orientation_degrees()
    temp2 = sense.get_temperature_from_humidity()
    temp3 = sense.get_temperature_from_pressure()
    press2 = 0
    humm2 = 0
    
    comp = sense.compass
    writeToCsv(temp, press, hum, pos_deg, comp, acc_x, acc_y, acc_z, temp2, press2, humm2, temp3)

