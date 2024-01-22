'''
import os
import redis
from azure.storage.blob import BlobServiceClient

# Set up Azure Blob Storage connection string and container name
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = 'my-container'

# Set up Redis connection
redis_host = 'localhost'
redis_port = 6379
redis_password = None
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)

# Create BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Get the container client object
container_client = blob_service_client.get_container_client(container_name)

# List all the blobs in the container
blobs_list = container_client.list_blobs()

# Iterate over the blobs and set the blob content to Redis
for blob in blobs_list:
    blob_client = container_client.get_blob_client(blob.name)
    blob_content = blob_client.download_blob().readall()
    redis_client.set(blob.name, blob_content)

print("Data migration completed successfully!")



===============================================

import redis
import io
from azure.storage.blob import BlobServiceClient

# Connect to Redis cache
redis_conn = redis.Redis(host='<your-redis-cache-name>.redis.cache.windows.net', port=6380, ssl=True, password='<your-access-key>')

# Connect to Azure Blob Storage
blob_conn_str = '<your-azure-blob-storage-connection-string>'
blob_service_client = BlobServiceClient.from_connection_string(blob_conn_str)

# Upload a blob to Redis cache
blob_client = blob_service_client.get_blob_client(container='<your-container-name>', blob='<your-blob-name>')
blob_data = blob_client.download_blob().readall()
redis_conn.set('<your-key-name>', blob_data)

# Download a blob from Redis cache
blob_data = redis_conn.get('<your-key-name>')
blob_stream = io.BytesIO(blob_data)
blob_client.upload_blob(data=blob_stream)

==================================================================

'''

import pymongo
import json
# set up the MongoDB client
client = pymongo.MongoClient("mongodb://usndtaxtdacdb09:t2nrMJ4RcgUt2NIlHjnsz0Kypchc3qrkJjrG9KO33mgoyGvTt1KyOt1YQYcQqri4OgwjrQ55m8JEACDbdologA==@usndtaxtdacdb09.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@usndtaxtdacdb09@")

# create a database and collection
mydb = client["TestDB"]
mycol = mydb["customers2"]

# insert a document into the collection
#mydict = { "name": "John", "address": "Highway 37" }

print("===========working")
with open("StatesByCountries.json", "rb") as json_file:
	configData = json.load(json_file)
print(configData)
#x = mycol.insert_one(configData)

if isinstance(configData, list):
    mycol.insert_many(configData) 
else:
    mycol.insert_one(configData)
# print the ID of the inserted document
print(x.inserted_id)
