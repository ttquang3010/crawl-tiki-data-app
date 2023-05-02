from datetime import datetime
from google.cloud import storage
import logging

logger = logging.getLogger()

class CloudStorage():
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket('project1-quangtt')
    
    def upload_file(self, upload_dir, upload_file, upload_type):
        try:
            # Upload a file to a specified directory in a cloud storage bucket.
            self.bucket.blob(upload_dir).upload_from_string(upload_file, upload_type)
        except Exception as e:
            logger.exception("An error occurred during the upload process: %s", e)