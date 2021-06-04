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

for Server in Servers:
    print(Server)
    try:
        requests.packages.urllib3.disable_warnings()
        pw = os.getenv('pass')
        domain = os.getenv('domain')
        username = os.getenv('user')
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

        response = requests.get(
            f'{url}/rest/inventory/v1/desktop-pools', verify=False, headers=access_token)
        data = response.json()
        mycursor = mydb.cursor()
        print(data)
        for pool in data:
          pool_name = pool['name']
          try:
              max_monitors = int(pool['settings']['display_protocol_settings']['max_number_of_monitors'])
          except KeyError:
              max_monitors = 0
          enable_provisioning = 0 if pool['enabled'] == "False" else 1
          allow_reset = 0 if pool['settings']['session_settings']['allow_users_to_reset_machines'] == "False" else 1
          default_display_protocol = pool[ 'settings']['display_protocol_settings']['default_display_protocol']
          power_policy = pool['settings']['session_settings']['power_policy']
          max_resolution = pool['settings']['display_protocol_settings']['max_resolution_of_any_one_monitor'] if 'max_resolution_of_any_one_monitor' in pool['settings']['display_protocol_settings'].keys() else "Not Present"

          sql = ''' INSERT INTO HorizonPoolConfiguration(HorizonServer, DisplayName, MaxMonitors, EnableProvisioning, AllowReset, DefaultDisplayProtocol, PowerPolicy, MaxResolution) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE  MaxMonitors=VALUES(MaxMonitors), EnableProvisioning=VALUES(EnableProvisioning), AllowReset=VALUES(AllowReset), DefaultDisplayProtocol=VALUES(DefaultDisplayProtocol), PowerPolicy=VALUES(PowerPolicy), MaxResolution=VALUES(MaxResolution) '''
          val = (Server , pool_name, max_monitors, enable_provisioning, allow_reset,default_display_protocol, power_policy, max_resolution)
          mycursor.execute(sql, val)
          mydb.commit()
    except requests.exceptions.RequestException as err:
        print(err)
