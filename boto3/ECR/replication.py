import boto3
Session = boto3.Session()

def get_registry(source_region):
    ecr = Session.client('ecr', region_name=source_region)
    try:
        response = ecr.describe_registry()
    except Exception as e:
        print(f"Error getting replication configuration: {e}")
        return None
    
    if 'replicationConfiguration' in response:
        return response['replicationConfiguration']
    else:
        print("No replication configuration found")
    return response

def set_registry(source_region, destination_region, replication_config,account_id):
    ecr = Session.client('ecr', region_name=source_region)

    Rule = {
        'region': destination_region,
        'registryId': account_id
    }


    if 'rules' in replication_config:
        if replication_config['rules']:
            if 'destinations' in replication_config['rules'][0]:
                replication_config['rules'][0]['destinations'].append(Rule)
            else:
                replication_config['rules'][0]['destinations'] = [Rule]
        else: 
            new_rule = {'destinations': [Rule]}
            replication_config['rules'] = [new_rule]
    else: 
        new_rule = {'destinations': [Rule]}
        replication_config['rules'] = [new_rule]
        
    try:
        ecr.put_replication_configuration(
            replicationConfiguration=replication_config
        )
        print(f"Successfully udpated replication configuration added region: {destination_region}.")
    except Exception as e:
        print(f"Error setting replication configuration: {e}")
        return False
    return True


if __name__ == "__main__":
    source_region = input("Enter the source region: ")
    destination_region = input("Enter the destination region: ")
    account_id = input("Enter the account ID: ")
    
    replication_config = get_registry(source_region)
    if replication_config:
        print(replication_config)
        set_registry(source_region, destination_region, replication_config,account_id)
    else:
        print(f"Failed to retrieve replication configuration from {source_region}.")
