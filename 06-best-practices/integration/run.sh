#!/usr/bin/env bash

docker-compose up -d

sleep 10

export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
export S3_ENDPOINT_URL="http://localhost:4566" 

aws --endpoint-url $S3_ENDPOINT_URL s3 mb s3://nyc-duration

pipenv run python -c'import integration_test; integration_test.prepare_test_data(2023, 1)'

ERROR_CODE=$?
if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

aws --endpoint-url $S3_ENDPOINT_URL s3 ls s3://nyc-duration/in/

(cd ..; pipenv run python batch.py)

ERROR_CODE=$?
if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

aws --endpoint-url $S3_ENDPOINT_URL s3 ls s3://nyc-duration/out/

docker-compose down