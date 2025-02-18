# from ip2geotools.databases.noncommercial import DbIpCity
import json
import pandas as pd
import os

class UserAnalytics:
    def __init__(self):
        self.user_file_path = os.environ.get("USER_FILE_PATH")
        if self.user_file_path is None:
            raise Exception("USER_FILE_PATH environment variable is not set.")
        
        if '.json' not in self.user_file_path:
            raise Exception("The user file needs to be a JSON file.")

        with open(self.user_file_path, 'r') as file:
            user_data = json.load(file)
        
        self.user_data = user_data
    
    def get_account_data(self):
        return self.user_data["account"]

    def get_devices_data(self):
        return self.user_data["devices"]
    
    def get_profile_data(self):
        return self.user_data["profile"] 
    
    def get_preferences_data(self):
        return self.user_data["preferences"]
    
    def get_location_data(self):
        return self.user_data["location"]


# def parse_user_ip_addresses(file_path='data/export/user.json'):
#     """
#     Parses the IP addresses out of  the user data and gets latitude and longitude coordinates from the IP addresses.
#     This is only grabbing a subset of the IP addresses because the full set of data takes too long.
#     :return: a DataFrame with latitude and longitude coordinates
#     """
#     json_file_path = file_path

#     # opening json file
#     with open(json_file_path, 'r') as file:
#         # raw data is a list of dictionaries "list of interactions with a person"
#         raw_data = json.load(file)

#     device_value = []
#     # parse just the device records
#     if 'devices' in raw_data:
#         values = raw_data['devices']
#         device_value = values

#     # extract the IP addresses
#     ip_addresses = [entry['ip_address'] for entry in device_value]

#     lats = []
#     longs = []
#     # lookup the latitude and longitude coordinates of each IP address
#     # TODO: this API call doesn't work super well, replace it
#     # for ip in ip_addresses[:100]:
#     #     coord = DbIpCity.get(ip, api_key="free")
#     #     lats.append(coord.latitude)
#     #     longs.append(coord.longitude)

#     # define column names and create a DataFrame
#     coordinates = pd.DataFrame({'latitude': lats, 'longitude': longs})
#     return coordinates
