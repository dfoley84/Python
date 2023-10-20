import os
import boto3
import traceback
from sqlalchemy import create_engine, event, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Database:
    def __init__(self, endpoint, db_database, db_user, rds_engine,  aws_region):
        self.endpoint = endpoint
        self.db_database = db_database
        self.db_user = db_user
        self.aws_region = aws_region
        self.rds_engine = rds_engine

        self.config = self.get_config()
        self.engine = self.create_engine()
        self.Session = sessionmaker(bind=self.engine)
        
        # Add event listener for connection
        @event.listens_for(self.engine, "do_connect")
        def provide_token(dialect, conn_rec, cargs, cparams):
            cparams['password'] = self.generate_auth_token()

        
    def get_config(self):
        configs = {
            'mysql': {
                'username': self.db_user,
                'host': self.endpoint,
                'port': 3306,
                'database': self.db_database,
                'charset': 'utf8mb4',
                'url_format': "mysql+pymysql://{username}@{host}:{port}/{database}?charset={charset}"
            },
            'postgres': {
                'username': self.db_user,
                'host': self.endpoint,
                'port': 5432,
                'database': self.db_database,
                'url_format': "postgresql+psycopg2://{username}@{host}:{port}/{database}"
            }
        }

        if self.rds_engine not in configs:
            raise ValueError(f"Unsupported engine: {self.rds_engine}")
        return configs[self.rds_engine]
    

    def create_engine(self):
        engine_url = self.config['url_format'].format(**self.config)
        connect_args = {}
        if self.rds_engine == 'mysql':
            connect_args = {
                'client_flag': 0,
                'ssl': {
                    'ca': 'rds-combined-ca-bundle.pem'
                }
            }
        elif self.rds_engine == 'postgres':
            connect_args = {
                'sslrootcert': 'rds-combined-ca-bundle.pem'
            }
        return create_engine(engine_url, connect_args=connect_args)
       
  
    def generate_auth_token(self):
        session = boto3.session.Session()
        rds = session.client('rds', region_name=self.aws_region)
        auth_token = rds.generate_db_auth_token(DBHostname=self.endpoint, Port=self.config['port'], DBUsername=self.db_user)
        return auth_token
    


    def get_session(self):
        try:
            return self.Session()
        except exc.SQLAlchemyError:
            print("Issue with Connection:", traceback.format_exc())
            return None
