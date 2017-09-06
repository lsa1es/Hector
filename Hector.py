import re
import time
import os
import sys
from zabbix_api import ZabbixAPI

zapi = ZabbixAPI(server="", timeout=30)
zapi.login("", "")

#HOST = sys.argv[1]
#hId = '9'

# incluir em arquivo - hector_pzbx.cfg
StartDiscoverersDefault = '1'
StartEscalatorsDefault = '1'
StartHTTPPollersDefault = '1'
StartIPMIPollersDefault = '0'
StartJavaPollersDefault = '0'
StartPingersDefault = '1'
StartPollersUnreachableDefault = '1'
StartPollersDefault = '5'
StartProxyPollersDefault = '1'
StartSNMPTrapperDefault = '0'
StartTimersDefault = '1'
StartTrappersDefault = '5'
StartVMwareCollectorsDefault = '0'

qntd_loops = 5

VMwareCollectors_lst = []
Trappers_lst = []
Timers_lst = []
SNMPTrapper_lst = []
Proxy_lst = []
Java_lst = []
IPMI_lst = []
HTTP_lst = []
Escalators_lst = []
Pollers_lst = []
PollersUnreachable_lst = []
Pingers_lst = []
Discoverers_lst = []
lines = []

#hosts = zapi.host.get{("output":"extend", "filter": { "host": HOST } )}
#for x in hosts:
#    hId = x[u'hostid']

