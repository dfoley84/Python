from PyPowerStore import powerstore_conn
import os, sys

user = os.getenv('User')
pwd = os.getenv('Pass')
ip = os.getenv('ipaddress')

lunname = sys.argv[0]

conn = powerstore_conn.PowerStoreConn(user,pwd,ip,False)
volume_create = conn.provisioning.create_volume(name=lunname, size=1073741824)
