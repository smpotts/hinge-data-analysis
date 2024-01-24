from ip2geotools.databases.noncommercial import DbIpCity
import json
import pandas as pd


def parse_user_ip_addresses():
    json_file_path = 'data/export/user.json'

    # opening json file
    with open(json_file_path, 'r') as file:
        # raw data is a list of dictionaries "list of interactions with a person"
        raw_data = json.load(file)

    device_value = []
    if 'devices' in raw_data:
        values = raw_data['devices']
        device_value = values

    ip_addresses = [entry['ip_address'] for entry in device_value]

    lats = []
    longs = []
    for ip in ip_addresses[:50]:
        coord = DbIpCity.get(ip, api_key="free")
        lats.append(coord.latitude)
        longs.append(coord.longitude)

    # define column names and create a DataFrame
    coordinates = pd.DataFrame({'latitude': lats, 'longitude': longs})
    print(coordinates.to_string())
    return coordinates
