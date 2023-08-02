from fastapi import FastAPI
import boto3
import logging
from EC2 import router as ec2_aws_router
from RDS import router as rds_aws_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(ec2_aws_router, prefix="/ec2")
app.include_router(rds_aws_router, prefix="/rds")



#Get All S3 Buckets
@app.get("/s3/buckets",tags=["S3"])
def get_all_buckets(region: str, aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str):
    s3 = boto3.resource('s3',
                        region_name=region,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token)
    buckets = s3.buckets.all()
    return [bucket.name for bucket in buckets]


