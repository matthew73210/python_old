#! python

#based on : https://github.com/ivmech/ivPID/blob/master/PID.py
#and https://studentnet.cs.manchester.ac.uk/resources/library/thesis_abstracts/MSc14/FullText/Ioannidis-Feidias-fulltext.pdf

#import appdaemon.plugins.hass.hassapi as hass
import time
from math import *


class PID(): #add hass.Hass when in appdeamon
    
    def initialize(self): #This is where the variables used by the program will be set, and pulled when restarted.
        
        
        self.kd = self.get_state("input_number.pid_kd", attribute="state")
        self.ki = self.get_state("input_number.pid_ki", attribute="state")
        self.kp = self.get_state("input_number.pid_kp", attribute="state")
        
        self.setpoint = 0
        self.outside_temp = 0
        self.room_temp = 0
        self.error = 0
        self.last_error = 0
        
        #add function to check if pid values need calibrating. i.e. been reset to 0 or model is drifting to far from simulation
        
        
