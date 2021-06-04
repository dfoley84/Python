import requests
import json
import getpass
import mysql.connector
import os
import datetime

Servers = [ ]

mydb = mysql.connector.connect(
  host=" ",
  user=" ",
  password="",
  database=""
)

#Remove SQL DataFrom Table
mycursor = mydb.cursor()
mycursor.execute('TRUNCATE TABLE connectionserver_datastore_reload')

for Server in Servers:
    print(Server)
    try:
        requests.packages.urllib3.disable_warnings()
        pw = os.getenv('pass')
        domain = os.getenv('domain')
        username =os.getenv('user')
        url = 'https://{}'.format(Server)
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
        }
        data = {"domain": domain, "password": pw, "username": username}
        json_data = json.dumps(data)
        response = requests.post(
            f'{url}/rest/login', verify=False, headers=headers, data=json_data)
        data = response.json()
        access_token = {
            'accept': '*/*',
            'Authorization': 'Bearer ' + data['access_token']
        }

        response = requests.get(f'{url}/rest/monitor/virtual-centers', verify=False, headers=access_token)
        data = response.json()
        for server in data:
            for host in server['datastores']:
                name = host['details']['name']
                path = host['details']['path']
                capcity = host['capacity_mb']
                free = host['free_space_mb']
                status = host['status']
                typestorage = host['type']
     
                sql = '''INSERT INTO connectionserver_datastore_reload(HorizonServer, DataStoreName, DataStorePath, DataStore_Capacity, DataStore_FreeSpace, DataStore_status, DataStore_type  ) VALUES (%s, %s, %s, %s, %s, %s, %s)'''     
                val = (Server, name, path, capcity, free, status, typestorage )
                mycursor.execute(sql, val)
                mydb.commit()

    except requests.exceptions.RequestException as err:
        print(err)

#Connect to SQL Database
mycursor.execute('''INSERT INTO connectionserver_datastore(HorizonServer, DataStoreName, DataStorePath, DataStore_Capacity, DataStore_FreeSpace, DataStore_type, DataStore_status)
                    SELECT HorizonServer, DataStoreName, DataStorePath, DataStore_Capacity, DataStore_FreeSpace, DataStore_type, DataStore_status FROM connectionserver_datastore_reload
                    WHERE NOT EXISTS (SELECT HorizonServer, DataStoreName, DataStorePath, DataStore_Capacity, DataStore_FreeSpace, DataStore_type, DataStore_status FROM connectionserver_datastore WHERE connectionserver_datastore.DataStoreName = connectionserver_datastore_reload.DataStoreName)''')
mydb.commit()


mycursor.execute('''UPDATE connectionserver_datastore
JOIN connectionserver_datastore_reload
ON  connectionserver_datastore.DataStoreName = connectionserver_datastore_reload.DataStoreName
SET   
connectionserver_datastore.DataStore_Capacity = connectionserver_datastore_reload.DataStore_Capacity,
connectionserver_datastore.DataStore_FreeSpace = connectionserver_datastore_reload.DataStore_FreeSpace,
connectionserver_datastore.DataStore_status = connectionserver_datastore_reload.DataStore_status
''')
			
mydb.commit()

