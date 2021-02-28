endpoint=http://localhost:4566
resources_env=--endpoint-url=$(endpoint) --region us-east-1 --profile localstack
table_name=fake-table
queue_name=fake-queue
bucket_name=fake-bucket


cdk-shell:
	docker-compose run --rm $(CDK_SERVICE) /bin/bash

localstack:
	docker run --rm -p 4566:4566 -p 4571:4571 -e SERVICES=dynamodb,s3,sqs,lambda localstack/localstack

local_set_up:
	# Table
	aws dynamodb create-table \
		--table-name $(table_name) \
		--attribute-definitions \
			AttributeName=pk,AttributeType=S \
			AttributeName=sk,AttributeType=S \
		--key-schema \
			AttributeName=pk,KeyType=HASH \
			AttributeName=sk,KeyType=RANGE \
		--provisioned-throughput \
			ReadCapacityUnits=10,WriteCapacityUnits=5 \
		$(resources_env)

	# bucket
	aws s3api create-bucket --bucket $(bucket_name) --region us-east-1 \
		$(resources_env)

	# queue
	aws sqs create-queue --queue-name $(queue_name) $(resources_env)

pytest:
	IS_LOCAL=1 POWERTOOLS_TRACE_DISABLED=1 pytest

list_resources:
	aws dynamodb list-tables $(resources_env)
	aws s3api list-buckets $(resources_env)
	aws sqs list-queues $(resources_env)

dynamo_scan:
	aws dynamodb scan --table-name $(table_name) $(resources_env)

sqs_receive_messages:
	aws  sqs receive-message  --queue-url $(endpoint)/000000000000/$(queue_name) $(resources_env)

s3_objects:
	aws s3api list-objects --bucket $(bucket_name) $(resources_env)
