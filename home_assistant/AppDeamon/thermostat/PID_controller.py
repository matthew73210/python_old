#! python

#based on : https://github.com/ivmech/ivPID/blob/master/PID.py
#and https://studentnet.cs.manchester.ac.uk/resources/library/thesis_abstracts/MSc14/FullText/Ioannidis-Feidias-fulltext.pdf
#https://www.google.fr/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwiojuaxzc7dAhUExIUKHUAXC_EQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.asee.org%2Fpublic%2Fconferences%2F56%2Fpapers%2F12762%2Fdownload&psig=AOvVaw1NW3PjdZT95BNjl0Mb4Tnl&ust=1537705403878733

import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta
from math import *
import time


class PID(hass.Hass): #add hass.Hass when in appdeamon
    
    def initialize(self): #This is where the variables used by the program will be set, and pulled when restarted.
        
        self.log_level = 0 #set to 0 to supress logs in functions
        
        self.kd = 0
        self.ki = 0
        self.kp = 0
        
        self.Pterm = 0
        self.Iterm = 0
        self.Dterm = 0
        
        self.output = 0
        
        self.setpoint = 0
        self.outside_temp = 0
        self.insulation_coeff = 0
        self.room_temp = 0
        self.error = 0
        self.last_error = 0
        self.heatloss = 0
        
        self.dt = 0
        self.d_error = 0
        
        self.windup_guard = 50
        self.max_output = 100
        self.max_boiler_water_temp = 65
        self.boiler_water_temp = 0
        self.temp_window = 1.5
        
        self.current_time = time.time()
        self.last_time = self.current_time
        
        self.log("initialized")
        
        #add function to check if pid values need calibrating. i.e. been reset to 0 or model is drifting to far from simulation
        
        self.run_every(self.mode_check,datetime.now(),60)
        
    def mode_check(self,kwargs):
        
        mode = self.get_state("input_select.thermostat_mode", attribute="state")
        
        if self.log_level > 0:
            self.log(mode)
        
        if mode == "Hysteresis":
            if self.log_level > 0:
                self.log("Hysteresis mode")
                
            self.Hysteresis(kwargs)
        elif mode == "PID":
            if self.log_level > 0:
                self.log("PID mode")
                
            self.PID(kwargs)
        else:
            if self.log_level > 0:
                self.log("Heating off")
        
        
        
    def Hysteresis(self,kwargs):
        self.setpoint = self.get_state("input_number.room_temp", attribute="state")
        self.room_temp = self.get_state("sensor.temp_lvr", attribute="state")
        
        if float(self.room_temp) < (float(self.setpoint)-float(self.temp_window)):
            self.boiler_water_temp = self.max_boiler_water_temp
            
        if float(self.room_temp) > (float(self.setpoint)+float(self.temp_window)):
            self.boiler_water_temp = 0
            
        
        self.set_state("sensor.boiler_water_temp", state = self.boiler_water_temp)
        
    def PID(self,kwargs):
        
        #Pull PID coeffs from HA
        self.kd = self.get_state("input_number.pid_kd", attribute="state")
        self.ki = self.get_state("input_number.pid_ki", attribute="state")
        self.kp = self.get_state("input_number.pid_kp", attribute="state")
        
        #Pull heatloss coeff from HA
        self.insulation_coeff = self.get_state("input_number.insulation_coeff", attribute="state")
        
        #Pull temps and setpoint from HA
        self.setpoint = self.get_state("input_number.room_temp", attribute="state")
        self.outside_temp = self.get_state("sensor.temp_outside", attribute="state")
        self.room_temp = self.get_state("sensor.temp_lvr", attribute="state")
        
        #Get time
        self.current_time = time.time()
        
        #Heatloss calculation, as load disturbance 
        self.heatloss = float(self.insulation_coeff)*(float(self.room_temp)-float(self.outside_temp))
        
        #Calculate dt, error and d_error
        self.dt = self.current_time - self.last_time
        self.error = float(self.setpoint) - float(self.room_temp) + self.heatloss
        self.d_error = self.error - self.last_error
        
        
        #Push values to memory for next iteration
        self.last_time = self.current_time
        self.last_error = self.error
        
        #Input heatloss into error
        self.heatloss = float(self.insulation_coeff)*(float(self.room_temp)-float(self.outside_temp))
        
        #Calculate PID
        self.Pterm = float(self.kp)*float(self.error)
        self.Iterm += float(self.ki)*(float(self.error)*float(self.dt))
        self.Dterm = float(self.kd)*(float(self.d_error)/float(self.dt))
        
        self.output = self.Pterm + self.Dterm + self.Iterm
        
        #Clip output and Iterm agaisnt windup
        if self.output > self.max_output:
            self.output = self.max_output
            self.Iterm = self.windup_guard
            self.log("output and Iterm clipped")
        if self.output < -self.max_output:
            self.output = -self.max_output
            self.Iterm = -self.windup_guard
            self.log("output and Iterm clipped")
        
        #Temp mapping
        self.boiler_water_temp = (self.output*self.max_boiler_water_temp)/self.max_output
        
        if self.boiler_water_temp < 10:
            self.boiler_water_temp = 0
        
        
        
        
        
        self.set_state("sensor.Pterm", state = self.Pterm)
        self.set_state("sensor.Iterm", state = self.Iterm)
        self.set_state("sensor.Dterm", state = self.Dterm)
        self.set_state("sensor.heatloss", state = self.heatloss)
        self.set_state("sensor.heating_error", state = self.error)
        self.set_state("sensor.heating_output", state = self.output)
        self.set_state("sensor.boiler_water_temp", state = self.boiler_water_temp)
      
