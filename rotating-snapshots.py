#!/bin/python3
from calendar import week
import sys
import requests
import datetime
import base64
import re
import os
import time
from datetime import datetime

force=0
usernameio = os.getenv('IONOS_USERNAME')
try:
  usernameio.isascii
except:
  print("Missing Username -> IONOS_USERNAME\n")
  sys.exit(1)
passwordio = os.getenv('IONOS_PASSWORD')
try:
  passwordio.isascii
except:
  print("Missing Password -> IONOS_PASSWORD\n")
  sys.exit(1)
if len(sys.argv) <= 6:
    dcUuid=sys.argv[1]
    volUuid=sys.argv[2]
    name=sys.argv[3]
    frequency=sys.argv[4]
    if len(sys.argv) == 6:
      force=sys.argv[5]
elif sys.argv[1] == "--help":
  print(f"\n  rotating-snapshots.py is a Python script designed to help taking regular snapshots of your servers.\n\n"
  f"  USAGE:\n"
  f"  rotating-snapshots.py Datacenter_UUID Volume_UUIID Server_reference: [name with only alphanum] Frequency: [DWMMQY]  FORCE: [force]\n\n"
  f"    Frequency:\n"
  f"      D     Daily\n"
  f"      W     Weekly\n"
  f"      M     Monthly\n"
  f"      Q     Quarterly\n"
  f"      Y     Yearly\n")
  sys.exit(0)
elif len(sys.argv) >= 6:
  print(f"\n  Too many arguments, expected 4")
  print(f"  rotating-snapshots.py is a Python script designed to help taking regular snapshots of your servers.\n\n"
  f"  USAGE:\n"
  f"  rotating-snapshots.py Datacenter_UUID Volume_UUIID Server_reference: [name with only alphanum] Frequency: [DWMMQY]  FORCE: [force]\n\n"
  f"    Frequency:\n"
  f"      D     Daily\n"
  f"      W     Weekly\n"
  f"      M     Monthly\n"
  f"      Q     Quarterly\n"
  f"      Y     Yearly\n")
  sys.exit(1)
elif len(sys.argv) <+ 5:
  print(f"\n  Too few arguments, expected 4")
  print(f"  rotating-snapshots.py is a Python script designed to help taking regular snapshots of your servers.\n\n"
  f"  USAGE:\n"
  f"  rotating-snapshots.py Datacenter_UUID Volume_UUIID Server_reference: [name with only alphanum] Frequency: [DWMMQY]  FORCE: [force]\n\n"
  f"    Frequency:\n"
  f"      D     Daily\n"
  f"      W     Weekly\n"
  f"      M     Monthly\n"
  f"      Q     Quarterly\n"
  f"      Y     Yearly\n")
  sys.exit(1)

######################
apiEndpoint="https://api.ionos.com/cloudapi/v6"
######################

# Prepare base46 username:password Headers
user_input_usernameandpassword=str(usernameio+":"+passwordio)
message_bytes = user_input_usernameandpassword.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
token = base64_bytes.decode('ascii')
authAcc={"Authorization": "Basic "+token+""}


def rotate_daily(authAcc,volUuid,dcUuid,name,snapshotList):
  # 1 backup every day of the week
  dow=datetime.today().strftime('%a')
  # delete previous snapshot with the same mane and description
  for i in snapshotList['items']:
    namei=i['properties']['name']
    nameM=dow+"-"+name
    snapUuid=i['id']
    description=i['properties']['description']
    if namei == nameM:
      if description == volUuid:
        print(f"Deleting {namei}, {description}")
        url=apiEndpoint+"/snapshots/"+snapUuid
        response=requests.delete(url, headers=authAcc)
  # create snapshot
  url=apiEndpoint+"/datacenters/"+ dcUuid +"/volumes/"+ volUuid +"/create-snapshot"
  dataForCreate={'name': dow+"-"+name,'description':volUuid}
  print(f"{url}, headers={authAcc}, data={dataForCreate}")
  response=requests.post(url, headers=authAcc, data=dataForCreate)
  return response

def rotate_weekly(authAcc,volUuid,dcUuid,name,snapshotList,force):
  # 1 backup for every tyme the day is a multiple of 7
  dom=datetime.today().day
  x=(dom % 7)
  if force == "force":
    x = 0
  if x == 0:
    for i in snapshotList['items']:
      namei=i['properties']['name']
      nameM=str(dom)+"-W-"+name
      snapUuid=i['id']
      description=i['properties']['description']
      if namei == nameM:
        if description == volUuid:
          print(f"Deleting {namei}, {description}")
          url=apiEndpoint+"/snapshots/"+snapUuid
          response=requests.delete(url, headers=authAcc)
    # create snapshot
    url=apiEndpoint+"/datacenters/"+ dcUuid +"/volumes/"+ volUuid +"/create-snapshot"
    dataForCreate={'name': str(dom)+"-W-"+name,'description':volUuid}
    print(f"{url}, headers={authAcc}, data={dataForCreate}")
    response=requests.post(url, headers=authAcc, data=dataForCreate)
  else:
    response="Not this time for Weekly BKP"
  return response

