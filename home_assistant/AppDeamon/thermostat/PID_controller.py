#! python

#based on : https://github.com/ivmech/ivPID/blob/master/PID.py
#https://studentnet.cs.manchester.ac.uk/resources/library/thesis_abstracts/MSc14/FullText/Ioannidis-Feidias-fulltext.pdf
#https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=12&ved=2ahUKEwiAqL_LksndAhWN4YUKHZ1dBIkQFjALegQIAxAC&url=http%3A%2F%2Fwww.mdpi.com%2F2071-1050%2F9%2F10%2F1868%2Fpdf&usg=AOvVaw3d-p3MLeCq3fWIewLoz9xh

import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta
from math import *
import time


class PID(hass.Hass): #add hass.Hass when in appdeamon
    
    def initialize(self): #This is where the variables used by the program will be set, and pulled when restarted.
        
        #for these variables i could create a dictonary
        self.kd = 0
        self.ki = 0
        self.kp = 0
        
        self.Pterm = 0
        self.Iterm = 0
        self.Dterm = 0
        
        self.output = 0
        
        self.setpoint = 0
        self.outside_temp = 0
        self.room_temp = 0
        self.error = 0
        self.last_error = 0
        
        self.dt = 0
        self.d_error = 0
        
        self.windup_guard = 20.0
        
        self.current_time = time.time()
        self.last_time = self.current_time
        
        self.log("initialized")
        
        #add function to check if pid values need calibrating. i.e. been reset to 0 or model is drifting to far from simulation
        
        self.run_every(self.test_function,datetime.now(),60)
        
        
    def test_function(self,kwargs):
    
        self.kd = self.get_state("input_number.pid_kd", attribute="state")
        self.ki = self.get_state("input_number.pid_ki", attribute="state")
        self.kp = self.get_state("input_number.pid_kp", attribute="state")
        
        
        self.setpoint = self.get_state("input_number.room_temp", attribute="state")
        self.outside_temp = self.get_state("sensor.temp_outside", attribute="state")
        self.room_temp = self.get_state("sensor.temp_lvr", attribute="state")
        self.current_time = time.time()
        
        
        self.error = float(self.setpoint) - float(self.room_temp)
        
        self.dt = self.current_time - self.last_time
        self.d_error = self.error - self.last_error
        
        self.log("setpoint")
        self.log(self.setpoint)
        self.log("outside temp")
        self.log(self.outside_temp)
        self.log("room temp")
        self.log(self.room_temp)
        self.log("error")
        self.log(self.error)
        
        self.log("kd,kp,kd")
        self.log(self.kd)
        self.log(self.kp)
        self.log(self.ki)
        
        self.log("dt, d_error")
        self.log(self.dt)
        self.log(self.d_error)
        
        self.log("time, last_time")
        self.log(self.current_time)
        self.log(self.last_time)
        
        
        self.last_time = self.current_time
        self.last_error = self.error
        
        self.log("variables printed")
        
        if (self.Iterm < -self.windup_guard):
            self.Iterm = -self.windup_guard
            self.log("min guard set")
        if (self.Iterm > self.windup_guard):
            self.Iterm = self.windup_guard
            self.log("max guard set")
        
        self.Pterm = float(self.kp)*float(self.error)
        self.Iterm += float(self.ki)*(float(self.error)*float(self.dt))
        self.Dterm = float(self.kd)*(float(self.d_error)/float(self.dt))
        
        self.output = self.Pterm + self.Dterm + self.Iterm
        
        self.log('pid terms')
        self.log(self.Pterm)
        self.log(self.Iterm)
        self.log(self.Dterm)
        
        self.set_state("sensor.Pterm", state = self.Pterm)
        self.set_state("sensor.Iterm", state = self.Iterm)
        self.set_state("sensor.Dterm", state = self.Dterm)
        self.set_state("sensor.output", state = self.output)
        
        
        
        
        
        
        
        
        
        
        
        
