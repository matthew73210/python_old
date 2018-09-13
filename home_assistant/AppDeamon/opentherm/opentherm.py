#! python
import appdaemon.plugins.hass.hassapi as hass
import telnetlib
import re
from datetime import datetime, timedelta

#Here are the different msg_id that are printed with the PS=1 command
#please refer to the following doccuments : http://otgw.tclcode.com/firmware.html and https://www.domoticaforum.eu/uploaded/Ard%20M/Opentherm%20Protocol%20v2-2.pdf

#Status (MsgID=0) - Printed as two 8-bit bitfields
#Control setpoint (MsgID=1) - Printed as a floating point value / not used
#Remote parameter flags (MsgID= 6) - Printed as two 8-bit bitfields / not used
#Maximum relative modulation level (MsgID=14) - Printed as a floating point value / not used
#Boiler capacity and modulation limits (MsgID=15) - Printed as two bytes / not used
#Room Setpoint (MsgID=16) - Printed as a floating point value / not used
#Relative modulation level (MsgID=17) - Printed as a floating point value
#CH water pressure (MsgID=18) - Printed as a floating point value / not used
#Room temperature (MsgID=24) - Printed as a floating point value / not used
#Boiler water temperature (MsgID=25) - Printed as a floating point value
#DHW temperature (MsgID=26) - Printed as a floating point value
#Outside temperature (MsgID=27) - Printed as a floating point value / not used
#Return water temperature (MsgID=28) - Printed as a floating point value
#DHW setpoint boundaries (MsgID=48) - Printed as two bytes / not used
#Max CH setpoint boundaries (MsgID=49) - Printed as two bytes / not used
#DHW setpoint (MsgID=56) - Printed as a floating point value
#Max CH water setpoint (MsgID=57) - Printed as a floating point value
#Burner starts (MsgID=116) - Printed as a decimal value
#CH pump starts (MsgID=117) - Printed as a decimal value
#DHW pump/valve starts (MsgID=118) - Printed as a decimal value
#DHW burner starts (MsgID=119) - Printed as a decimal value
#Burner operation hours (MsgID=120) - Printed as a decimal value
#CH pump operation hours (MsgID=121) - Printed as a decimal value
#DHW pump/valve operation hours (MsgID=122) - Printed as a decimal value
#DHW burner operation hours (MsgID=123) - Printed as a decimal value





