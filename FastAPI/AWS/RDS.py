# aws_resources.py
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
import boto3
import logging

router = APIRouter()

@router.get("/DBInstances", tags=["RDS"])
def get_all_buckets(region: str, aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str):
    rds = boto3.client('rds',
                        region_name=region,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token)
    
    instances = rds.describe_db_instances()
    return [instance['DBInstanceIdentifier'] for instance in instances['DBInstances']]

#Get All Snapshots
@router.get("/DBSnapshots", tags=["RDS"])
def get_all_buckets(region: str, aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str):
    rds = boto3.client('rds',
                        region_name=region,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token)
    
    instances = rds.describe_db_snapshots()
    return [instance['DBSnapshotIdentifier'] for instance in instances['DBSnapshots']]

