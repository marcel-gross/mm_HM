#!/usr/bin/python
#
# HM_xmlrpc_listener.py : Homematic xmlrpc listener
# -------------------------------------------------
#
# system .............: linux
# directory ..........: 
# program ............: HM_xmlrpc_listener.py
# version / release ..: 0.1
# date ...............: 2016.11.17 mg version 0.1
#
# programmer .........: Marcel Gross
# department .........: IT
#
# application group...: 
# application ........: mm_HM : Homematic House Automation
#
# usage ..............: HM_xmlrpc_listener.py
#
# special ............: 
#
# history ............: 2016.11.17 14:26 mg
#                       base version
#
### Libraries #################################################################
#
import SocketServer
import sys
import io
import sqlite3
import hashlib
import os
import time
import subprocess
import ConfigParser
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
#
# connect : to configured Database
#
#------------------------------------------------------------------------------ 
#
# sub : get parameters
#

def log_ops(string):
#
    wrklog = 'HM_xmlrpc_listener.log'
    TimeStamp = datetime.now()
    
    string = str(TimeStamp) + " " + string + "\n"
    try:
        File = open(wrklog, 'a')
        File.writelines(string)
        File.close()
    except Exception as e:
        print ("write of log was not successful")
    return
#
#------------------------------------------------------------------------------ 
#
def db_ops(args):
#
# read : configuration from mm_DMS.config (for DB-connection)
#
    HM_config = ConfigParser.ConfigParser()
    HM_config.read('mm_HM.config')
    usedDB = HM_config.get('mmHM_global', 'DB_database')
    #print ("DB used: %s"   % str(usedDB))
#
# connect : to configured Database
#
    global cursor 
    if usedDB == "mmHM_sqlite": 
        try: 
            SQLite_database = HM_config.get('mmHM_sqlite', 'SQLite_database')
            db = sqlite3.connect(SQLite_database)
#            db.isolation_level = None
            cursor = db.cursor()
            #print ('sqlite connection established')
        except :
            print ('sqlite connection failed')
            sys.exit(2)
    elif usedDB == "mmHM_mysql":
        connect_DB()
    else:
        print ("Database connection failed, due to wrong configuration in mm_HM.config file.")
#
#  db.isolation_level = None
    cursor = db.cursor()
    try:
        create_table_document_data()
        # Commit the change
        db.commit()
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        db.close()
        raise e
#	
    TimeStamp = datetime.now()
    ListenerId = str(args[1])
    DevID = str(args[2])
    DevParameter = str(args[3])
    DevParameterValue = str(args[4])
#
    try: 
        write_data_into_table(TimeStamp, ListenerId, DevID, DevParameter, DevParameterValue )
        db.commit()
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        db.close()
        raise e
    
    #sleep(DELAY)
    db.close()
    return
#
#------------------------------------------------------------------------------ 
#
# sub : write_data_into_table 
# 
def write_data_into_table(TimeStamp, ListenerId, DevID, DevParameter, DevParameterValue ):
#
#  
#
    cursor.execute('''insert into HM_comlog_data (comlog_TimeStamp, comlog_ListenerId, comlog_DevID, comlog_DevParameter, comlog_DevParameterValue) 
                      values (?, ?, ?, ?, ?)''', 
                      ( TimeStamp, ListenerId, DevID, DevParameter, DevParameterValue )
		  )
    return
#
#------------------------------------------------------------------------------ 
#
# sub : create_table_document_data 
# 
def create_table_document_data():
#
#      cursor.execute('''DROP TABLE IF EXISTS HM_comlog_data''')
#
# HM_comlog_data : communication logging data 
#
    cursor.execute('''CREATE TABLE IF NOT EXISTS
                      HM_comlog_data
		        (
 		          comlog_id       		INTEGER PRIMARY KEY AUTOINCREMENT,
                          comlog_TimeStamp		DATETIME,
			  comlog_ListenerId		VARCHAR(50),
			  comlog_DevID			VARCHAR(250),
			  comlog_DevParameter		VARCHAR(250),
			  comlog_DevParameterValue	VARCHAR(250)
			)
    ''')
    return
#
#------------------------------------------------------------------------------ 
#
# sub : initiate_hm_listener():
#
def initiate_hm_listener():
#
# read : configuration from mm_DMS.config (for DB-connection)
#
    import xmlrpclib
#
    HM_config = ConfigParser.ConfigParser()
    HM_config.read('mm_HM.config')
    HM_CCU2AdressPort = HM_config.get('mmHM_global', 'HM_CCU2_IPAddressPort')
    HM_CCU2Adress     = HM_config.get('mmHM_global', 'HM_CCU2_IPAddress')
    HM_ListenerAdress = HM_config.get('mmHM_global', 'HM_Listener_IPAddress')
    HM_ListenerPort   = HM_config.get('mmHM_global', 'HM_Listener_Port')
