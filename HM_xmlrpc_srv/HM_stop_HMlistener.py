#!/usr/bin/python
#
# HM_stop_HMlistener.py : HM_stop_HMlistener.py
# -------------------------------------------------
#
# system .............: linux
# directory ..........: 
# program ............: HM_stop_HMlistener.py
# version / release ..: 0.1
# date ...............: 2016.11.25 mg version 0.1
#
# programmer .........: Marcel Gross
# department .........: IT
#
# application group...: 
# application ........: mm_HM : Homematic House Automation
#
# usage ..............: HM_stop_HMlistener.py
#
# special ............: 
#
# history ............: 2016.11.25 14:26 mg
#                       base version
#
### Libraries #################################################################
#
import SocketServer
import sys
import io
import hashlib
import os
import time
import subprocess
import ConfigParser
import xmlrpclib
#
from datetime  import datetime
#
from mmHM_dbconfig import read_db_config
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
#
### Variables #################################################################
#
#
### Functions #################################################################
#------------------------------------------------------------------------------ 
#
# MAIN sub : HM_stop_HMlistener : stop Homematic xmlrpc-Listener
#
def HM_stop_HMlistener():
# 
#
# read : configuration from mm_DMS.config (for DB-connection)
#
    import xmlrpclib
    import time
#
    HM_config = ConfigParser.ConfigParser()
    HM_config.read('mm_HM.config')
    HM_CCU2AdressPort = HM_config.get('mmHM_global', 'HM_CCU2_IPAddressPort')
    HM_CCU2Adress     = HM_config.get('mmHM_global', 'HM_CCU2_IPAddress')
    HM_ListenerAdress = HM_config.get('mmHM_global', 'HM_Listener_IPAddress')
    HM_ListenerPort   = HM_config.get('mmHM_global', 'HM_Listener_Port')
#
# send : init with Listener IPAddress + Port and empty Parameter to CCU
#
    proxy = xmlrpclib.ServerProxy('http://' + HM_CCU2AdressPort)
    proxy = xmlrpclib.ServerProxy('http://' + HM_CCU2Adress + ':2001')
    print (proxy.init(HM_ListenerAdress + ':' + HM_ListenerPort, ''))
    print ("Stop HM Listener Request send to CCU: %s"   % str(HM_CCU2AdressPort))
    time.sleep( 1 )

    proxy = xmlrpclib.ServerProxy('http://' + HM_CCU2AdressPort)
    proxy = xmlrpclib.ServerProxy('http://' + HM_CCU2Adress + ':2010')
    print (proxy.init(HM_ListenerAdress + ':' + HM_ListenerPort, ''))
    print ("Stop HM Listener Request send to CCU: %s"   % str(HM_CCU2AdressPort))
    time.sleep( 1 )
    
#
# send : 
#
    s = xmlrpclib.ServerProxy('http://' + HM_ListenerAdress  + ":" + HM_ListenerPort)
    print ("Stop HM Listener Request send to HM Listener: %s"   % str(HM_ListenerAdress  + ":" + HM_ListenerPort))
    print (s.stop_listening("123456","stop listening now"))
    print ("Stop HM Listener Request send to HM Listener: %s"   % str(HM_ListenerAdress  + ":" + HM_ListenerPort))

    return  
#
### Main Program ##############################################################
#
if __name__ == '__main__':
#
    #parameters  = sys.argv[1:]
    #print ("sys.argv : " + str(sys.argv[1:]) + "\n")
    #print ("parameter: " + str(parameters) + "\n")
    HM_stop_HMlistener()
#
### END #######################################################################



