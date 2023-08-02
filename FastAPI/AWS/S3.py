from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
import boto3
import logging

router = APIRouter()

#Get All S3 Buckets
@router.get("/s3/buckets")
def get_all_buckets(region: str, aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str):
    s3 = boto3.resource('s3',
                        region_name=region,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token)
    buckets = s3.buckets.all()
    return [bucket.name for bucket in buckets]


