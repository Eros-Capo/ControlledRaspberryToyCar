# coding-utf8
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(22,18)

while True:
   print('Distanza da oggetto più vicino', sensor.distance, 'm')
   sleep(1)

