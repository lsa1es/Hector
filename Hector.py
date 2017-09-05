import re
import time
import os
from zabbix_api import ZabbixAPI


zapi = ZabbixAPI(server="", timeout=30)
zapi.login("", "" )

Pollers_lst = []
PollersUnreachable_lst = []
while True:

	file = []
	for line in open("/etc/zabbix/zabbix_server.conf"):
		if line[0] <> '#':
			file.append(line)

	file_ok = []
	for wspace in file:
		if not re.match(r'^\s*$', wspace):
			line = wspace.replace("\n","")
			file_ok.append(line)

# StartPollers
	r = re.compile("StartPollers")
	newlist = filter(r.match, file_ok)
	StartPollers_ConfValue = newlist[0].split("=")[-1]

	item_get = zapi.item.get({"selectHosts" : "extend" ,"output" : "extend", "filter" : { "key_" : "zabbix[process,poller,avg,busy]" } })
	for x in item_get:
		if x[u'templateid'] <> '0':
			StartPollers_ZbxValue = x[u'lastvalue']
  
	x = float(StartPollers_ConfValue) * float(StartPollers_ZbxValue)/ 100
	Pollers_lst.append(int(x))
	print "Pollers => %s/%s " % (x,StartPollers_ConfValue)
	if len(Pollers_lst) == 5:
		if int(max(Pollers_lst)) * 2 < StartPollers_ConfValue:
			print "Alterar valor StartPollers para: %s " % (int(max(Pollers_lst)) * 2)
			print
			Pollers_lst = []

# StartPollersUnreachable
	r = re.compile("StartPollersUnreachable")
        newlist = filter(r.match, file_ok)
        StartPollersUnreachable_ConfValue = newlist[0].split("=")[-1]

        item_get = zapi.item.get({"selectHosts" : "extend" ,"output" : "extend", "filter" : { "key_" : "zabbix[process,unreachable poller,avg,busy]" } })
        for x in item_get:
                if x[u'templateid'] <> '0':
                        StartPollersUnreachable_ZbxValue = x[u'lastvalue']

        x = float(StartPollersUnreachable_ConfValue) * float(StartPollersUnreachable_ZbxValue)/ 100
	print "Pollers Unreachable => %s/%s " % (x,StartPollersUnreachable_ConfValue)
	if len(PollersUnreachable_lst) == 5:
                if int(max(PollersUnreachable_lst)) * 2 < StartPollersUnreachable_ConfValue:
                        print "Alterar valor StartPollersUnreachable para: %s " % (int(max(PollersUnreachable_lst)) * 2)
			print 
                        PollersUnreachable_lst = []
# StartTrappers
        r = re.compile("StartTrappers")
        newlist = filter(r.match, file_ok)
        StartTrappers_ConfValue = newlist[0].split("=")[-1]

        item_get = zapi.item.get({"selectHosts" : "extend" ,"output" : "extend", "filter" : { "key_" : "zabbix[process,trapper,avg,busy]" } })
        for x in item_get:
                if x[u'templateid'] <> '0':
                        StartTrappers_ZbxValue = x[u'lastvalue']

        x = float(StartTrappers_ConfValue) * float(StartTrappers_ZbxValue)/ 100
        print "StartTrappers => %s/%s " % (x,StartTrappers_ConfValue)

# StartPingers
        r = re.compile("StartPingers")
        newlist = filter(r.match, file_ok)
        StartPingers_ConfValue = newlist[0].split("=")[-1]

        item_get = zapi.item.get({"selectHosts" : "extend" ,"output" : "extend", "filter" : { "key_" : "zabbix[process,icmp pinger,avg,busy]" } })
        for x in item_get:
                if x[u'templateid'] <> '0':
                        StartPingers_ZbxValue = x[u'lastvalue']

        x = float(StartPingers_ConfValue) * float(StartPingers_ZbxValue)/ 100
        print "StartPingers => %s/%s " % (x,StartPingers_ConfValue)

# StartDiscoverers
        r = re.compile("StartDiscoverers")
        newlist = filter(r.match, file_ok)
        StartDiscoverers_ConfValue = newlist[0].split("=")[-1]

        item_get = zapi.item.get({"selectHosts" : "extend" ,"output" : "extend", "filter" : { "key_" : "zabbix[process,discoverer,avg,busy]" } })
        for x in item_get:
                if x[u'templateid'] <> '0':
                        StartDiscoverers_ZbxValue = x[u'lastvalue']

        x = float(StartDiscoverers_ConfValue) * float(StartDiscoverers_ZbxValue)/ 100
        print "StartDiscoverers => %s/%s " % (x,StartDiscoverers_ConfValue)
# StartHTTPPollers
        r = re.compile("StartHTTPPollers")
        newlist = filter(r.match, file_ok)
        StartHTTPPollers_ConfValue = newlist[0].split("=")[-1]

        item_get = zapi.item.get({"selectHosts" : "extend" ,"output" : "extend", "filter" : { "key_" : "zabbix[process,http poller,avg,busy]" } })
        for x in item_get:
                if x[u'templateid'] <> '0':
                        StartHTTPPollers_ZbxValue = x[u'lastvalue']

        x = float(StartHTTPPollers_ConfValue) * float(StartHTTPPollers_ZbxValue)/ 100
        print "StartHTTPPollers => %s/%s " % (x,StartHTTPPollers_ConfValue)
# StartTimers
        r = re.compile("StartTimers")
        newlist = filter(r.match, file_ok)
	if not newlist:
		StartTimers_ConfValue = '1'
        if newlist:
		StartTimers_ConfValue = newlist[0].split("=")[-1]

        item_get = zapi.item.get({"selectHosts" : "extend" ,"output" : "extend", "filter" : { "key_" : "zabbix[process,timer,avg,busy]" } })
        for x in item_get:
                if x[u'templateid'] <> '0':
                        StartTimers_ZbxValue = x[u'lastvalue']

        x = float(StartTimers_ConfValue) * float(StartTimers_ZbxValue)/ 100
        print "StartTimers => %s/%s " % (x,StartTimers_ConfValue)

# StartEscalators
        r = re.compile("StartEscalators")
        newlist = filter(r.match, file_ok)
        StartEscalators_ConfValue = newlist[0].split("=")[-1]

        item_get = zapi.item.get({"selectHosts" : "extend" ,"output" : "extend", "filter" : { "key_" : "zabbix[process,escalator,avg,busy]" } })
        for x in item_get:
                if x[u'templateid'] <> '0':
                        StartEscalators_ZbxValue = x[u'lastvalue']

        x = float(StartEscalators_ConfValue) * float(StartEscalators_ZbxValue)/ 100
        print "StartEscalators => %s/%s " % (x,StartEscalators_ConfValue)

	time.sleep(30)
	print



