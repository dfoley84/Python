from time import sleep
from sshtunnel import open_tunnel
import paramiko
import pymysql


def SourceRDSInstance():    
    command = [
    'mysqldump --user=Admin --password="%s" -h %s ebdb > /tmp/%s.sql' % (Sourcepwd, SourceRDS, customer)
    ]

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(REMOTE_HOST, username='ec2-user', key_filename='./t.pem')

        for command in command:
            print("running command: {}".format(command))
            stdin , stdout, stderr = ssh.exec_command(command)
            print(stdout.read())
            print(stderr.read())
        ssh.close()

    except Exception as e:    
        print(e)

def DropTable():
    #Drop ebdb table in destination RDS Instance
    with open_tunnel(
        (REMOTE_HOST, 22),
        ssh_username='ec2-user',
        ssh_pkey='./t.pem',
        remote_bind_address=(TargetRDS, 3306)) as server:
        conn = pymysql.connect(host='127.0.0.1', user=TargetUser, port=server.local_bind_port, passwd=Targetpwd)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXIST ebdb")
        print(cur)
        cur.close()

def RestoreDB():
    #Restore ebdb table in destination RDS Instance
    command = [
    'mysql --user=%s --password"%s" -h %s < /tmp/%s.sql' % (TargetUser, Targetpwd, TargetRDS, customer)
    ]
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(REMOTE_HOST, username='ec2-user', key_filename='./t.pem')

        for command in command:
            print("running command: {}".format(command))
            stdin , stdout, stderr = ssh.exec_command(command)
            print(stdout.read())
            print(stderr.read())
        ssh.close()

    except Exception as e:    
        print(e)


if __name__ == '__main__':
    SourceRDS = input('Source RDS Instance: ')
    TargetRDS = input('Target RDS Instance: ')
    
    SourceUser = input('Source RDS User: ')
    TargetUser = input('Target RDS User: ')
    
    Sourcepwd = input('Source RDS Password: ')
    Targetpwd = input('Target RDS Password: ')

    DropTable()
    RestoreDB()





