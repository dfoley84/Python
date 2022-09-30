import boto3 


regions = []

for region in regions:
    session = boto3.Session(region_name=region)
    kmskey = session.client('kms')

    #List out KMS keys
    response = kmskey.list_keys()

    for key in response['Keys']:
        keyARN = key['KeyArn']
            #No function to filter between aws managed and customer managed keys
            #Using the Try and Except to filter to continue to next key if the key is aws managed.
        try:
            rotate = kmskey.enable_key_rotation(KeyId=keyARN)
        except:
            print('Key rotation is not enabled for key: ' + keyARN)
            continue

        print(rotate)
        


