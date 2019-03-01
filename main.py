#!/usr/bin/env python3

from sense_hat import SenseHat
import time
import csv
import datetime

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

class DataLogger(object):
    
    def __init__(self, init_csv_files=False):
        # initalize the commonly ued sensor
        self.sense = SenseHat()
        self.sense.clear()
        self.sense.set_imu_config(True, True, True)
        self.sense.low_light = True
        self.data_list = []
        self.acceleration_list = []

        # only initialize the csv files if intended
        if init_csv_files:
            self.init_csv_files()

    def write_data_to_file(self, data, file_name, mode='a', delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL):
        with open(file_name, mode=mode) as file:
            writer = csv.writer(file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
            for row in data:
                writer.writerow(row)
        
        self.sense.set_pixel(0, 0, GREEN)
        time.sleep(.05)
        self.sense.set_pixel(0, 0, BLACK)


    def init_csv_files(self):
        self.sense.set_pixel(0, 1, GREEN)
        self.sense.set_pixel(0, 0, GREEN)
        time.sleep(.1)
        self.sense.set_pixel(0, 1, BLACK)
        self.sense.set_pixel(0, 0, BLACK)
    
        delimiter=';'
        quotechar='"'
        quoting=csv.QUOTE_MINIMAL
        
        # see comment in init method
        data_headings = ['Zeit','Temperatur1', 'Temperatur2', 'Temperatur3', 'Luftdruck', 'Luftfeuchtigkeit', 'Yaw', 'Pitch', 'Roll', 'Compass X', 'Compass Y', 'Compass Z', 'Gyro X', 'Gyro Y', 'Gyro Z']
        with open('data.csv', 'w') as file:
            writer = csv.writer(file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
            writer.writerow(data_headings)

        acc_headings = ['Zeit','Acc_X','Acc_Y','Acc_Z']
        with open('acc.csv', 'w') as file:
            writer = csv.writer(file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
            writer.writerow(acc_headings)

        log_headings = ['Zeit','Fehler']
        with open('log.csv', 'w') as file:
            writer = csv.writer(file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
            writer.writerow(log_headings)

    def start_logging(self):
        # actual execution
        self.sense.set_pixel(0, 0, BLACK)
        counter = 0

        while True:
            self.log_accelleration()
            time.sleep(.250)
            counter += 1

            # using counter % 4 == 0 instead of counter == 4
            if(counter % 4 == 0):
                self.log_data()
                counter = 0

    def log_accelleration(self):
        acceleration_data = self.get_accelleration()
        self.acceleration_list.append(acceleration_data)
        if len(self.acceleration_list) % 10 == 0:
            try:
                self.write_data_to_file(self.acceleration_list, 'acc.csv')
                self.acceleration_list = []
            except Exception as e:
                self.log_exception(e)
                pass

    def log_data(self):
        # saving datetime first, before reading all the sensor data
        data = [datetime.datetime.now()]

        data += self.get_temperature()
        data += self.get_pressure()
        data += self.get_humidity()
        data += self.get_orientation()
        data += self.get_mag()
        data += self.get_gyro()
        
        self.sense.set_pixel(0, 1, BLUE)
        time.sleep(.05)
        self.sense.set_pixel(0, 1, BLACK)
        
        self.data_list.append(data)
        if len(self.data_list) % 10 == 0:
            try:
                self.write_data_to_file(self.data_list, 'data.csv')
                self.data_list = []
            except Exception as e:
                self.log_exception(e)
                pass

    def log_exception(self, exception):
        self.sense.set_pixel(1, 0, RED)
        row = []
        row.append([str(datetime.datetime.now()), str(exception)])
        self.write_data_to_file(row, 'log.csv')
        self.sense.set_pixel(0, 0, BLACK)

    def get_accelleration(self):
        try: 
            acceleration = self.sense.get_accelerometer_raw()
            acc_x = acceleration['x']
            acc_y = acceleration['y']
            acc_z = acceleration['z']
            self.sense.set_pixel(0, 1, BLUE)
            time.sleep(.05)
            self.sense.set_pixel(0, 1, BLACK)
        except Exception as e:
            self.log_exception(e)
            acc_x = '-'
            acc_y = '-'
            acc_z = '-'
            pass            
        return[datetime.datetime.now(), acc_x, acc_y, acc_z]

    def get_temperature(self):
        try:
            temperature1 = self.sense.get_temperature()
        except Exception as e:
            self.log_exception(e)
            temperature1 = '-'
            pass
        try:
            temperature2 = self.sense.get_temperature_from_humidity()
        except Exception as e:
            self.log_exception(e)
            temperature2 = '-'
            pass
        try:
            temperature3 = self.sense.get_temperature_from_pressure()
        except Exception as e:
            self.log_exception(e)
            temperature3 = '-'
            pass
        finally:
            return [temperature1, temperature2, temperature3]

    def get_pressure(self):
        try:
            pressure = self.sense.get_pressure()
        except Exception as e:
            self.log_exception(e)
            pressure = '-'
        finally:     
            return [pressure]

    def get_humidity(self):
        try:
            humidty = self.sense.get_humidity()
        except Exception as e:
            self.log_exception(e)
            humidty = '-'
        finally:     
            return [humidty]

    def get_orientation(self):       
        try:
            orientation = self.sense.get_orientation()
            yaw = orientation["yaw"]
            pitch = orientation["pitch"]
            roll = orientation["roll"]
        except Exception as e:
            self.log_exception(e)
            yaw = '-'
            pitch = '-'
            roll = '-'
        finally:  
            return [yaw, pitch, roll]

    def get_mag(self):
        try:
            mag = self.sense.get_compass_raw()
            x = mag["x"]
            y = mag["y"]
            z = mag["z"]
        except Exception as e:
            self.log_exception(e)
            x = '-'
            y = '-'
            z = '-'
        finally:
            return [x, y, z]

    def get_gyro(self):
        try:
            gyro = self.sense.get_gyroscope_raw()
            x = gyro["x"]
            y = gyro["y"]
            z = gyro["z"]
        except Exception as e:
            self.log_exception(e)
            x = '-'
            y = '-'
            z = '-'
        finally:  
            return [x, y, z]


if __name__ == '__main__':
    data_logger = DataLogger(init_csv_files=True)
    try:
        data_logger.start_logging()
    except Exception as e:
        data_logger.log_exception(e)