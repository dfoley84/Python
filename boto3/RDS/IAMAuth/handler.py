import sys 
from database import Database
import json

ErrorMessage = "Something went wrong: {}"
NoResults = "No results returned; Exiting Script"

def lambda_handler(event, context):
# Configure Environment Variables
    Endpoint = event['Endpoint']
    db_Table = event['DBTABLE']
    db_User = event['DBUser']
    aws_Region = event['REGION']

  
    response = {
        'statusCode': 200,
        'body': 'SSM Document Automation completed successfully.',
        'output': []  # Placeholder for output results
    }

    
    db = Database(Endpoint, db_Table, db_User, aws_Region)
    conn, cur, messages = db.DBConnection()
    if conn is None:
        for message in messages:
            response['output'].append(message)
        response['output'].append({'message': 'Connection Failed'})
        print('Database Connection Failed')
        return response

  try:
    ##SQL Queries 
  
  except Exception as e:
        print('Error Occurred Running Query: {}'.format(e))
        response['output'].append({'message': 'Error Occurred Running Query: {}'.format(e)})
        conn.rollback()  
  finally:
    if conn.open:
      cur.close()
      conn.close()
      response['output'].append({'message': 'MySQL Connection is Closed'})

    





