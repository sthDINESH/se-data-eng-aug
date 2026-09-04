import json
import boto3
import pprint as pp

# Create client and resource objects
session = boto3.Session(profile_name="se-data-eng")
s3_client = session.client("s3")
s3_resource = session.resource("s3")

# List buckets
bucket_list = s3_client.list_buckets()
# pp.pprint(bucket_list)

# for bucket in bucket_list["Buckets"]:
#     print(bucket["Name"])

bucket_name = "data-eng-resources"
bucket_contents = s3_client.list_objects_v2(
    Bucket=bucket_name
)

# pp.pprint(bucket_contents)
# for object in bucket_contents.all():
#     print(object.Key)

# Read object from bucket
s3_object = s3_client.get_object(
    Bucket=bucket_name,
    Key="python/chatbot-intent.json"
)
# pp.pprint(s3_object, sort_dicts=False)
strbody = s3_object["Body"].read()
# pp.pprint(json.loads(strbody), sort_dicts=False)

# Upload file to S3
s3_client.upload_file(Filename='data.json',
                      Bucket=bucket_name,
                      Key="se-sept-26/test/dinesh.json"
                      )

