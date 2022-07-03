import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.cleanup()

#MOTORS 
GPIO.setup(18, GPIO.OUT)
#DIR MOTOR 2 - sinistra
GPIO.setup(11, GPIO.OUT)
#DIR MOTOR 1 - destra
GPIO.setup(9, GPIO.OUT)

TRIG1 = 24
ECHO1 = 25

TRIG2 = 4
ECHO2 = 17

TRIG3 = 14
ECHO3 = 15

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)

GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)

pwm=GPIO.PWM(18, 1000)
pwm.start(0)

def front():
            pulse_start = 0
            pulse_end = 0
            pulse_duration = 0
    
            GPIO.output(TRIG1, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(TRIG1, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(TRIG1, GPIO.LOW)

            while GPIO.input(ECHO1)==0:
                    pulse_start = time.time()

            while GPIO.input(ECHO1)==1:
                    pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)

            return distance

def left():
            start = 0
            end = 0
            pulse_duration = 0
    
            GPIO.output(TRIG2, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(TRIG2, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(TRIG2, GPIO.LOW)

            while GPIO.input(ECHO2)==0:
                    start = time.time()

            while GPIO.input(ECHO2)==1:
                    end = time.time()

            pulse_duration = end - start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
                    
            return distance
            
def right():
            start = 0
            end = 0
            pulse_duration = 0
            
            GPIO.output(TRIG3, GPIO.LOW)
            time.sleep(0.3)
            GPIO.output(TRIG3, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(TRIG3, GPIO.LOW)

            while GPIO.input(ECHO3)==0:
                    start = time.time()

            while GPIO.input(ECHO3)==1:
                    end = time.time()

            pulse_duration = end - start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
                    
            return distance

def stop():
        pwm.ChangeDutyCycle(0)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(9, GPIO.LOW)
        time.sleep(1)

def indietro():
        pwm.ChangeDutyCycle(100)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(9, GPIO.HIGH)
        time.sleep(1)
		
def avanti():
        pwm.ChangeDutyCycle(100)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(9, GPIO.LOW)
        time.sleep(1)

def destra():
        pwm.ChangeDutyCycle(100)
        GPIO.output(9, GPIO.HIGH)
        GPIO.output(11, GPIO.LOW)
        time.sleep(1.6)
        stop()
        
def sinistra():
        pwm.ChangeDutyCycle(100)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(9, GPIO.LOW)
        time.sleep(1.6)
        stop()

def giro_destra():
        pwm.ChangeDutyCycle(100)
        GPIO.output(9, GPIO.HIGH)
        GPIO.output(11, GPIO.LOW)
        time.sleep(3.6)
        stop()

def giro_sinistra():
        pwm.ChangeDutyCycle(100)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(9, GPIO.LOW)
        time.sleep(3.6)
        stop()
    

def run():
        fronts = 0
        lefts = 0
        rights = 0
        
        while True:
            fronts = front()
            time.sleep(0.2)
            lefts = left()
            time.sleep(0.2)
            rights = right()
            time.sleep(0.2)

            if((fronts < 25)or(lefts < 25)or(rights < 25)):
                if((fronts < 25)and(lefts < 25)):
                    giro_destra()
                elif((fronts < 25)and(rights < 25)):
                    giro_sinistra()
                elif((lefts < 25)and(rights < 25)):
                    if(fronts>50):
                        avanti()
                    else:
                        indietro()
                elif (fronts < 25):
                    if(left>50):
                        sinistra()
                        avanti()
                        time.sleep(1)
                    else:
                        destra()
                        avanti()
                        time.sleep(1)
            else:
                if((fronts < 350)and(lefts < 350)and(rights < 350)):
                    if((fronts > lefts) and (fronts > rights)):
                        avanti()
                    elif((lefts > fronts) and (lefts > rights)):
                        sinistra()
                        avanti()
                        time.sleep(1)
                    elif((rights > fronts) and (rights > lefts)):
                        destra()
                        avanti()
                        time.sleep(1)
                    else:
                        indietro()
                else:
                    indietro()
                
            
            
    

