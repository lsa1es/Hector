import re
import time
from zabbix_api import ZabbixAPI


zapi = ZabbixAPI(server="")
zapi.login("", "" )


while True:
        time.sleep(30)

	file = []
	for line in open("/etc/zabbix/zabbix_server.conf"):
		if line[0] <> '#':
			file.append(line)

	file_ok = []
	for wspace in file:
		if not re.match(r'^\s*$', wspace):
			line = wspace.replace("\n","")
			file_ok.append(line)


	r = re.compile("StartPollers")
	newlist = filter(r.match, file_ok)
	StartPollers_ConfValue = newlist[0].split("=")[-1]
	#print "StartPollers = %s " % (StartPollers_ConfValue)

	item_get = zapi.item.get({"selectHosts" : "extend" ,"output" : "extend", "filter" : { "key_" : "zabbix[process,poller,avg,busy]" } })
	for x in item_get:
		if x[u'templateid'] <> '0':
			StartPollers_ZbxValue = x[u'lastvalue']
			#print StartPollers_ZbxValue
  
	y = (float(StartPollers_ConfValue) * float(StartPollers_ZbxValue))/100
	print y
	print

#print "Total = %s - 100" % (StartPollers_ConfValue)
#print "Valor Atual: %s " % (StartPollers_ZbxValue)
#print "Qual o Valor de x? "

