#!/usr/bin/env python  
import RPi.GPIO as GPIO
import time
import signal
import atexit
import Tkinter as Tk


class Radar:
    
    
    
    def __init__(self):
        ##SETUP PINS
            ####PINS
        self.servopin = 11
        self.echopin = 16
        self.triggerpin = 18
        
        atexit.register(GPIO.cleanup)  
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servopin, GPIO.OUT, initial=False)
        GPIO.setup(self.triggerpin,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.echopin,GPIO.IN)
        time.sleep(2)
        self.p = GPIO.PWM(self.servopin,50)
        self.p.start(0)
        time.sleep(2)
        self.distances={}
        self.init_distances()
        print("Initial distances: " + str(self.distances))
        
        
        #Current angle and distances
        self.current_angle = 0
        self.current_distance = 0
        
        
    def checkdist(self):
        GPIO.output(self.triggerpin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.triggerpin, GPIO.LOW)
        while not GPIO.input(self.echopin):
            pass
        t1 = time.time()
        while GPIO.input(self.echopin):
            pass
        t2 = time.time()
        return (t2-t1)*340/2
        
    def init_distances(self):
        for i in range(0,181,10):
            self.p.ChangeDutyCycle(2.5 + 10 * i / 180)
            time.sleep(0.2)
            self.distances[i] = self.checkdist()
            print 'Distance ' + 'for ' + str(i) + ': ' +  '%0.2f m' %self.checkdist()
            time.sleep(0.5)
            self.p.ChangeDutyCycle(0)
            time.sleep(0.2)
            
    def run_radar(self):
        try:
            while(True):
                for i in range(0,180,10):
                    #print("i: " + str(i))
                    #print("Value for angle " + str(i) + ": " + str(2.5 + 10 * i / 180))
                    #print(2.5 + 10 * i / 180)
                    '''Explanation
                    Python 2.7 dividiert und gibt integer zurueck -> KIndergarten dividieren
                    Python 3.6 gibt Float zurueck
                    Skript fuer python 2.7 gedacht
                    In PDF von Addept ms zu s Umrechnungsfehler sonst passt die Erklaerung fuer
                    2.5, 7.5 und 12.5 sind PWM Werte fuer 0, 90 und 180 grad servo motor
                    0,05s= 0grad (2,5/50), 0,15 s (7,5/50) = 90grad , 0,25s (12,5/50) = 180 grad
                    #codingworld.io/project/der-servo-am-raspberry-pi
                    '''
                    self.p.ChangeDutyCycle(2.5 + 10 * i / 180)
                    time.sleep(0.2)
                    
                    self.current_angle = i
                    self.current_distance = self.checkdist()
                    print 'Distance: %0.2f m' %self.current_distance 
                    
                    time.sleep(0.5)
                    self.p.ChangeDutyCycle(0)
                    time.sleep(0.2)
                for i in range(180,0,-10):
                    #print("Value for angle " + str(i) + ": " + str(2.5 + 10 * i / 180))
                    self.p.ChangeDutyCycle(2.5 + 10 * i / 180)
                    time.sleep(0.2)
                    self.current_angle = i
                    self.current_distance = self.checkdist()
                    print 'Distance: %0.2f m' %self.current_distance 
                    time.sleep(0.5)
                    self.p.ChangeDutyCycle(0)
                    time.sleep(0.2)
        except KeyboardInterrupt:
            GPIO.cleanup()
            