class opentherm_OTGW(hass.Hass):

    def initialize(self):
        
        #In this function the you need to set the ip and the port used by the OTGW, after that it trys to connect and validate the paramters. Otherwise it throws an error.
        
        
        self.HOST = "192.168.1.100" #set OTGW ip
        self.PORT = "6638" #set OTGW port
        self.OTGW = telnetlib.Telnet() #telnet object
        self.log_level = 1 #set to 0 to supress logs in functions
        self.validation = 0 #used to stop function if except thrown
        
        try:
            self.log("Testing connection")
            self.OTGW.open(self.HOST,self.PORT,1)
            self.OTGW.close()
            self.validation = 1
            self.log("Connection successful")
            self.log("opentherm_OTGW is ready")
            
        except:
            self.error("Connection couldn't establish, HOST and PORT set ?")
            self.error("Opentherm is not working")
            self.validation = 0
        
        
        self.control_setpoint_old = 0 
        self.data_list_old = 0
        self.data_list = 0
        
        
        if self.validation == 1:
        
            self.run_every(self.run_opentherm,datetime.now(),20)
    
    def run_opentherm(self,kwargs):
    
        self.run = 0
        self.OTGW_test(kwargs)
        
        if self.run == 1:
            self.OTGW_read(kwargs)
            self.OTGW_write(kwargs)
            self.OTGW_send_to_HA(kwargs)
    
    def OTGW_test(self,kwargs):
        
        try:
            self.OTGW.open(self.HOST,self.PORT,10)
            self.OTGW.close()
            self.run = 1
            if self.log_level > 0:
                self.log("Host is still up!")
        except:
            self.log("Host is down, retry next time")
            self.run =0
            
    
    def OTGW_read(self,kwargs):
    
    #In this function the app sends a command to the OTGW and then parses the output, this is tailored to the digits i didn't need.
    #I would recommend using putty and connecting to the OTGW using a telnet connection. Then sending a 'PS=1' command.
    #The OTGW replies with PS: and then the data we need, it also inserts a b, \r\n, and some ' all of which need to be removed.
    #Per the opentherm protocol the msg_id should only contain decimals.
    
        self.OTGW.open(self.HOST,self.PORT,10)
        
        
        if self.log_level > 0:
            self.log("Port opened")
        
        self.OTGW.write(('PS=1' + '\r\n').encode('ascii'))
        output=self.OTGW.read_until(("\n>").encode('ascii'),1)
        self.OTGW.close()
        
        if self.log_level > 0:
            self.log("PS=1 sent")
        
        data=str(output)
        
        if self.log_level > 0:
            self.log("string set")
        
        data_1= re.sub("b|P|S|r|n| |:|'|\\\\", "", data)
        
        if self.log_level > 0:
            self.log("data removed from string")
        
        data_2= data_1[1:]
        
        if self.log_level > 0:
            self.log("first value removed from string")
        
        self.data_list = data_2.split(',')
        
        if self.log_level > 0:
            self.log("string split")
        
            self.log(self.data_list)
    
    
    def OTGW_write(self,kwargs):
        
        #In this function we pull the setpoint from an input_nulber set in the configuration.yaml folder and send it to the OTGW, which replies and confirms.
        #As this function restarts every x seconds there is no need to check if the command was sussesfull. This could be a futur addidtion.
        
        state = self.get_state("input_number.command_setpoint", attribute="state")
        
        control_setpoint= str(state)
        
        if self.control_setpoint_old != control_setpoint:
        
            if self.log_level > 0:
                self.log("Sending new control_setpoint")
                
            self.OTGW.open(self.HOST,self.PORT,10)
            
            
            self.OTGW.write(('CS=' + control_setpoint + '\r\n').encode('ascii'))
            self.output=self.OTGW.read_until(("\n>").encode('ascii'),1)
            self.data=str(self.output)
            if self.log_level > 0:
                self.log(re.sub("b|r|n|'|\\\\", "", self.data))
                
            self.OTGW.close()
            
            self.control_setpoint_old=control_setpoint
        
        else:
            if self.log_level > 0:
                self.log("nothing to send")
        
    def OTGW_send_to_HA(self,kwargs):
        
        #Here we check if the data has changed and update the variables. I chose to do it this was as to let you choose which and what data gets sent to HA.
        #For this to work you can either (thanks ReneTode) send as a sensor or update a input_nuber/text. All the entities must be set in configuration.yaml
        
        if self.data_list_old != self.data_list:
        
        
            msgid_0=self.data_list.pop(0)
            msgid_1=float(self.data_list.pop(0))
            msgid_6=self.data_list.pop(0)
            msgid_14=float(self.data_list.pop(0))
            msgid_15=self.data_list.pop(0)
            msgid_16=float(self.data_list.pop(0))    
            msgid_17=float(self.data_list.pop(0))
            msgid_18=float(self.data_list.pop(0))
            msgid_24=float(self.data_list.pop(0))
            msgid_25=float(self.data_list.pop(0))
            msgid_26=float(self.data_list.pop(0))
            msgid_27=float(self.data_list.pop(0))
            msgid_28=float(self.data_list.pop(0))
            msgid_48=self.data_list.pop(0)
            msgid_49=self.data_list.pop(0)
            msgid_56=float(self.data_list.pop(0))
            msgid_57=float(self.data_list.pop(0))
            msgid_116=int(self.data_list.pop(0))
            msgid_117=int(self.data_list.pop(0))
            msgid_118=int(self.data_list.pop(0))
            msgid_119=int(self.data_list.pop(0))
            msgid_120=int(self.data_list.pop(0))
            msgid_121=int(self.data_list.pop(0))
            msgid_122=int(self.data_list.pop(0))
            msgid_123=int(self.data_list.pop(0))
            
            if self.log_level > 0:
                self.log("variables updated")
            
            
            self.call_service("input_text/set_value",entity_id="input_text.msgid_0",value=msgid_0)
            
            if msgid_0 == "00000001/00000000":
                self.set_state("sensor.central_heating", state = "on")
            
            if msgid_0 == "00000001/00000010":
                self.set_state("sensor.central_heating_running", state = "on")
                self.set_state("sensor.central_heating", state = "on")
                
            if msgid_0 == "00000001/00001010":
                self.set_state("sensor.central_heating_running", state = "on")
                self.set_state("sensor.central_heating", state = "on")
                self.set_state("sensor.flame_status", state = "on")
                
            if msgid_0 == "00000000/00001100":
                self.set_state("sensor.hot_water_running", state = "on")
                self.set_state("sensor.flame_status", state = "on")
                
            if msgid_0 == "00000000/00000000":
                self.set_state("sensor.central_heating_running", state = "off")
                self.set_state("sensor.central_heating", state = "off")
                self.set_state("sensor.flame_status", state = "off")
                self.set_state("sensor.hot_water_running", state = "off")
            
            
            self.set_state("sensor.msgid_17", state = msgid_17)
            self.set_state("sensor.msgid_25", state = msgid_25)
            self.set_state("sensor.msgid_26", state = msgid_26)
            self.set_state("sensor.msgid_28", state = msgid_28)
            self.set_state("sensor.msgid_56", state = msgid_56)
            self.set_state("sensor.msgid_57", state = msgid_57)
            self.set_state("sensor.msgid_116", state = msgid_116)
            self.set_state("sensor.msgid_117", state = msgid_117)
            self.set_state("sensor.msgid_118", state = msgid_118)
            self.set_state("sensor.msgid_119", state = msgid_119)
            self.set_state("sensor.msgid_120", state = msgid_120)
            self.set_state("sensor.msgid_121", state = msgid_121)
            self.set_state("sensor.msgid_122", state = msgid_122)
            self.set_state("sensor.msgid_123", state = msgid_123)
            
            self.data_list_old = self.data_list
            
            if self.log_level > 0:
                self.log("variables printed")
            
        else:
            if self.log_level > 0:
                self.log("nothing to write")
        
        
