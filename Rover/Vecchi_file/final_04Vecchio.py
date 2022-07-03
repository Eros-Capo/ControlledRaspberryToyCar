import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.cleanup()

GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

TRIG = 24
ECHO = 25

TRIG1 = 4
ECHO1 = 17

TRIG2 = 21
ECHO2 = 22

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(10, GPIO.OUT) #verde
GPIO.setup(15, GPIO.OUT) #rosso
GPIO.setup(14, GPIO.OUT) #giallo

pwm=GPIO.PWM(18, 1000)
pwm1=GPIO.PWM(23, 1000)
pwm.start(0)
pwm1.start(0)

GPIO.output(TRIG, False)
time.sleep(2)

t_fine = time.time() + 5*1
dist = 60.00

def avanti():
	GPIO.output(10,1)
	time.sleep(0.5)
	GPIO.output(10,0)
	pwm.ChangeDutyCycle(80)
	pwm1.ChangeDutyCycle(80)
	
def destra():
	GPIO.output(15, True)
	time.sleep(0.5)
	GPIO.output(15, False)
	pwm.ChangeDutyCycle(0)
	pwm1.ChangeDutyCycle(80)

def sinistra():
	GPIO.output(14,1)
	time.sleep(0.5)
	GPIO.output(14,0)
	pwm.ChangeDutyCycle(80)
	pwm1.ChangeDutyCycle(0)
	
def stop():
	pwm.ChangeDutyCycle(0)
	pwm1.ChangeDutyCycle(0)
	
def forward():
	global pulse_start 
	global pulse_end
	pulse_start = 0
	pulse_end = 0
	time.sleep(0.1)
	GPIO.output(TRIG, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(TRIG, GPIO.LOW)

	while GPIO.input(ECHO)==0:
		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)

	return distance
	
def left():
	global start
	global end
	time.sleep(0.1)
	GPIO.output(TRIG1, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(TRIG1, GPIO.LOW)

	while GPIO.input(ECHO1)==0:
		start = time.time()

	while GPIO.input(ECHO1)==1:
		end = time.time()

	pulse_duration = end - start
	distance = pulse_duration * 17150
	distance = round(distance, 2)
		
	return distance
	
def right():
	global inizio
	global fine
	time.sleep(0.1)
	GPIO.output(TRIG2, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(TRIG2, GPIO.LOW)

	while GPIO.input(ECHO2)==0:
		inizio = time.time()

	while GPIO.input(ECHO2)==1:
		fine = time.time()

	pulse_duration = fine - inizio
	distance = pulse_duration * 17150
	distance = round(distance, 2)
	return distance
	

try:
	while True:
	
		time.sleep(0.5)
		
		distanzavanti = forward()
		
		if distanzavanti < 200:
		
			if distanzavanti > dist and distanzavanti < 200:
				avanti()
				

			elif distanzavanti < 25 and distanzavanti > 10: #while 
				distanzasinistra = left()
				
				if distanzasinistra < 25 and distanzasinistra > 10: 
					destra()
					time.sleep(3)
					stop()
					
				elif distanzasinistra > 25 and distanzasinistra > distanzavanti: 
					sinistra()
					time.sleep(3)
					stop()
					
				#distanzavanti = forward()
				
			elif distanzavanti < dist and distanzavanti > 30:
				avanti()
				time.sleep(2)
				stop()
				distanzasinistra = left()
				
				if distanzasinistra > distanzavanti and distanzasinistra > 25 and distanzasinistra < 200:
					sinistra()
					time.sleep(0.5)
					avanti()
					time.sleep(1)
					stop()
					
				else:
					destra()
					time.sleep(0.5)
					avanti()
					time.sleep(1)
					stop()
					
		distanzavanti = forward()
						
except KeyboardInterrupt:
	pwm.stop()
	pwm1.stop()
	GPIO.cleanup()

pwm.stop()
pwm1.stop()
GPIO.cleanup()


