# coding=utf-8
from gpiozero import PWMOutputDevice
from time import sleep

MotorA = PWMOutputDevice(9)
MotorB = PWMOutputDevice(11)
#Definizione funzioni
def forwardMotor():
   MotorA.value=0;
   MotorB.value=0;

def backwardMotor():
   MotorA.value=1;
   MotorB.value=1;

def rightMotor():
   MotorA.value=0;
   MotorB.value=1;

def leftMotor():
   MotorA.value=1;
   MotorB.value=0;

#Main
while 1:
   a=raw_input("What do you wanna do? 1 Forward 2 Backward 3 Right 4 Left 5 Shutdown");
   if a == "1":
      print("Going foreward!");
      forwardMotor();
      sleep();
   elif a == "2":
      print("Going backward!");
      backwardMotor();
      sleep(2)
   elif a == "3":
      print("Turning right!");
      rightMotor();
      sleep(2);
   elif a == "4":
      print("Turning left!");
      leftMotor();
      sleep();
   elif a == "exit":
      exit();
   elif a != "":
      print("Not a valid input! Try Again!");
