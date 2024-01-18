#!/bin/bash

# Replace these with your actual S3 bucket and file paths
BUCKET_NAME="divmovie"
SMALL_DATA_PATH="smalldata.parquet"
ALGORITHM_PATH="algorithm.pkl"

# Download smalldata.parquet to the root directory
aws s3 cp s3://$BUCKET_NAME/$SMALL_DATA_PATH smalldata.parquet

# Download algorithm.pkl to the root directory
aws s3 cp s3://$BUCKET_NAME/$ALGORITHM_PATH algorithm.pkl