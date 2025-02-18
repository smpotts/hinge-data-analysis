import os
import json

from app.tools.Logger import logger

class UserImporter:
    def __init__(self):
        self.user_file_path = os.environ.get("USER_FILE_PATH")
        if self.user_file_path is None:
            raise Exception("USER_FILE_PATH environment variable is not set.")
        
        if '.json' not in self.user_file_path:
            raise Exception("The user file needs to be a JSON file.")

        with open(self.user_file_path, 'r') as file:
            user_data = json.load(file)
            logger.info(f"Imported user data from {self.user_file_path}.")
        
        self.user_data = user_data