from sshtunnel import open_tunnel
from time import sleep
import pymysql

REMOTE_HOST = ''
DB_HOST = '.rds.amazonaws.com'

# SSH Tunnel
with open_tunnel(
    (REMOTE_HOST, 22),
    ssh_username='',
    ssh_pkey='',
    remote_bind_address=(DB_HOST, 3306)) as server:

    conn = pymysql.connect(host='127.0.0.1', user='', port=server.local_bind_port, passwd='', db='')
    cur = conn.cursor()
    cur.execute("SELECT * FROM <> ")
    print(cur.fetchall())
    conn.close()

 

                           
