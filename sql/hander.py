import boto3
from database import Database
from sqlalchemy import text, exc

def lambda_handler(event, context):
    # Extract parameters from the event
    rds_endpoint = event['Endpoint']
    db_database = event['DBTABLE']
    db_user = event['DBUser']
    sql_query = event['SQLQuery']
    rds_engine = event['rds_engine']
    ssm_automation_id = event['Execution']
    aws_region = boto3.session.Session().region_name

  
    # Initialize response structure
    response = {
        'statusCode': 200,
        'body': 'SSM Document Automation completed successfully.',
        'output': []  # Placeholder for output results
    }


    db = Database(rds_endpoint, db_database, db_user, rds_engine, aws_region)
    session = db.get_session()
    

    if session is None:
        response['output'].append({'message': 'Database Connection Failed'})
        print('Database Connection Failed')
        return response

    # Split the SQL query by semicolon
    query_list = [q.strip() for q in sql_query.split(';') if q.strip()]

    #loop through the queries and execute them
    for query in query_list:
        query_response = execute_query(session, query, ssm_automation_id)
        response['output'].append(query_response)

    # Close the database session
    session.close()
    return response

def execute_query(session, query, ssm_automation_id):
    response = {
        'statusCode': 200,
        'body': 'Query executed successfully.',
        'output': []
    }

    try:
        if "SELECT" in query.upper():
            result = session.execute(text(query)).fetchall()
            for row in result:
                response['output'].append({'message': row})
        else:
            result = session.execute(text(query))
            session.commit()
            changed_rows = result.rowcount
            response['output'].append({'message': f'{changed_rows} rows affected.'})

    except exc.SQLAlchemyError as e:
        session.rollback()
        response['statusCode'] = 500
        response['body'] = 'There was an error processing the request.'
        response['output'].append({'message': str(e)})

        
        ssm_client = boto3.client('ssm', boto3.session.Session().region_name)
        ssm_client.send_automation_signal(
            AutomationExecutionId=ssm_automation_id,
            SignalType='StopStep',
            Payload={
                'FailureMessage': str(e)
            }
        )
        
    finally:
        if session is not None:
            session.close()
    
    return response
      