#
    HM_Parameter = 'hm_listener on ' + HM_ListenerAdress + ' on port: ' + HM_ListenerPort
#
    proxy = xmlrpclib.ServerProxy('http://' + HM_CCU2Adress + ':2001')
    time.sleep( 1 )
    print proxy.init(HM_ListenerAdress + ':' + HM_ListenerPort, HM_Parameter)
    print ("HM Listener Request send to CCU: %s"   % str(HM_CCU2Adress + ':2001'))
    time.sleep( 2 )
    
    proxy = xmlrpclib.ServerProxy('http://' + HM_CCU2Adress + ':2010')
    time.sleep( 1 )
    print proxy.init(HM_ListenerAdress + ':' + HM_ListenerPort, HM_Parameter)
    print ("HM Listener Request send to CCU: %s"   % str(HM_CCU2Adress + ':2010'))
    time.sleep( 3 )
    
    exit(0)
    return
    
#------------------------------------------------------------------------------ 
### Main Program ##############################################################
#
# 
# Threaded mix-in
#
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn,SimpleXMLRPCServer): pass
# 
# Example class to be published
#
class mm_HM_XMLRPC_Object:
    def stop_listening(*args):
        global self_shutdown
	#print "---"
	#db_ops(args)
	string = "stop_listening: " + str(args[1]) + " " + str(args[2]) #+ " " + str(args[3]) + " "  + str(args[4])
	log_ops(string)
	server.shutdown()
	server.server_close()
	#return '<?xml version="1.0"?>\n<methodResponse>\n   <params>\n      <param>\n         <value>\n            <array>\n               <data>\n               </data>\n            </array>\n         </value>\n      </param>\n   </params>\n</methodResponse>'
        ret_array = []
        return ret_array

    def event(*args):
        #print "---event---"
        #for arg in args:
        #    print arg
	#print "---"
	db_ops(args)
	string = "event: " + str(args[1]) + " " + str(args[2]) + " " + str(args[3]) + " "  + str(args[4])
	log_ops(string)
	#return '<?xml version="1.0"?>\n<methodResponse>\n   <params>\n      <param>\n         <value>\n            <array>\n               <data>\n               </data>\n            </array>\n         </value>\n      </param>\n   </params>\n</methodResponse>'
        ret_array = []
        return ret_array

    def listDevices(*args):
#        print "---listDevices---"
        string = "listDevices: "
        for arg in args:
            string = string + " " + str(arg)

	log_ops(string)
	ret_array = []
	
	#a =  ['<?xml version="1.0"?>\n<methodResponse>\n   <params>\n      <param>\n         <value>\n            <array>\n               <data>\n               </data>\n            </array>\n         </value>\n      </param>\n   </params>\n</methodResponse>']
        return ret_array
              
    def newDevices(*args):
        #print "---newDevices---"
        string = "newDevices: "
        for arg in args:
            string = string + " " + str(arg)

	log_ops(string)
	#return '<?xml version="1.0"?>\n<methodResponse>\n   <params>\n      <param>\n         <value>\n            <array>\n               <data>\n               </data>\n            </array>\n         </value>\n      </param>\n   </params>\n</methodResponse>'
        ret_array = []
        return ret_array

    def newDevice(*args):
        #print "---newDevice---"
        string = "newDevice: "
        for arg in args:
            string = string + " " + str(arg)

	log_ops(string)
	#return '<?xml version="1.0"?>\n<methodResponse>\n   <params>\n      <param>\n         <value>\n            <array>\n               <data>\n               </data>\n            </array>\n         </value>\n      </param>\n   </params>\n</methodResponse>'
        ret_array = []
        return ret_array
# 
# fork : process and initiate the hm_listener
#
child_pid = os.fork()
if child_pid == 0:
# 
# initiate : the hm_listener on the CCU in a forked child-process
#
    initiate_hm_listener()
    exit(0)
else:
#
# read : configuration and get the Listener Port
#
    HM_config = ConfigParser.ConfigParser()
    HM_config.read('mm_HM.config')
    HM_ListenerPort = HM_config.get('mmHM_global', 'HM_Listener_Port')
# 
# Instantiate and bind to localhost:HM_ListenerPort
#
    server = AsyncXMLRPCServer(('', int(HM_ListenerPort)), SimpleXMLRPCRequestHandler)
# 
# Register example object instance
#
    server.register_introspection_functions()
    server.register_instance(mm_HM_XMLRPC_Object())
    server.register_multicall_functions()
# 
# run : server in endless loop
#
    try:
       server.serve_forever()
    except KeyboardInterrupt:
       print 'KeyboardInterrupt Exit - don\'t forget to stop sending the events to the gateway! '
#
### END #######################################################################
