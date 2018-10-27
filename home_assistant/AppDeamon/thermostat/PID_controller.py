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
        
        self.anti_windup = 0
        
        self.Pterm = 0
        self.Iterm = 0
        self.Dterm = 0
        
        self.Iterm_anti_windup = 0
        
        self.output = 0
        
        self.setpoint = 0
        self.outside_temp = 0
        self.insulation_coeff = 0
        self.room_temp = 0
        self.error = 0
        self.last_error = 0
        self.heatloss = 0
        self.windup = 0
        self.windup_X = 0
        
        self.dt = 0
        self.d_error = 0
        
        self.windup_guard = 50
        self.max_output = 100
        self.max_boiler_water_temp = 65
        self.boiler_water_temp = 0
        self.temp_window = 1.5
        
        self.current_time = time.time() #had a problem where the integral would have a massive delta t, a consequence of have a 20 second cycle. Check dt with log that it is larger than 1 but no mre than 10. Otherwise it will osscilate with anti windup
        self.last_time = self.current_time
        
        self.log("initialized")
        
        
        self.run_every(self.mode_check,datetime.now(),5) #this needs to be set compaired to system deadtime, to low and the integral will windup even with antiwindup.
        
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
            self.boiler_water_temp = 0
            self.Pterm = 0
            self.Iterm = 0
            self.Dterm = 0
            self.error = 0
            self.output = 0
            self.windup_X = 0
            
            
        self.sendtoHA()
            
    def sendtoHA(self):
        self.set_state("input_number.command_setpoint", state = self.boiler_water_temp )
        self.set_state("sensor.Pterm", state = self.Pterm)
        self.set_state("sensor.Iterm", state = self.Iterm)
        self.set_state("sensor.Dterm", state = self.Dterm)
        self.set_state("sensor.heating_error", state = self.error)
        self.set_state("sensor.heating_output", state = self.output)
        self.set_state("sensor.boiler_water_temp", state = self.boiler_water_temp)
        self.set_state("sensor.windup_X", state = self.windup_X)
        if self.log_level > 0:
                self.log("Command sent to HA")
        
        
    def Hysteresis(self,kwargs):
        self.setpoint = self.get_state("input_number.room_temp", attribute="state")
        self.room_temp = self.get_state("sensor.temp_lvr", attribute="state")
        
        if float(self.room_temp) < (float(self.setpoint)-float(self.temp_window)):
            self.boiler_water_temp = self.max_boiler_water_temp
            
        if float(self.room_temp) > (float(self.setpoint)+float(self.temp_window)):
            self.boiler_water_temp = 0
            
        
        self.set_state("sensor.boiler_water_temp", state = self.boiler_water_temp)
        
    def PID(self,kwargs):
        
        #reset main windup variable
        self.windup = 0
        
        #Pull PID coeffs from HA
        self.kd = self.get_state("input_number.pid_kd", attribute="state")
        self.ki = self.get_state("input_number.pid_ki", attribute="state")
        self.kp = self.get_state("input_number.pid_kp", attribute="state")
        self.anti_windup = self.get_state("input_number.pid_anti_windup", attribute="state")
        
        #Pull temps and setpoint from HA
        self.setpoint = self.get_state("input_number.room_temp", attribute="state")
        self.room_temp = self.get_state("sensor.temp_lvr", attribute="state")
        
        #Get time
        self.current_time = time.time()
        if self.log_level > 0:
            self.log("time")
            self.log(self.current_time)

        #Calculate dt, error and d_error
        self.dt = self.current_time - self.last_time
        if self.log_level > 0:
            self.log("dt")
            self.log(self.dt)
        self.error = float(self.setpoint) - float(self.room_temp)
        self.d_error = self.error - self.last_error
        

        
        
        #Push values to memory for next iteration
        self.last_time = self.current_time
        self.last_error = self.error
        
        #testing antiwind for i term, if over it will re evaluate the i term
        self.Iterm_anti_windup = self.Iterm
        
        #Calculate PID
        self.Pterm = float(self.kp)*float(self.error)
        self.Iterm = self.Iterm + float(self.ki)*((float(self.error))*float(self.dt))
        self.Dterm = float(self.kd)*(float(self.d_error)/float(self.dt))
        
        
        
        self.output = self.Pterm + self.Dterm + self.Iterm
        
        #Clip output and Iterm agaisnt windup
        if self.output > self.max_output:
            self.windup = -float(self.output) + float(self.max_output)
            self.windup_X = float(self.windup) * float(self.anti_windup)
            self.Iterm = self.Iterm_anti_windup + float(self.ki)*((float(self.error) + float(self.windup_X))*float(self.dt))
            self.output = self.Pterm + self.Dterm + self.Iterm
        if self.output < 0:
            self.windup = -float(self.output) + float(0)
            self.windup_X = float(self.windup) * float(self.anti_windup)
            self.Iterm = self.Iterm_anti_windup + float(self.ki)*((float(self.error) + float(self.windup_X))*float(self.dt))
            self.output = self.Pterm + self.Dterm + self.Iterm

            
            

        
        
        
        if self.log_level > 0:
            self.log("windup and windup X")
            self.log(self.windup)
            self.log(self.windup_X)
        
        
        
        #Temp mapping
        self.boiler_water_temp = (self.output*self.max_boiler_water_temp)/self.max_output
        
        if self.boiler_water_temp < 10:
            self.boiler_water_temp = 0
        #self.boiler_water_temp = 0 #comment out when finished testing, program will send values to boiler
        
