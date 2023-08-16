from bucket import BucketPolicy, create_bucket


if __name__ == "__main__":
    bucket_name = "Test"  # Replace with your bucket name
    region = "eu-west-1"  # Replace with your desired region

    if create_bucket(bucket_name, region):
        print(f"Bucket '{bucket_name}' created successfully!")

        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "ForceSSLOnlyAccess",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:*",
                    "Resource": [
                        f"arn:aws:s3:::{bucket_name}/*",
                        f"arn:aws:s3:::{bucket_name}"
                    ],
                    "Condition": {
                        "Bool": {
                            "aws:SecureTransport": "false"
                        }
                    }
                }
            ]
        }

        bucket_policy_manager = BucketPolicy(bucket_name, bucket_policy)
        bucket_policy_manager.apply_policy()
        bucket_policy_manager.block_public_access()
        
        print(f"Applied bucket policy to '{bucket_name}' successfully!")
    else:
        print("Bucket creation failed.")
