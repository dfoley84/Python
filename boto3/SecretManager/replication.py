import boto3
Session = boto3.Session()

def get_secret(source_region, secret_name):
    client = Session.client('secretsmanager', region_name=source_region)
    try:
        response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        print(f"Error getting secret: {e}")
        return None
    
    if 'SecretString' in response:
        return response['SecretString']
    else:
        print("Binary secret not supported")
        return None


def set_secret(destination_region, secret_name, secret_value):
    client = Session.client('secretsmanager', region_name=destination_region)
    try:
        client.create_secret(Name=secret_name, SecretString=secret_value)
    except Exception as e:
        print(f"Error setting secret: {e}")
        return False
    return True


if __name__ == "__main__":
    source_region = input("Enter the source region: ")
    destination_region = input("Enter the destination region: ")
    NumberofSecrets = int(input("Enter the number of secrets to copy: "))
    SecertsName = []

    for Secerts in range(NumberofSecrets):
        secret_name = input(f"Enter the secret name {Secerts+1}: ")
        SecertsName.append(secret_name)

    for secret_name in SecertsName:
        secret_value = get_secret(source_region, secret_name)
        if secret_value:
            if set_secret(destination_region, secret_name, secret_value):
                print(f"Successfully copied secret {secret_name} from {source_region} to {destination_region}.")
            else:
                print(f"Failed to copy secret {secret_name} to {destination_region}.")
        else:
            print(f"Failed to retrieve secret {secret_name} from {source_region}.")
