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
        self.OTGW = telnetlib.Telnet()
        self.log("opentherm_OTGW is ready")

        #self.run_every(self.OTGW_read,datetime.now(),20)
        #self.run_every(self.OTGW_write,datetime.now(),20)
    
    def OTGW_read(self,kwargs):
    
    
        self.OTGW.open(self.HOST,self.PORT)
        self.log("Port opened")
        
        self.OTGW.write(('PS=1' + '\r\n').encode('ascii'))
        self.output=self.OTGW.read_until(("\n>").encode('ascii'),1)
        self.OTGW.close()
        self.log("PS=1 sent")
        
        self.data=str(self.output)
        self.log("string set")
        
        self.data_1= re.sub("b|P|S|r|n| |:|'|\\\\", "", self.data)
        self.log("data removed from string")
        
        self.data_2= self.data_1[1:]
        self.log("first value removed from string")
        
        self.data_list = self.data_2.split(',')
        self.log("string split")
                    
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
        
    
        
        self.log("variables printed")
        
        
        
        self.log("end of function")
    
    
    def OTGW_write(self,kwargs):
    
        state = self.get_state("input_number.command_setpoint", attribute="state")
        
        control_setpoint= str(state)
        
        
        self.OTGW.open(self.HOST,self.PORT)
        
        
        self.OTGW.write(('CS=' + control_setpoint + '\r\n').encode('ascii'))
        self.output=self.OTGW.read_until(("\n>").encode('ascii'),1)
        self.data=str(self.output)
        self.log(re.sub("b|r|n|'|\\\\", "", self.data))
        self.OTGW.close()
