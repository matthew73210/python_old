#! python
import telnetlib
import re
import getpass
import sys


HOST = "192.168.1.100" #set OTGW ip
PORT = "6638" #set OTGW port
debug_lvl = 0 #set debug level: 0 or 1
verbose_lvl =1 #set verbose level: 0 or 1


tn = telnetlib.Telnet()


def telnet_write():
    
        control_setpoint= input("setpoint ?")
        
        
        
        if verbose_lvl > 0:
        
            print("connecting to host")
        
        if debug_lvl > 0:
            print("Debug set to print")
            tn.set_debuglevel(debug_lvl)
        
        tn.open(HOST,PORT)
        
        if verbose_lvl > 0:
        
            print("Port opened")
            
        tn.write(('CS=' + control_setpoint + '\r\n').encode('ascii'))
        print(tn.read_until(("\n>").encode('ascii'),1))
        tn.close()
        
        if verbose_lvl > 0:
            print("connection closed")
            

telnet_write()

