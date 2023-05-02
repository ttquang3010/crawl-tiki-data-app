import logging
import os
import re
import time

import pandas

from ..cloud_storage.cloud_storage import CloudStorage
from ...const.CONST import MAX_DEPTH_LIMIT
from .saver import Saver

logger = logging.getLogger()

class SaverAsCSV(Saver):
    def __init__(self, data, save_path):
        super().__init__(data, save_path)

    def save(self):
        # Save data as a CSV file to a specified path on Google Cloud Bucket
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
         
            dataFrame = pandas.DataFrame(self.data)
            upload_file = dataFrame.to_csv(index=False)
            upload_dir = f'{bucket_path}-{time.strftime("%Y%m%d-%H%M%S")}.csv'
            upload_type = 'text/csv'

            gcsService = CloudStorage()
            gcsService.upload_file(upload_dir, upload_file, upload_type)
        except Exception as e:
            logger.exception("An error occurred while uploading the file (CSV): %s", e)