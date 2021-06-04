import requests,json, getpass
import pypyodbc
import mysql.connector
import  datetime
import os

Servers = [   ]

mydb = mysql.connector.connect(
  host=" ",
  user=" ",
  password="",
  database=""
)

for Server in Servers:
    print(Server)
    try:
        requests.packages.urllib3.disable_warnings()
        pw = os.getenv('pass')
        domain = os.getenv('domain')
        username =os.getenv('user')
        url= 'https://{}'.format(Server)
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            }
        data = {"domain": domain, "password": pw, "username": username}
        json_data = json.dumps(data)
        response = requests.post(f'{url}/rest/login', verify=False, headers=headers, data=json_data)
        data = response.json()
        access_token = {
            'accept': '*/*',
            'Authorization': 'Bearer ' + data['access_token']
            }
        
        response = requests.get(f'{url}/rest/config/v1/virtual-centers', verify=False,  headers=access_token)
        data = response.json()
        mycursor = mydb.cursor()
        for i in data:
            try:
                ServerName = i['server_name']
                print(ServerName)
            except KeyError:
                ServerName = 'NotSet'
            try:
                UserName = i["user_name"]
            except KeyError:
                UserName = 'NotSet'
            try:
                Version = i["version"]
            except KeyError:
                Version = 'NotSet'
            try:
                Sparse_Reclamation_enabled = i['se_sparse_reclamation_enabled']
            except KeyError:
                Sparse_Reclamation_enabled = 'NotSet'
            try:
                MaxPowerConcurrent = i['limits']['power_operations_limit']
            except KeyError:
                MaxPowerConcurrent = 'NotSet'
            try:
                MaxProvisiong = i['limits']['provisioning_limit']
            except KeyError:
                MaxProvisiong = 'NotSet'
            try:
                Storage = i['storage_accelerator_data']['enabled']
            except KeyError:
                Storage = 'NotSet'

            sql = '''INSERT INTO horizonconnectionserver (HorizonConnection, ServerName, UserName, ServerVersion, SparseReclamation, PowerOperationsLimit, ProvisioningLimit, StorageAcclerator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                      ON DUPLICATE KEY UPDATE ServerVersion=VALUES(ServerVersion), SparseReclamation=VALUES(SparseReclamation), PowerOperationsLimit=VALUES(PowerOperationsLimit), ProvisioningLimit=VALUES(ProvisioningLimit), StorageAcclerator=VALUES(StorageAcclerator)'''
            val = (Server, ServerName, UserName, Version, Sparse_Reclamation_enabled, MaxPowerConcurrent, MaxProvisiong, Storage)

            mycursor.execute(sql, val)
            mydb.commit()

    except requests.exceptions.RequestException as err:
        print("Issue with Server: {}".format(Server))
