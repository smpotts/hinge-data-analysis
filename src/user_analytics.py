from ip2geotools.databases.noncommercial import DbIpCity
import json
import pandas as pd


def parse_user_ip_addresses():
    """
    Parses the IP addresses out of  the user data and gets latitude and longitude coordinates from the IP addresses.
    This is only grabbing a subset of the IP addresses because the full set of data takes too long.
    :return: a DataFrame with latitude and longitude coordinates
    """
    json_file_path = 'data/export/user.json'

    # opening json file
    with open(json_file_path, 'r') as file:
        # raw data is a list of dictionaries "list of interactions with a person"
        raw_data = json.load(file)

    device_value = []
    # parse just the device records
    if 'devices' in raw_data:
        values = raw_data['devices']
        device_value = values

    # extract the IP addresses
    ip_addresses = [entry['ip_address'] for entry in device_value]

    lats = []
    longs = []
    # lookup the latitude and longitude coordinates of each IP address
    for ip in ip_addresses[:100]:
        coord = DbIpCity.get(ip, api_key="free")
        lats.append(coord.latitude)
        longs.append(coord.longitude)

    # define column names and create a DataFrame
    coordinates = pd.DataFrame({'latitude': lats, 'longitude': longs})
    return coordinates
