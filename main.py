#!/usr/bin/env python3

from sense_hat import SenseHat
import time    
import csv
import datetime

sense = SenseHat()
sense.clear()
sense.set_imu_config(True, True, True)
counter = 0

with open('data.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Zeit','Temperatur', 'Druck', 'Luftfeuchtigkeit', 'Orientierung (Degrees)', 'Kompass (Norden)', 'Beschl. X', 'Beschl. Y', 'Beschl. Z', 'Temperatur (Feuchtigkeit)', 'Druck 2', 'Luftfeuchtigkeit 2', 'Temparatur (Druck)'])

with open('acc.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Zeit','X','Y','Z'])

# Farben definieren
red = (255, 0, 0)
green = (0, 255, 0)

def writeToCsv(temp, press, hum, pos_deg, pos_comp, temp2, press2, humm2, temp3):
    with open('data.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([datetime.datetime.now(),temp, press, hum, pos_deg, pos_comp, temp2, press2, humm2, temp3])
    print('data geschrieben')
    
def writeAccelerationToCsv(x,y,z):
    with open('acc.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([datetime.datetime.now(),x,y,z])
    print('acc geschrieben')
    
def main():
    try:
        while True:
            print('t')
            #Region Acceleration
            tempp = 2/0
            acceleration = sense.get_accelerometer_raw()
            acc_x = acceleration['x']
            acc_y = acceleration['y']
            acc_z = acceleration['z']
            writeAccelerationToCsv(acc_x,acc_y,acc_z)
            time.sleep(.250)
            counter+=1
            
            #Region Data
            if(counter == 4):
                temp = sense.get_temperature()
                press = sense.get_pressure()
                hum = sense.get_humidity()   
                pos_deg = sense.get_orientation_degrees()
                temp2 = sense.get_temperature_from_humidity()
                temp3 = sense.get_temperature_from_pressure()
                press2 = 0
                humm2 = 0        
                comp = sense.compass
                writeToCsv(temp, press, hum, pos_deg, comp, temp2, press2, humm2, temp3)
                counter = 0;
    except Exception as e:
        with open('log.csv', mode='a') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([datetime.datetime.now(),str(e)])
    finally:
        pass
        main()
    
if __name__ == '__main__':
    main()