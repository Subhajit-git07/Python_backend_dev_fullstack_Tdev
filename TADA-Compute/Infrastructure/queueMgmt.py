import os

from azure.storage.queue import QueueClient, TextBase64EncodePolicy

from Config import EnvSettings

class queueSettings:
    def __init__(self):
        self.blob_connect_str = os.getenv(EnvSettings.saAccessKey)
        
    def get_queue_client(self, queueName: str):
        return QueueClient.from_connection_string(self.blob_connect_str, queueName, 
                                                        message_encode_policy = TextBase64EncodePolicy())

queueSet = queueSettings()