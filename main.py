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
    writer.writerow(['Zeit','Temperatur1', 'Temperatur2', 'Temperatur3', 'Luftdruck', 'Luftfeuchtigkeit', 'Yaw', 'Pitch', 'Roll', 'Compass X', 'Compass Y', 'Compass Z', 'Gyro X', 'Gyro Y', 'Gyro Z'])

with open('acc.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Zeit','Acc_X','Acc_Y','Acc_Z'])

# Farben definieren
red = (255, 0, 0)
green = (0, 255, 0)
black = (0,0,0)

def writeDataToCsv(temperature, temperature2, temperature3, pressure, humidty, yaw, pitch, roll, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z):
    with open('data.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([datetime.datetime.now(),temperature, temperature2, temperature3, pressure, humidty, yaw, pitch, roll, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z])
    print('data geschrieben')
    
def writeAccelerationToCsv(x,y,z):
    with open('acc.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([datetime.datetime.now(),x,y,z])
    print('acc geschrieben')
    
def main():
    try:
        while False:
            #Region Acceleration
            acceleration = sense.get_accelerometer_raw()
            acc_x = acceleration['x']
            acc_y = acceleration['y']
            acc_z = acceleration['z']
            writeAccelerationToCsv(acc_x,acc_y,acc_z)
            time.sleep(.250)
            counter+=1
            
            #Region Data
            if(counter == 4):                
                temperature = sense.get_temperature()
                temperature2 = sense.get_temperature_from_humidity()
                temperature3 = sense.get_temperature_from_pressure()
                
                pressure = sense.get_pressure()
                humidty = sense.get_humidity()
                
                orientation = sense.get_orientation()
                yaw = orientation["yaw"]
                pitch = orientation["pitch"]
                roll = orientation["roll"]
                
                mag = sense.get_compass_raw()
                mag_x = mag["x"]
                mag_y = mag["y"]
                mag_z = mag["z"]
                
                gyro = sense.get_gyroscope_raw()
                gyro_x = gyro["x"]
                gyro_y = gyro["y"]
                gyro_z = gyro["z"]
                
                writeDataToCsv(temperature, temperature2, temperature3, pressure, humidty, yaw, pitch, roll, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z)
                
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