#! python
import telnetlib
import re


HOST = "192.168.1.100" #set OTGW ip
PORT = "6638" #set OTGW port
debug_lvl = 0 #set debug level: 0 or 1
verbose_lvl =1 #set verbose level: 0 or 1




tn = telnetlib.Telnet()


def telnet_read():
    
    try:
        
        if verbose_lvl > 0:
        
            print("connecting to host")
        
        if debug_lvl > 0:
            print("Debug set to print")
            tn.set_debuglevel(debug_lvl)
        
        tn.open(HOST,PORT)
        
        if verbose_lvl > 0:
        
            print("Port opened")
            
        tn.write(('PS=1' + '\r\n').encode('ascii'))
        output=tn.read_until(("\n>").encode('ascii'),1)
        tn.close()
        
        if verbose_lvl > 0:
            print("connection closed")
        
        return output
    
    except:
        print("Something went wrong, try setting debug and verbose to trace error")


def parse_data():
    
    if verbose_lvl > 0:
        print("Removing unused data bits")
        
    data_1= re.sub("b|P|S|r|n| |:|'|\\\\", "", data)
    data_2= data_1[1:]
    
    if verbose_lvl > 0:
        print("Creating table")
    data_list = data_2.split(',')
    
    return data_list
   
    
data= str(telnet_read())     
data= parse_data()  
print(data)

#Status (MsgID=0) - Printed as two 8-bit bitfields
#Control setpoint (MsgID=1) - Printed as a floating point value
#Remote parameter flags (MsgID= 6) - Printed as two 8-bit bitfields
#Maximum relative modulation level (MsgID=14) - Printed as a floating point value
#Boiler capacity and modulation limits (MsgID=15) - Printed as two bytes
#Room Setpoint (MsgID=16) - Printed as a floating point value
#Relative modulation level (MsgID=17) - Printed as a floating point value
#CH water pressure (MsgID=18) - Printed as a floating point value
#Room temperature (MsgID=24) - Printed as a floating point value
#Boiler water temperature (MsgID=25) - Printed as a floating point value
#DHW temperature (MsgID=26) - Printed as a floating point value
#Outside temperature (MsgID=27) - Printed as a floating point value
#Return water temperature (MsgID=28) - Printed as a floating point value
#DHW setpoint boundaries (MsgID=48) - Printed as two bytes
#Max CH setpoint boundaries (MsgID=49) - Printed as two bytes
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

if verbose_lvl > 0:
        print("Parsing data to variables")

MsgID_0=data.pop(0)
MsgID_1=float(data.pop(0))
MsgID_6=data.pop(0)
MsgID_14=float(data.pop(0))
MsgID_15=data.pop(0)
MsgID_16=float(data.pop(0))    
MsgID_17=float(data.pop(0))
MsgID_18=float(data.pop(0))
MsgID_24=float(data.pop(0))
MsgID_25=float(data.pop(0))
MsgID_26=float(data.pop(0))
MsgID_27=float(data.pop(0))
MsgID_28=float(data.pop(0))
MsgID_48=data.pop(0)
MsgID_49=data.pop(0)
MsgID_56=float(data.pop(0))
MsgID_57=float(data.pop(0))
MsgID_116=int(data.pop(0))
MsgID_117=int(data.pop(0))
MsgID_118=int(data.pop(0))
MsgID_119=int(data.pop(0))
MsgID_120=int(data.pop(0))
MsgID_121=int(data.pop(0))
MsgID_122=int(data.pop(0))
MsgID_123=int(data.pop(0))

if verbose_lvl > 0:
        print("Data parsed to variables")
