import json
import logging
import os
import re
import time

from ..cloud_storage.cloud_storage import CloudStorage
from ...const.CONST import MAX_DEPTH_LIMIT
from .saver import Saver

logger = logging.getLogger()

class SaverAsJSON(Saver):
    def __init__(self, data, save_path):
        super().__init__(data, save_path)

    def save(self):
        # Save data as a JSON file to a specified path on Google Cloud Bucket
        try:
            invalid_char_regex = r'[^\w/-]'

            # Replace "\" with "/"
            bucket_path = self.save_path.replace('\\', '/')

            # Remove invalid characters
            bucket_path = re.sub(invalid_char_regex, '', bucket_path)  

            # Remove extra "/" characters
            bucket_path = re.sub(r'/+', '/', bucket_path)

            # Limit the depth of the folder structure
            bucket_path_parts = bucket_path.split("/")
            bucket_path_parts = bucket_path_parts[:MAX_DEPTH_LIMIT]
            bucket_path = "/".join(bucket_path_parts)

            upload_dir = f'{bucket_path}-{time.strftime("%Y%m%d-%H%M%S")}.json'
            upload_file = json.dumps(self.data, indent=4, ensure_ascii=False)
            upload_type = 'application/json'

            gcs_service = CloudStorage()
            gcs_service.upload_file(upload_dir, upload_file, upload_type)
        except Exception as e:
            logger.exception("An error occurred while saving the file (JSON): %s", e)
        