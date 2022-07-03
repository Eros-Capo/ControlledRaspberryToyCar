import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.cleanup()

GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

TRIG = 24
ECHO = 25

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

pwm=GPIO.PWM(18, 1000)
pwm1=GPIO.PWM(23, 1000)
pwm.start(0)
pwm1.start(0)

GPIO.output(TRIG, False)
print "Aspettiamo il sensore"
time.sleep(2)

t_end = time.time() + 60 * 1
dist = 10.00

def avanti():
	pwm.ChangeDutyCycle(100)
	pwm1.ChangeDutyCycle(100)
	
def destra():
	pwm.ChangeDutyCycle(0)
	pwm1.ChangeDutyCycle(100)

def sinistra():
	pwm.ChangeDutyCycle(100)
	pwm1.ChangeDutyCycle(0)
	
def stop():
	pwm.ChangeDutyCycle(0)
	pwm1.ChangeDutyCycle(0)
	

try:
	while True:

			avanti()
			time.sleep(3)
			stop()


except KeyboardInterrupt:
	pwm.stop()
	pwm1.stop()
	GPIO.cleanup()

pwm.stop()
pwm1.stop()
GPIO.cleanup()


