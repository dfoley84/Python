import boto3

REGION = 'eu-west-1'

ec2 = boto3.client('ec2', region_name=REGION)
ec2_resource = boto3.resource('ec2', region_name=REGION)

def Remove_Unused_EBS():
    volumes = ec2.describe_volumes(
        Filters=[
            {
                'Name': 'status',
                'Values': [
                    'available',
                ]
            },
        ])['Volumes']
    for volume in volumes:
        ec2_volume = ec2_resource.Volume(volume['VolumeId'])
        ec2_volume.delete()

def Remove_Unused_Snapshots():
    snapshots = ec2.describe_snapshots(
        Filters=[
            {
                'Name': 'status',
                'Values': [
                    'completed',
                ]
            },
        ])['Snapshots']
    for snapshot in snapshots:
        ec2_snapshot = ec2_resource.Snapshot(snapshot['SnapshotId'])
        ec2_snapshot.delete()


def Remove_Unused_AMI():
    images = ec2.describe_images(
        Filters=[
            {
                'Name': 'state',
                'Values': [
                    'available',
                ]
            },
        ])['Images']
    for image in images:
        ec2_image = ec2_resource.Image(image['ImageId'])
        ec2_image.deregister()



