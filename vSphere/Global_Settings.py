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

for Server in Servers:
    print(Server)
    try:
        requests.packages.urllib3.disable_warnings()
        pw = os.getenv('pass')
        domain = os.getenv('domain')
        username =  os.getenv('user')
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

        # Getting Connection Status for Connection Brokers
        response = requests.get(
            f'{url}/rest/config/v1/settings/general', verify=False,  headers=access_token)
        data = response.json()
        mycursor = mydb.cursor()

        block_restricted_clients = data['block_restricted_clients'] if "block_restricted_clients" in data else "NotSet"
        client_idle_session_timeout_minutes = data['client_idle_session_timeout_minutes'] if "'client_idle_session_timeout_minutes" in data else "NotSet"
        client_idle_session_timeout_policy = data['client_idle_session_timeout_policy'] if "client_idle_session_timeout_policy" in data else "NotSet"
        client_max_session_timeout_minutes = data['client_max_session_timeout_minutes'] if "client_max_session_timeout_minutes" in data else "NotSet"
        client_max_session_timeout_policy = data['client_max_session_timeout_policy'] if "client_max_session_timeout_policy" in data else "NotSet"
        client_session_timeout_minutes = data['client_session_timeout_minutes'] if "client_session_timeout_minutes" in data else "NotSet"
        console_session_timeout_minutes = data['console_session_timeout_minutes'] if "console_session_timeout_minutes" in data else "NotSet"
        display_pre_login_message = data['display_pre_login_message'] if "display_pre_login_message" in data else "NotSet"
        display_warning_before_forced_logoff = data['display_warning_before_forced_logoff'] if "display_warning_before_forced_logoff" in data else "NotSet"
        enable_automatic_status_updates = data['enable_automatic_status_updates'] if "enable_automatic_status_updates" in data else "NotSet"
        enable_credential_cleanup_for_htmlaccess = data['enable_credential_cleanup_for_htmlaccess'] if "enable_credential_cleanup_for_htmlaccess" in data else "NotSet"
        enable_multi_factor_re_authentication = data['enable_multi_factor_re_authentication'] if "enable_multi_factor_re_authentication" in data else "NotSet"
        enable_sending_domain_list = data['enable_sending_domain_list'] if "enable_sending_domain_list" in data else "NotSet"
        enable_server_in_single_user_mode = data['enable_server_in_single_user_mode'] if "enable_server_in_single_user_mode" in data else "NotSet"
        forced_logoff_message = data['forced_logoff_message'] if "forced_logoff_message" in data else "NotSet"
        forced_logoff_timeout_minutes = data['forced_logoff_timeout_minutes'] if "forced_logoff_timeout_minutes" in data else "NotSet"
        hide_domain_list_in_client = data['hide_domain_list_in_client'] if "hide_domain_list_in_client" in data else "NotSet"
        hide_server_information_in_client = data['hide_server_information_in_client'] if "hide_server_information_in_client" in data else "NotSet"
        machine_sso_timeout_minutes = data['machine_sso_timeout_minutes'] if "machine_sso_timeout_minutes" in data else "NotSet"
        machine_sso_timeout_policy = data['machine_sso_timeout_policy'] if "machine_sso_timeout_policy" in data else "NotSet"
        pre_login_message = data['pre_login_message'] if "pre_login_message" in data else "NotSet"
        restricted_client_message = data['restricted_client_message'] if "restricted_client_message" in data else "NotSet"
        store_cal_on_client = data['store_cal_on_client'] if "store_cal_on_client" in data else "NotSet"
        store_cal_on_connection_server = data['store_cal_on_connection_server'] if "store_cal_on_connection_server" in data else "NotSet"

        sql = '''INSERT INTO GlobalSettings (HorizonServer,client_idle_session_timeout_policy,client_max_session_timeout_minutes,client_max_session_timeout_policy,client_session_timeout_minutes,console_session_timeout_minutes,display_pre_login_message,display_warning_before_forced_logoff,enable_automatic_status_updates,enable_credential_cleanup_for_htmlaccess,enable_multi_factor_re_authentication,enable_sending_domain_list,enable_server_in_single_user_mode,forced_logoff_message,forced_logoff_timeout_minutes,hide_domain_list_in_client,hide_server_information_in_client,machine_sso_timeout_minutes,machine_sso_timeout_policy,store_cal_on_client,store_cal_on_connection_server) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                 ON DUPLICATE KEY UPDATE client_idle_session_timeout_policy=VALUES(client_idle_session_timeout_policy), client_max_session_timeout_minutes=VALUES(client_max_session_timeout_minutes), client_max_session_timeout_policy=VALUES(client_max_session_timeout_policy),
                      client_session_timeout_minutes=VALUES(client_session_timeout_minutes), console_session_timeout_minutes=VALUES(console_session_timeout_minutes), display_pre_login_message=VALUES(display_pre_login_message), display_warning_before_forced_logoff=VALUES(display_warning_before_forced_logoff),
                      enable_automatic_status_updates=VALUES(enable_automatic_status_updates), enable_credential_cleanup_for_htmlaccess=VALUES(enable_credential_cleanup_for_htmlaccess), enable_multi_factor_re_authentication=VALUES(enable_multi_factor_re_authentication), enable_sending_domain_list=VALUES(enable_sending_domain_list),
                      enable_server_in_single_user_mode=VALUES(enable_server_in_single_user_mode), forced_logoff_message=VALUES(forced_logoff_message), forced_logoff_timeout_minutes=VALUES(forced_logoff_timeout_minutes), hide_domain_list_in_client=VALUES(hide_domain_list_in_client), hide_server_information_in_client=VALUES(hide_server_information_in_client),
                      machine_sso_timeout_minutes=VALUES(machine_sso_timeout_minutes), machine_sso_timeout_policy=VALUES(machine_sso_timeout_policy),store_cal_on_client=VALUES(store_cal_on_client), store_cal_on_connection_server=VALUES(store_cal_on_connection_server) '''
        
        val = (Server,client_idle_session_timeout_policy,client_max_session_timeout_minutes,client_max_session_timeout_policy,client_session_timeout_minutes,console_session_timeout_minutes,display_pre_login_message,display_warning_before_forced_logoff,enable_automatic_status_updates,enable_credential_cleanup_for_htmlaccess,enable_multi_factor_re_authentication,enable_sending_domain_list,enable_server_in_single_user_mode,forced_logoff_message,forced_logoff_timeout_minutes,hide_domain_list_in_client,hide_server_information_in_client,machine_sso_timeout_minutes,machine_sso_timeout_policy,store_cal_on_client,store_cal_on_connection_server)

        mycursor.execute(sql, val)
        mydb.commit()

    except requests.exceptions.RequestException as err:
        print(err)
