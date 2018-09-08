#! python
import appdaemon.plugins.hass.hassapi as hass
import telnetlib
import re
from datetime import datetime, timedelta

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
    
        
        self.HOST = "192.168.1.100" #set OTGW ip
        self.PORT = "6638" #set OTGW port
        self.OTGW = telnetlib.Telnet() #telnet object
        self.log_level = 0 #set to 0 to supress logs in functions
        
        
        
        
        self.control_setpoint_old = 0 
        self.data_list_old = 0
        
        self.log("opentherm_OTGW is ready")
        
        
        self.run_every(self.OTGW_read,datetime.now(),20)
        
    
    def OTGW_read(self,kwargs):
    
    
        self.OTGW.open(self.HOST,self.PORT)
        
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
        
        data_list = data_2.split(',')
        
        if self.log_level > 0:
            self.log("string split")
        
        
        if self.data_list_old != data_list:
        
        
            msgid_0=data_list.pop(0)
            msgid_1=float(data_list.pop(0))
            msgid_6=data_list.pop(0)
            msgid_14=float(data_list.pop(0))
            msgid_15=data_list.pop(0)
            msgid_16=float(data_list.pop(0))    
            msgid_17=float(data_list.pop(0))
            msgid_18=float(data_list.pop(0))
            msgid_24=float(data_list.pop(0))
            msgid_25=float(data_list.pop(0))
            msgid_26=float(data_list.pop(0))
            msgid_27=float(data_list.pop(0))
            msgid_28=float(data_list.pop(0))
            msgid_48=data_list.pop(0)
            msgid_49=data_list.pop(0)
            msgid_56=float(data_list.pop(0))
            msgid_57=float(data_list.pop(0))
            msgid_116=int(data_list.pop(0))
            msgid_117=int(data_list.pop(0))
            msgid_118=int(data_list.pop(0))
            msgid_119=int(data_list.pop(0))
            msgid_120=int(data_list.pop(0))
            msgid_121=int(data_list.pop(0))
            msgid_122=int(data_list.pop(0))
            msgid_123=int(data_list.pop(0))
            
            if self.log_level > 0:
                self.log("variables updated")
            
            self.call_service("input_number/set_value",entity_id="input_number.msgid_17",value=msgid_17)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_25",value=msgid_25)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_26",value=msgid_26)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_28",value=msgid_28)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_56",value=msgid_56)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_57",value=msgid_57)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_116",value=msgid_116)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_117",value=msgid_117)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_118",value=msgid_118)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_119",value=msgid_119)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_120",value=msgid_120)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_121",value=msgid_121)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_122",value=msgid_122)
            self.call_service("input_number/set_value",entity_id="input_number.msgid_123",value=msgid_123)
            
            self.data_list_old = data_list
            
            if self.log_level > 0:
                self.log("variables printed")
            
        else:
            if self.log_level > 0:
                self.log("nothing to write")
        
        
        self.OTGW_write(kwargs)
    
    
    def OTGW_write(self,kwargs):
    
        state = self.get_state("input_number.command_setpoint", attribute="state")
        
        control_setpoint= str(state)
        
        if self.control_setpoint_old != control_setpoint:
        
            if self.log_level > 0:
                self.log("Sending new control_setpoin")
                
            self.OTGW.open(self.HOST,self.PORT)
            
            
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
        
