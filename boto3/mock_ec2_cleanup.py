import unittest
import boto3
from moto import mock_ec2

class TestEC2Removal(unittest.TestCase):

    @mock_ec2
    def test_remove_unused_EBS(self):
        REGION = 'eu-west-1'

        ec2 = boto3.client('ec2', region_name=REGION)
        ec2_resource = boto3.resource('ec2', region_name=REGION)

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
            print(f"Deleting volume: {volume['VolumeId']}")
            ec2_volume.delete()
            print(f"Deleted volume: {volume['VolumeId']}")

    @mock_ec2
    def test_remove_unused_snapshots(self):
        REGION = 'eu-west-1'

        ec2 = boto3.client('ec2', region_name=REGION)
        ec2_resource = boto3.resource('ec2', region_name=REGION)

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
            try:
                ec2_snapshot = ec2_resource.Snapshot(snapshot['SnapshotId'])
                print(f"Deleting snapshot: {snapshot['SnapshotId']}")
                ec2_snapshot.delete()
                print(f"Deleted snapshot: {snapshot['SnapshotId']}")
            except Exception as e:
                print(e)
                continue

    @mock_ec2
    def test_remove_unused_AMI(self):
        REGION = 'eu-west-1'

        ec2 = boto3.client('ec2', region_name=REGION)
        ec2_resource = boto3.resource('ec2', region_name=REGION)

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
            print(f"Deregistering image: {image['ImageId']}")
            ec2_image.deregister()
            print(f"Deregistered image: {image['ImageId']}")

if __name__ == "__main__":
    unittest.main()
