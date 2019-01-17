import requests
import json
import sys
import collections
import base64
from base64 import *
import sys

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

url1="https://10.250.1.208/api/authentication/login"

Payload = {
  "email": "softwaresupport@vaeit.com",
  "password": "w72P2Q6iM9bk7fO&",
  "remember_me": True
}

headers =  {"Content-Type": "application/json-patch+json"}

response1=requests.post(url1, data=json.dumps(Payload), verify=False, headers=headers)
cookie=response1.cookies

url2="https://10.250.1.208/api/task-status/aggregations"
response2=requests.get(url2, cookies=cookie, verify=False)

j=json.loads(response2.text)
agg_list=[i['aggregation_id'] for i in j]

for agg_id in agg_list:
 url3="https://10.250.1.208/api/task-status/aggregations/{}".format(agg_id)
 response3=requests.get(url3, cookies=cookie, verify=False)

j1=json.loads(response3.text)
task_list=[i['task_id'] for i in j1]

massive_list=[]
massive_dict={}
event_list=[]

for tsk_id in task_list:
 if tsk_id:
   url4="https://10.250.1.208/api/task-status/tasks/{}/events".format(tsk_id)
#   print url4
   response4=requests.get(url4, cookies=cookie, verify=False)
   massive_list.append(response4.json())
   massive_dict[tsk_id]=response4.json()
   for z in massive_list:
    event_list.append(z[0]['event_name'])

counter=collections.Counter(event_list)
print counter 

msg_details_list=[i[0]['message_details'] for i in massive_list]
print len(msg_details_list)


genius=['ARPEntry','InterfaceIP','InterfaceStatus','RouteTable','HardwareInventory','NodeInterface','NodeConfiguration']

f64=open('base64_output_parse', 'w')

#sys.stdout=f64
#print massive_list

ss = [b64decode(json.loads(ii['message_details'])['output']) for ii in i for i in massive_list if ii['event_name'] == 'device_parsed']
print ss


for s in ss: print "======================", s

for i in massive_list:
  for ii in i:
#    if ii['time'].startswith('2018-10-'): 
#    if ii['time'].startswith('2018-10-4') \
     if ii['event_name'] == 'device_parsed':
      print "==================", json.loads(ii['message_details'])['host'], "\n", b64decode(json.loads(ii['message_details'])['output'])
