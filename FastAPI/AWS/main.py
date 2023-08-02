from fastapi import FastAPI
import boto3
import logging
from EC2 import router as ec2_aws_router
from RDS import router as rds_aws_router
from S3 import router as s3_aws_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(ec2_aws_router, prefix="/ec2", tags=["EC2"])
app.include_router(rds_aws_router, prefix="/rds", tags=["RDS"])
app.include_router(s3_aws_router, prefix="/s3", tags=["S3"])



