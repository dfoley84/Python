import requests,json, getpass
import  datetime
import os
import mysql.connector

Servers = [ ]
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
        
        #Getting Connection Status for Connection Brokers
        response = requests.get(f'{url}/rest/monitor/connection-servers', verify=False,  headers=access_token)
        data = response.json()
        mycursor = mydb.cursor()

        for i in data:
            ConnectionBroker = i["name"]
            Status = i['status']
            sql = ''' INSERT INTO ConnectionServerHealth(HorizonServer, ConnectionBroker, Status) VALUES (%s, %s, %s)
                  ON DUPLICATE KEY UPDATE Status=VALUES(Status)'''
            val = (Server, ConnectionBroker, Status)
            mycursor.execute(sql, val)
            mydb.commit()

        response = requests.get(f'{url}/rest/monitor/event-database', verify=False,  headers=access_token)
        data = response.json()
        DBName = data['details']['server_name']
        DBStatus = data['status']
        sql = ''' INSERT INTO  EventDatabaseHealth(HorizonServer, DBServer, DBStatus) VALUES (%s, %s, %s)
                  ON DUPLICATE KEY UPDATE DBStatus=VALUES(DBStatus)'''
        val = (Server, DBName, DBStatus)
        mycursor.execute(sql, val)
        mydb.commit()

        response = requests.get(f'{url}/rest/monitor/virtual-centers', verify=False, headers=access_token)
        data = response.json()
        for info in data:
           for server in info["connection_servers"]:
            sql = ''' INSERT INTO vCenterHealthStatus(HorizonServer, name, type, status, vCenterName) VALUES (%s, %s, %s, %s, %s)
                      ON DUPLICATE KEY UPDATE status=VALUES(status)'''
            val = (Server, server["name"], "CONNECTION SERVER", server["status"], info["name"])

            mycursor.execute(sql, val)
            mydb.commit()

    except requests.exceptions.RequestException as err:
        print("Issue with Server: {}".format(Server))
        #cursor.execute("INSERT INTO dbo.FailedConnection VALUES (?, ?)", Server, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        #cursor.commit()

