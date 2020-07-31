#!/usr/bin/python


import getopt,sys,json,os
import pprint
import requests
import urllib3

urllib3.disable_warnings()
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pyzabbix import ZabbixMetric, ZabbixSender

s=requests.Session()
s.verify=False

# This function is not yet use 
# Declare to add zabbix trap mode in futur
def output_data(endpoint,key,data,out):
   senderCmd = 'zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -s '+endpoint+' -k '+key+' -o \''+json.dumps(data)+'\''
   if(out == "trap"):
       os.system(senderCmd)
   elif(out == "debug"):
       print("DEBUG")
       print(senderCmd)
   elif(out == "console"):
      print json.dumps(data)

# Call Api
# need to be secure
def requestGetSRM(user,password,urlbase,request):
   headers = {'Accept': 'application/json'}
   result=s.get(urlbase+'/'+ request,headers=headers,auth=(user,password),verify=False)
   return json.loads(result.content)
   

def main(argv):
   scheme="https"
   target=''
   port='58443'
   username=''
   password=''
   request=''
   out='console'
   entity=""
   allproperties="acknowledged,acknowledgedAsString,active,activeAsMetric,bunit,category,certainty,closedat,collhost,collinst,count,customer,device,devtype,duration,enterprise,eventDefinition,eventdisplayname,eventname,eventSource,eventstate,eventtext,eventtype,fullmsg,generic,id,impact,inmaintenance,isproblem,isproblemAsString,isroot,lastchangedat,lastchangedatuts,location,name,openedat,openedatAsString,owner,part,partdisplayname,parttype,parttypedisplayname,pltfmgrp,severity,severityAsMetric,severityAsString,sourcedomainname,sourceeventtype,sourceip,systemdefined1,systemdefined2,systemdefined3,systemdefined4,systemdefined5,topN,troubleticketid,unit,univmxip"

   try:
      opts, args = getopt.getopt(argv,"hs:t:p:r:d:o:e:",["scheme=","target=","port=","user=","password=","out=","entity=","request="])
   except getopt.GetoptError:
      print "Error"
      sys.exit(2)
   for opt, arg in opts:
      if opt == "-h":
         print '-c <command> -s <service>'
         print( "port:" + port)
         sys.exit()
      elif opt in ("-t","--target"):
         target = arg
      elif opt in ("-d","--port"):
         port = arg
      elif opt in ("-u","--user"):
         username = arg
      elif opt in ("-p","--password"):
         password  = arg
      elif opt in ("-m","--out"):
          out = arg
      elif opt in ("-e","--entity"):
          entity = arg
      elif opt in ("-r","--request"):
          request = arg
   urlbase=scheme+'://'+target+':'+port+'/APG-REST'
   if(request == "discoverEvents"):         
      zbxkey="srm.Events.discovery"
      response=requestGetSRM(username,password,urlbase,'events/occurrences/values?filter=active%3D%271%27&properties='+allproperties)
      print json.dumps(response['occurrences'])
   elif(request == "EventsInfo"):         
      zbxkey="srm.Events.info["+entity+']'
      filter='id%3D%27'+entity+'%27'
      requete='events/occurrences/values?filter='+filter+'&properties='+allproperties
      response=requestGetSRM(username,password,urlbase,requete)
      item=response['occurrences'][0]
      output=item['properties']
      print json.dumps(output)

main(sys.argv[1:])