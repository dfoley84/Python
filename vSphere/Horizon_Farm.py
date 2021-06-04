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

mycursor = mydb.cursor()
mycursor.execute('''TRUNCATE horizonfarm''')
mydb.commit()

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
        response = requests.get(f'{url}/rest/inventory/v1/farms', verify=False, headers=access_token)
        data = response.json()
        mycursor = mydb.cursor()
        for i in data:
            try:
                Display = i['display_name']
            except KeyError:
                Display = 'NotSet'
            try:
                enabled = i['enabled']
            except KeyError:
                enabled = 'NotSet'
            try:
                name = i['name']
            except KeyError:
                name = 'NotSet'
            try:
                delete_in_progess = i['settings']['delete_in_progess']
            except KeyError:
                delete_in_progess = 'NotSet'
            try:
                allow_display_protocol_override =  i['settings']['display_protocol_settings']['allow_display_protocol_override']
            except KeyError:
                allow_display_protocol_override = 'NotSet'
            
            try:
                default_display_protocol =  i['settings']['display_protocol_settings']['default_display_protocol']
            except KeyError:
                default_display_protocol = 'NotSet'

            try:
                grid_vgpus_enabled =  i['settings']['display_protocol_settings']['grid_vgpus_enabled']
            except KeyError:
                grid_vgpus_enabled = 'NotSet'

            try:
                html_access_enabled =  i['settings']['display_protocol_settings']['html_access_enabled']
            except KeyError:
                html_access_enabled = 'NotSet'

            try:
                session_collaboration_enabled =  i['settings']['display_protocol_settings']['session_collaboration_enabled']
            except KeyError:
                session_collaboration_enabled = 'NotSet'

            try:
                vgpu_grid_profile =  i['settings']['display_protocol_settings']['vgpu_grid_profile']
            except KeyError:
                vgpu_grid_profile = 'NotSet'

            try:
                custom_script_in_use =  i['settings']['load_balancer_settings']['custom_script_in_use']
            except KeyError:
                custom_script_in_use = 'NotSet'

            try:
                include_session_count =  i['settings']['load_balancer_settings']['lb_metric_settings']['include_session_count']
            except KeyError:
                include_session_count = 'NotSet'

            try:
                disconnected_session_timeout_policy =  i['settings']['session_settings']['disconnected_session_timeout_policy']
            except KeyError:
                disconnected_session_timeout_policy = 'NotSet'

            try:
                empty_session_timeout_minutes =  i['settings']['session_settings']['empty_session_timeout_minutes']
            except KeyError:
                empty_session_timeout_minutes = 'NotSet'

            try:
                empty_session_timeout_policy =  i['settings']['session_settings']['empty_session_timeout_policy']
            except KeyError:
                empty_session_timeout_policy = 'NotSet'

            try:
                logoff_after_timeout =  i['settings']['session_settings']['logoff_after_timeout']
            except KeyError:
                logoff_after_timeout = 'NotSet'
            try:
                pre_launch_session_timeout_minutes =  i['settings']['session_settings']['pre_launch_session_timeout_minutes']
            except KeyError:
                pre_launch_session_timeout_minutes = 'NotSet'

            try:
                pre_launch_session_timeout_policy =  i['settings']['session_settings']['pre_launch_session_timeout_policy']
            except KeyError:
                pre_launch_session_timeout_policy = 'NotSet'
                
            try:
                Farmtype =  i['type']
            except KeyError:
                Farmtype = 'NotSet'


            sql = '''INSERT INTO horizonfarm(HorizonServer,Displayname,enabled,Displaynameid,delete_in_progess,allow_display_protocol_override,default_display_protocol,grid_vgpus_enabled,html_access_enabled,session_collaboration_enabled,vgpu_grid_profile,
                     custom_script_in_use,include_session_count,disconnected_session_timeout_policy,empty_session_timeout_minutes,empty_session_timeout_policy,logoff_after_timeout,pre_launch_session_timeout_minutes,pre_launch_session_timeout_policy,Farmtype) 
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
          
            val = (Server, Display,enabled,name,delete_in_progess,allow_display_protocol_override,default_display_protocol,grid_vgpus_enabled,html_access_enabled,session_collaboration_enabled,
                    vgpu_grid_profile,custom_script_in_use,include_session_count,disconnected_session_timeout_policy,empty_session_timeout_minutes,empty_session_timeout_policy,logoff_after_timeout,
                    pre_launch_session_timeout_minutes,pre_launch_session_timeout_policy,Farmtype)

            mycursor.execute(sql, val)
            mydb.commit()

    except requests.exceptions.RequestException as err:
        print(err)
