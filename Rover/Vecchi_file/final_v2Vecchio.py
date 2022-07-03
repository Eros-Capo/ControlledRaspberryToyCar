import time
import RPi.GPIO as GPIO
from Queue import Queue
from threading import Thread

GPIO.setmode(GPIO.BCM)

GPIO.cleanup()

GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

TRIG1 = 24
ECHO1 = 25

TRIG2 = 4
ECHO2 = 17

TRIG3 = 21
ECHO3 = 22

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)

GPIO.setup(10, GPIO.OUT) #verde
GPIO.setup(15, GPIO.OUT) #rosso
GPIO.setup(14, GPIO.OUT) #giallo

pwm=GPIO.PWM(18, 1000)
pwm1=GPIO.PWM(23, 1000)
pwm.start(0)
pwm1.start(0)

NUMBER_OF_THREADS = 4
JOB_NUMBER = [1, 2, 3, 4]
queue = Queue()

class USavanti:
    
    def forward(self):
        GPIO.output(TRIG1, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(TRIG1, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG1, GPIO.LOW)

        start = 0
        end = 0

        while GPIO.input(ECHO1)==0:
            start = time.time()

        tempo = 0.0001

        print "tempo1" 
        
        while GPIO.input(ECHO1)==1 and (tempo < 0.014):
            end = time.time()
            tempo = end - start

        pulse_duration = end - start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print distance      
        return distance

    def run(self):
        self.forward()
        
        
class USsinistra:
    def left(self):
        GPIO.output(TRIG2, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(TRIG2, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG2, GPIO.LOW)

        start = 0
        end = 0

        while GPIO.input(ECHO2)==0:
            start = time.time()

        print "tempo2" 
        
        while GPIO.input(ECHO2)==1:
            end = time.time()

        pulse_duration = end - start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print distance       
        return distance

    def run(self):
        self.left()
        

class USdestra:
    def right(self):
        GPIO.output(TRIG3, GPIO.LOW)
        time.sleep(0.3)
        GPIO.output(TRIG3, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG3, GPIO.LOW)

        start = 0
        end = 0

        while GPIO.input(ECHO3)==0:
            start = time.time()

        tempo = 0.0001

        print "tempo3" 
        
        while GPIO.input(ECHO3)==1 and (tempo < 0.014):
            end = time.time()
            tempo = end - start

        pulse_duration = end - start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print distance    
        return distance

    def run(self):
        self.right()
        

class Gas:
    def avanti(self):
        pwm.ChangeDutyCycle(100)
        pwm1.ChangeDutyCycle(100)
        time.sleep(2)
    
    def destra(self):
        pwm.ChangeDutyCycle(0)
        pwm1.ChangeDutyCycle(100)
        time.sleep(2)
        
    def sinistra(self):
        pwm.ChangeDutyCycle(100)
        pwm1.ChangeDutyCycle(0)
        time.sleep(2)
        
    def running(self):
        try:
            while True:
                dist_avanti = USavanti().run()
                dist_sinistra = USsinistra().run()
                dist_destra = USdestra().run()

                print "avanti" + dist_avanti
                #print "sinistra" + dist_sinistra
                #print "destra" + dist_destra
                
                #while dist_avanti < 200 and dist_sinistra < 200 and dist_destra < 200:

                if dist_avanti > 20:
                    Gas().avanti()
                else:
                    if dist_sinistra < dist_destra:
                        Gas().destra()
                    else:
                        Gas().sinistra()
                
                    '''
                    if dist_avanti > (dist_destra and dist_sinistra):
                        Gas().avanti()
                    
                    elif dist_sinistra > (dist_destra and dist_avanti):
                        Gas().sinistra()
                    
                    elif dist_destra > (dist_avanti and dist_sinistra):
                        Gas().destra()
                    '''    
                    #time.sleep
                                
        
        except Exception as e:
            print e
        except KeyboardInterrupt:
            pwm.stop()
            pwm1.stop()
            GPIO.cleanup()
        
    def run(self):
        self.running()


class ThreadHandler:
    def create_workers(self):
        for _ in range(NUMBER_OF_THREADS):
            t = Thread(target=self.work)
            t.daemon = True
            t.start()

    def work(self):
        x = queue.get()
        if x == 1:
            USavanti().run()
        if x == 2:
            USdestra().run()
        if x == 3:
            USsinistra().run()
        if x == 4:
            Gas().run()
        queue.task_done()

    def create_jobs(self):
        for x in JOB_NUMBER:
            queue.put(x)
        queue.join()

    def run(self):
        self.create_workers()
        self.create_jobs()


if __name__ == '__main__':
    ThreadHandler().run()
