# aws_resources.py
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
import boto3
import logging

router = APIRouter()

@router.get("/instances", tags=["EC2"])
def get_all_buckets(region: str, aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str):
    ec2 = boto3.resource('ec2',
                        region_name=region,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token)
    
    instances = ec2.instances.all()
    return [instance.id for instance in instances]

@router.get("/instance/{instance_id}", tags=["EC2"])
def get_instance_details_by_name(region: str, aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str, instance_id: str):
    try:
        ec2 = boto3.resource('ec2',
                        region_name=region,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token)
        
        instance = ec2.Instance(instance_id)
        instance.load()
        instance_name = next((tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'), None)
       
        return {
            "instance_id": instance.id,
            "instance_name": instance_name,
            "instance_status": instance.state['Name'],
            "instance_ip": instance.private_ip_address,
            "instance_type": instance.instance_type,
            "instance_launch_time": instance.launch_time,
            "SecurityGroups": [sg['GroupName'] for sg in instance.security_groups]
        } 
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


        
