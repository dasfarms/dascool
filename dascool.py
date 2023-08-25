#!/usr/bin/env python

import os
import glob
import time
import lib4relind as r
# uncomment for LCD when i get one
# from RPLCD import CharLCD
# lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])


def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20


def readf(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    fahrenheit = (temperature / 1000) * 1.8 + 32
    fahstr = str(round(fahrenheit, 1))
    return fahrenheit, fahstr


def readc(ds18b20):
    
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = int(temperature) / 1000
    celstr = str(round(celsius, 1))
    return celsius, celstr


def loop(ds18b20): 
        
    while True:

        if readf(ds18b20)[0] < 45 or readc(ds18b20)[0] < 8:
            r.set_relay(0, 0, 1)

        else:
            r.set_relay(0, 0, 0)


def kill():
    quit()
    

if __name__ == '__main__':
    
    r.set_relay_all(0, 0)
    
    try:
        serialNum = sensor()

        loop(serialNum)
#  ! !  !    UNCOMMENT FOR LCD  !  !   !
#        lcd.cursor_pos = (0, 0)
#        lcd.write_string("Temp: " + readc()[1] + unichr(223) + "C")
#        lcd.cursor_pos = (1, 0)
#        lcd.write_string("Temp: " + readf()[1] + unichr(223) + "F")

        time.sleep(300)

    except KeyboardInterrupt:
        kill()
        
