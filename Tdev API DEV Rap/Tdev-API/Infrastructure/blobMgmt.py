import json
from azure.storage.blob import BlobServiceClient
from config import settings

class blobSettings:
	def __init__(self):
		blob_connect_str = settings.saAccessKey
		self.blob_service_client = BlobServiceClient.from_connection_string(blob_connect_str)

	def uploadToBlob(self, data, file_path):
		blobClient = blobSet.blob_service_client.get_blob_client(container="cache", blob=file_path)
		blobClient.upload_blob(json.dumps(data, ensure_ascii=False, indent=4), overwrite = True)
        
blobSet = blobSettings()