def rotate_monthly(authAcc,volUuid,dcUuid,name,snapshotList,force):
  # 1 backup every 15th of the month
  dom=datetime.today().day
  if force == "force":
    dom = 15
  if dom == 15:
    for i in snapshotList['items']:
      namei=i['properties']['name']
      nameM=str(dom)+"-M-"+name
      snapUuid=i['id']
      description=i['properties']['description']
      if namei == nameM:
        if description == volUuid:
          print(f"Deleting {namei}, {description}")
          url=apiEndpoint+"/snapshots/"+snapUuid
          response=requests.delete(url, headers=authAcc)
    # create snapshot
    url=apiEndpoint+"/datacenters/"+ dcUuid +"/volumes/"+ volUuid +"/create-snapshot"
    dataForCreate={'name': str(dom)+"-M-"+name,'description':volUuid}
    print(f"{url}, headers={authAcc}, data={dataForCreate}")
    response=requests.post(url, headers=authAcc, data=dataForCreate)
  else:
    response="Not this time for Monthly BKP"
  return response

def rotate_quarterly(authAcc,volUuid,dcUuid,name,snapshotList,force):
  # 1 backup every 18th of the last moth of the quarter
  dom=datetime.today().day
  mon=datetime.today().month
  x=(mon % 3)
  if force == "force":
    x = 0
    dom = 18
  if x == 0:
    if dom == 18:
      for i in snapshotList['items']:
        namei=i['properties']['name']
        nameM=str(dom) +"-"+ str(mon) +"-Q-"+name
        snapUuid=i['id']
        description=i['properties']['description']
        if namei == nameM:
          if description == volUuid:
            print(f"Deleting {namei}, {description}")
            url=apiEndpoint+"/snapshots/"+snapUuid
            response=requests.delete(url, headers=authAcc)
      # create snapshot
      url=apiEndpoint+"/datacenters/"+ dcUuid +"/volumes/"+ volUuid +"/create-snapshot"
      dataForCreate={'name': str(dom) +"-"+ str(mon) +"-Q-"+name,'description':volUuid}
      print(f"{url}, headers={authAcc}, data={dataForCreate}")
      response=requests.post(url, headers=authAcc, data=dataForCreate)
  else:
    response="Not this time for Quarterly BKP"
  return response

def rotate_yearly(authAcc,volUuid,dcUuid,name,snapshotList,force):
  # 1 backup every 20th of the 6th month
  dom=datetime.today().day
  mon=datetime.today().month
  if force == "force":
    mon = 6
    dom = 25
  if mon == 6:
    if dom == 25:
      for i in snapshotList['items']:
        namei=i['properties']['name']
        nameM=str(dom) +"-"+ str(mon) +"-Y-"+name
        snapUuid=i['id']
        description=i['properties']['description']
        if namei == nameM:
          if description == volUuid:
            print(f"Deleting {namei}, {description}")
            url=apiEndpoint+"/snapshots/"+snapUuid
            response=requests.delete(url, headers=authAcc)
      # create snapshot
      url=apiEndpoint+"/datacenters/"+ dcUuid +"/volumes/"+ volUuid +"/create-snapshot"
      dataForCreate={'name': str(dom) +"-"+ str(mon) +"-Y-"+name,'description':volUuid}
      print(f"{url}, headers={authAcc}, data={dataForCreate}")
      response=requests.post(url, headers=authAcc, data=dataForCreate)
  else:
    response="Not this time for Yearly BKP"
  return response

# Buld a Snapshot Catalog
def catalog(authAcc):
  url = apiEndpoint+"/snapshots?pretty=true&depth=2"
  response = requests.get(url, headers=authAcc)
  catalogSnap = (response.json())
  return catalogSnap

snapshotList=catalog(authAcc)

if re.search('[D]', frequency) :
  execD=rotate_daily(authAcc,volUuid,dcUuid,name,snapshotList)
  print(f"\n\n{execD}\n")
time.sleep(20)

if re.search('[W]', frequency) :
  execW=rotate_weekly(authAcc,volUuid,dcUuid,name,snapshotList,force)
  print(f"\n\n{execW}\n")
time.sleep(20)

if re.search('[M]', frequency) :
  execM=rotate_monthly(authAcc,volUuid,dcUuid,name,snapshotList,force)
  print(f"\n\n{execM}\n")
time.sleep(20)

if re.search('[Q]', frequency) : 
  execQ=rotate_quarterly(authAcc,volUuid,dcUuid,name,snapshotList,force)
  print(f"\n\n{execQ}\n")
time.sleep(20)

if re.search('[Y]', frequency) : 
  execY=rotate_yearly(authAcc,volUuid,dcUuid,name,snapshotList,force)
  print(f"\n\n{execY}\n")