while True:
    lines.append('.')

    file = []
    for line in open("zabbix_server.conf"):
        if line[0] <> '#':
            file.append(line)

    file_ok = []
    for wspace in file:
        if not re.match(r'^\s*$', wspace):
            line = wspace.replace("\n", "")
            file_ok.append(line)


    # StartPollers
    r = re.compile("StartPollers")
    newlist = filter(r.match, file_ok)
    if not newlist:
        StartPollers_ConfValue = StartPollersDefault
    if newlist:
        StartPollers_ConfValue = newlist[0].split("=")[-1]
    item_get = zapi.item.get(
        {"selectHosts": "extend", "output": "extend", "filter": {"key_": "zabbix[process,poller,avg,busy]"}})
    for x in item_get:
        if x[u'templateid'] <> '0':
            StartPollers_ZbxValue = x[u'lastvalue']
            x = float(StartPollers_ConfValue) * float(StartPollers_ZbxValue) / 100
            Pollers_lst.append(int(x))
            #print "Pollers => %s/%s " % (x, StartPollers_ConfValue)
            if len(Pollers_lst) == qntd_loops:
                media = sum(Pollers_lst) / len(Pollers_lst)
                print "StartPollers - Media: %s " % (media)
                # 4 - Value Default for StartPollers
                if 4 > (int(max(Pollers_lst)) * 2):
                    print "StartPollers - Keep default configuration"
                    Pollers_lst = []
                elif (int(max(Pollers_lst)) * 2) <> int(StartPollers_ConfValue):
                    print "StartPollers - Change from %s to %s" % (int(StartPollers_ConfValue), (int(max(Pollers_lst)) * 2))
                    print
                    Pollers_lst = []


    # StartPollersUnreachable
    r = re.compile("StartPollersUnreachable")
    newlist = filter(r.match, file_ok)
    if not newlist:
        StartPollers_ConfValue = StartPollersDefault
    if newlist:
        StartPollersUnreachable_ConfValue = newlist[0].split("=")[-1]
    item_get = zapi.item.get({"selectHosts": "extend", "output": "extend",
                              "filter": {"key_": "zabbix[process,unreachable poller,avg,busy]"}})
    for x in item_get:
        if x[u'templateid'] <> '0':
            StartPollersUnreachable_ZbxValue = x[u'lastvalue']
            x = float(StartPollersUnreachable_ConfValue) * float(StartPollersUnreachable_ZbxValue) / 100
            PollersUnreachable_lst.append(int(x))
            #print "Pollers Unreachable => %s/%s " % (x, StartPollersUnreachable_ConfValue)
            if len(PollersUnreachable_lst) == qntd_loops:
                media = sum(PollersUnreachable_lst) / len(PollersUnreachable_lst)
                print "StartPollersUnreachable - Media: %s " % (media)
                # 1 - Value Default for PollersUnreachable
                if StartPollersDefault > (int(max(PollersUnreachable_lst)) * 2):
                    print "StartPollersUnreachable - Keep default configuration"
                    PollersUnreachable_lst = []
                elif int(max(PollersUnreachable_lst)) * 2 <> int(StartPollersUnreachable_ConfValue):
                    print "StartPollersUnreachable - Change to %s from %s " % ((int(max(PollersUnreachable_lst)) * 2),StartPollersUnreachable_ConfValue)
                    print
                    PollersUnreachable_lst = []


    # StartTrappers
    r = re.compile("StartTrappers")
    newlist = filter(r.match, file_ok)
    if not newlist:
        StartTrappers_ConfValue = StartTrappersDefault
    if newlist:
        StartTrappers_ConfValue = newlist[0].split("=")[-1]
    item_get = zapi.item.get(
        {"selectHosts": "extend", "output": "extend", "filter": {"key_": "zabbix[process,trapper,avg,busy]"}})
    for x in item_get:
        if x[u'templateid'] <> '0':
            StartTrappers_ZbxValue = x[u'lastvalue']
            x = float(StartTrappers_ConfValue) * float(StartTrappers_ZbxValue) / 100
            Trappers_lst.append(int(x))
            if len(Trappers_lst) == qntd_loops:
                media = sum(Trappers_lst) / len(Trappers_lst)
                print "StartTrappers - Media: %s " % (media)
                # print "StartTrappers => %s/%s " % (x, StartTrappers_ConfValue)
                # Values Defaults of PollersUnreachable
                if StartTrappersDefault > (int(max(Trappers_lst)) * 2):
                    print "StartTrappers - Keep default configuration"
                    Trappers_lst = []
                elif int(max(Trappers_lst)) * 2 <> int(StartTrappers_ConfValue):
                    print "StartTrappers - Change to %s from %s " % ((int(max(Trappers_lst)) * 2),StartTrappers_ConfValue)
                    print
                    Trappers_lst = []


    # StartPingers
    r = re.compile("StartPingers")
    newlist = filter(r.match, file_ok)
    if not newlist:
        StartPingers_ConfValue = StartPingersDefault
    if newlist:
        StartPingers_ConfValue = newlist[0].split("=")[-1]
    item_get = zapi.item.get(
        {"selectHosts": "extend", "output": "extend", "filter": {"key_": "zabbix[process,icmp pinger,avg,busy]"}})
    for x in item_get:
        if x[u'templateid'] <> '0':
            StartPingers_ZbxValue = x[u'lastvalue']
            x = float(StartPingers_ConfValue) * float(StartPingers_ZbxValue) / 100
            Pingers_lst.append(int(x))
            #print "StartPingers => %s/%s " % (x, StartPingers_ConfValue)
            if len(Pingers_lst) == qntd_loops:
                media = sum(Pingers_lst) / len(Pingers_lst)
                print "StartPingers - Media: %s " % (media)
                # Values default of zabbix
                if StartPingersDefault > (int(max(Pingers_lst)) * 2):
                    print "StartPingers - Keep default configuration"
                    Pingers_lst = []
                elif int(max(Pingers_lst)) * 2 <> int(StartPingers_ConfValue):
                    print "StartPingers - Change to %s from %s " % ((int(max(Pingers_lst)) * 2),StartPingers_ConfValue)
                    print
                    Pingers_lst = []


    # StartDiscoverers
    r = re.compile("StartDiscoverers")
    newlist = filter(r.match, file_ok)
    if not newlist:
        StartDiscoverers_ConfValue = StartDiscoverersDefault
    if newlist:
        StartDiscoverers_ConfValue = newlist[0].split("=")[-1]
    item_get = zapi.item.get(
        {"selectHosts": "extend", "output": "extend", "filter": {"key_": "zabbix[process,discoverer,avg,busy]"}})
    for x in item_get:
        if x[u'templateid'] <> '0':
            StartDiscoverers_ZbxValue = x[u'lastvalue']
            x = float(StartDiscoverers_ConfValue) * float(StartDiscoverers_ZbxValue) / 100
            Discoverers_lst.append(int(x))
            #print "StartDiscoverers => %s/%s " % (x, StartDiscoverers_ConfValue)
            if len(Discoverers_lst) == qntd_loops:
                media = sum(Discoverers_lst) / len(Discoverers_lst)
                print "StartDiscoverers - Media: %s " % (media)
                # Value Default of zabbix
                if StartDiscoverersDefault > (int(max(Discoverers_lst)) * 2):
                    print "StartDiscoverers - Keep default configuration"
                    Discoverers_lst = []
                elif int(max(Discoverers_lst)) * 2 <> int(StartDiscoverers_ConfValue):
                    print "StartDiscoverers - Change to %s from %s " % ((int(max(Discoverers_lst)) * 2),StartDiscoverers_ConfValue)
                    print
                    Discoverers_lst = []

    # StartHTTPPollers
    r = re.compile("StartHTTPPollers")
    newlist = filter(r.match, file_ok)
    if not newlist:
        StartHTTPPollers_ConfValue = StartHTTPPollersDefault
    if newlist:
        StartHTTPPollers_ConfValue = newlist[0].split("=")[-1]
    item_get = zapi.item.get(
        {"selectHosts": "extend", "output": "extend", "filter": {"key_": "zabbix[process,http poller,avg,busy]"}})
    for x in item_get:
        if x[u'templateid'] <> '0':
            StartHTTPPollers_ZbxValue = x[u'lastvalue']
            x = float(StartHTTPPollers_ConfValue) * float(StartHTTPPollers_ZbxValue) / 100
            HTTP_lst.append(int(x))
            #print "StartHTTPPollers => %s/%s " % (x, StartHTTPPollers_ConfValue)
            if len(Discoverers_lst) == qntd_loops:
                media = sum(HTTP_lst) / len(HTTP_lst)
                print "StartHTTPPPollers - Media: %s " % (media)
                # 1 - Values defaults of zabbix
                if StartHTTPPollersDefault > (int(max(HTTP_lst)) * 2):
                    print "StartHTTPPollers - Keep default configuration"
                    HTTP_lst = []
                elif int(max(HTTP_lst)) * 2 <> int(StartHTTPPollers_ConfValue):
                    print "StartHTTPPollers - Change to %s from %s " % ((int(max(HTTP_lst)) * 2),StartHTTPPollers_ConfValue)
                    print
                    HTTP_lst = []

    # StartTimers
    r = re.compile("StartTimers")
    newlist = filter(r.match, file_ok)
    if not newlist:
        StartTimers_ConfValue = StartTimersDefault
    if newlist:
        StartTimers_ConfValue = newlist[0].split("=")[-1]
    item_get = zapi.item.get(
        {"selectHosts": "extend", "output": "extend", "filter": {"key_": "zabbix[process,timer,avg,busy]"}})
    for x in item_get:
        if x[u'templateid'] <> '0':
            StartTimers_ZbxValue = x[u'lastvalue']
            x = float(StartTimers_ConfValue) * float(StartTimers_ZbxValue) / 100
            Timers_lst.append(int(x))
            #print "StartHTTPPollers => %s/%s " % (x, StartHTTPPollers_ConfValue)
            if len(Timers_lst) == qntd_loops:
                media = sum(Timers_lst) / len(Timers_lst)
                print "StartTimers - Media: %s " % (media)
                # Values defauls of zabbix
                if StartTimersDefault > (int(max(Timers_lst)) * 2):
                    print "StartTimers - Keep default configuration"
                    Timers_lst = []
                elif int(max(Timers_lst)) * 2 <> int(StartTimers_ConfValue):
                    print "StartTimers - Change to %s from %s " % ((int(max(Timers_lst)) * 2),StartTimers_ConfValue)
                    print
                    Timers_lst = []

    # StartEscalators
    r = re.compile("StartEscalators")
    newlist = filter(r.match, file_ok)
    if not newlist:
        StartEscalators_ConfValue = StartEscalatorsDefault
    if newlist:
        StartEscalators_ConfValue = newlist[0].split("=")[-1]
    item_get = zapi.item.get(
        {"selectHosts": "extend", "output": "extend", "filter": {"key_": "zabbix[process,escalator,avg,busy]"}})
    for x in item_get:
        if x[u'templateid'] <> '0':
            StartEscalators_ZbxValue = x[u'lastvalue']
            StartEscalators_ZbxDelay = x[u'delay']
            x = float(StartEscalators_ConfValue) * float(StartEscalators_ZbxValue) / 100
            Escalators_lst.append(int(x))
            #print "StartHTTPPollers => %s/%s " % (x, StartHTTPPollers_ConfValue)
            if len(Escalators_lst) == qntd_loops:
                media = sum(Escalators_lst) / len(Escalators_lst)
                print "StartEscalators - Media: %s " % (media)
                # 1 - Values Defaults of zabbix
                if StartEscalatorsDefault > (int(max(Escalators_lst)) * 2):
                    print "StartEscalators - Keep default configuration"
                    Escalators_lst = []
                elif int(max(Escalators_lst)) * 2 <> int(StartEscalators_ConfValue):
                    print "StartEscalators - Change to %s from %s " % ((int(max(Escalators_lst)) * 2),StartEscalators_ConfValue)
                    print
                    Escalators_lst = []

    time.sleep(30)
    if len(lines) ==  qntd_loops:
        print
        lines = []


