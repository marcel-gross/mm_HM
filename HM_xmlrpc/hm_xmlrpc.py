#!/usr/bin/python

import xmlrpclib

# Create an object to represent our server.
server_url = 'http://192.168.2.120:2001';
server = xmlrpclib.Server(server_url);
server_ip_url = 'http://192.168.2.120:2010';
server_ip = xmlrpclib.Server(server_ip_url);

# Call the server and get our result.
result = server.listDevices()
#firmware = result['1']
print result[0]
HM = result[0]
print HM['FIRMWARE']
#print result

hmcmd = server.system.listMethods()
print hmcmd
print "\n"
print server.system.methodHelp('ping')
#
# Heitzkoerper-Thermostat
#
print server.getValue('MEQ0686345:4','ACTUAL_TEMPERATURE')
print server.getValue('MEQ0686345:4','SET_TEMPERATURE')
print server.getValue('MEQ0686345:4','VALVE_STATE')
print server.getValue('MEQ0686345:4','BATTERY_STATE')
#server.setValue('MEQ0686345:4','MANU_MODE', 16.0)
reply = server.setValue('MEQ0686345:4','AUTO_MODE',True)
print "reply: ", reply
#
# Thermostat
#
print "TEMP: ", server.getValue('MEQ1330641:1','TEMPERATURE')
print "HUM.: ", server.getValue('MEQ1330641:1','HUMIDITY')
#server.setValue('MEQ1330641:1','HUMIDITY')
#'boolean':True,
#pinit = server.init('http://192.168.2.118:8000','')
#print "init.:" , pinit

result_ip = server_ip.listDevices()
print result_ip
print "PRES.: ", server_ip.getValue('000C17099A0416:1','PRESENCE_DETECTION_STATE')
