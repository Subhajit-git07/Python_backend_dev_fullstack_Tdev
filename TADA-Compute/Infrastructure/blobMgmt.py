import os

from azure.storage.blob import BlobServiceClient

from Config import EnvSettings

class blobSettings: 
    def __init__(self):
        blob_connect_str = os.getenv(EnvSettings.saAccessKey)
        self.blob_service_client = BlobServiceClient.from_connection_string(blob_connect_str)

blobSet = blobSettings()