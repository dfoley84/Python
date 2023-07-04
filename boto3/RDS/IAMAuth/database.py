import os 
import pymysql
import boto3
import traceback
import json
import base64
import logging


class Database:
    def __init__(self, Endpoint, db_Table, db_User, aws_Region):
        self.Endpoint = Endpoint
        self.db_Table = db_Table
        self.db_User = db_User
        self.aws_Region = aws_Region
        self.config = self.set_config()


    def set_config(self):
        # Create session and rds client
        session = boto3.session.Session()
        rds = session.client('rds', region_name=self.aws_Region)
        
        # Generate auth token
        auth_token = rds.generate_db_auth_token(DBHostname=self.Endpoint, Port=3306, DBUsername=self.db_User)
        print('auth_token: {}'.format(auth_token))

        config = {
            'user': self.db_User,
            'password': auth_token,
            'ssl': {'ca': 'rds-combined-ca-bundle.pem'},
            'host': self.Endpoint,
            'database': self.db_Table,
            'port': 3306,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'autocommit': False
        }
        return config
    
    def DBConnection(self):
        messages = []
        conn = None
        cursor = None
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            return conn, cursor, messages
        except pymysql.MySQLError as err:
            print("Something went wrong:", traceback.format_exc())
            messages.append({'message': "Something went wrong:"+ traceback.format_exc()})
            return conn, cursor, messages

