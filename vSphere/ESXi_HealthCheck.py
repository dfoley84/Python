import requests
import json
import getpass
import mysql.connector
import os
import datetime

Servers = []

mydb = mysql.connector.connect(
  host=" ",
  user=" ",
  password="",
  database=""
)

#Remove SQL DataFrom Table
mycursor = mydb.cursor()
mycursor.execute('TRUNCATE TABLE esxi_hosts_reload')

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
            for host in server['hosts']:
                esxi = host['details']['name']
                status = host['status']

                sql = ''' INSERT INTO esxi_hosts_reload(HorizonServer, ESXiName, ESXiStatus) VALUES (%s, %s, %s)'''     
                val = (Server, esxi, status )
                mycursor.execute(sql, val)
                mydb.commit()

    except requests.exceptions.RequestException as err:
        print(err)
        

#Connect to SQL Database
mycursor.execute('''INSERT INTO esxi_hosts(HorizonServer, ESXiName, ESXiStatus)
                            SELECT HorizonServer, ESXiName, ESXiStatus FROM esxi_hosts_reload
                            WHERE NOT EXISTS (Select HorizonServer, ESXiName, ESXiStatus FROM esxi_hosts WHERE esxi_hosts.ESXiName = esxi_hosts_reload.ESXiName)''')
mydb.commit()

mycursor.execute('''UPDATE esxi_hosts
JOIN esxi_hosts_reload
ON  esxi_hosts.ESXiName = esxi_hosts_reload.ESXiName
SET   
esxi_hosts.ESXiStatus = esxi_hosts_reload.ESXiStatus
''')
			
mydb.commit()






