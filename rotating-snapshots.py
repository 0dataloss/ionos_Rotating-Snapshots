#!/bin/python3
from calendar import week
from pydoc import describe
import sys
import requests
import datetime
import base64
import os
from datetime import datetime

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
if len(sys.argv) == 4:
    volUuid=sys.argv[1]
    dcUuid=sys.argv[2]
    name=sys.argv[3]
else:
  print(f"\nVolume ID not found")
  sys.exit(1)

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
      #print(nameM, namei)
      #print(description, volUuid)
      if namei == nameM:
        if description == volUuid:
          print(f"Deleting {namei}, {description}")
          url="https://api.ionos.com/cloudapi/v6/snapshots/"+snapUuid
          response=requests.delete(url, headers=authAcc)
    # create snapshot
    url="https://api.ionos.com/cloudapi/v6/datacenters/"+ dcUuid +"/volumes/"+ volUuid +"/create-snapshot"
    dataForCreate={'name': dow+"-"+name,'description':volUuid}
    print(f"{url}, headers={authAcc}, data={dataForCreate}")
    response=requests.post(url, headers=authAcc, data=dataForCreate)
    return response

#def rotate_weekly():
#    # If it is sunday and there are 7 backups, overwrite Sun and create weekly
#
#def rotate_monthly():
#    # If it is the last day of the month create monthly 
# 

# Buld a Snapshot Catalog
def catalog(authAcc):
  url = "https://api.ionos.com/cloudapi/v6/snapshots?pretty=true&depth=2"
  response = requests.get(url, headers=authAcc)
  catalogSnap = (response.json())
  return catalogSnap

snapshotList=catalog(authAcc)
exec=rotate_daily(authAcc,volUuid,dcUuid,name,snapshotList)
print(f"\n\n{exec}\n")
