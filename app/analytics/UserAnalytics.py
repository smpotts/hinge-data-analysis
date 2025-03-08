from datetime import datetime
from collections import defaultdict
import json
import os

class UserAnalytics:
    def __init__(self):
        self.assets_path = os.environ.get("ASSETS_PATH")
        self.user_file_path = os.environ.get("USER_FILE_PATH")
        if self.user_file_path is None:
            raise Exception("USER_FILE_PATH environment variable is not set.")
        
        if '.json' not in self.user_file_path:
            raise Exception("The user file needs to be a JSON file.")

        with open(self.user_file_path, 'r') as file:
            user_data = json.load(file)
        
        self.user_data = user_data

    def get_media_file_paths(self):
        assets_dir = self.assets_path
        jpg_files = [f for f in os.listdir(assets_dir) if f.endswith(".jpg")]
        return jpg_files
    
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

    def build_user_location_dict(self):
        location = self.get_location_data()
        user_location = {}

        user_location["city"] = location["sublocality"]
        user_location["latitude"] = location["latitude"]
        user_location["longitude"] = location["longitude"]
        user_location["country"] = location["country"]
        user_location["neighborhood"] = location["neighborhood"]
        user_location["locality"] = location["locality"]

        return user_location

    def build_user_summary_dict(self):
        profile_data = self.get_profile_data()
        account_data = self.get_account_data()
        user_summary = {}

        # get profile data
        user_summary["first_name"] = profile_data["first_name"]
        user_summary["age"] = profile_data["age"]
        # convert height in cm to inches and ft
        feet, inches = _convert_height(profile_data["height_centimeters"])
        user_summary["height_feet"] = feet
        user_summary["height_inches"] = inches
        user_summary["gender"] = profile_data["gender"]
        user_summary["ethnicities"] = profile_data["ethnicities"]
        user_summary["religions"] = profile_data["religions"]
        user_summary["job_title"] = profile_data["job_title"]
        user_summary["workplaces"] = profile_data["workplaces"]
        user_summary["education_attained"] = profile_data["education_attained"]
        user_summary["hometowns"] = profile_data["hometowns"]
        user_summary["languages_spoken"] = profile_data["languages_spoken"]
        user_summary["politics"] = profile_data["politics"]
        user_summary["pets"] = profile_data["pets"]
        user_summary["relationship_types"] = profile_data["relationship_types"]
        user_summary["dating_intention"] = profile_data["dating_intention"]

        # capture duration paused and on app time
        user_summary["last_pause_duration"] = _timestamp_durations(
            leading_timestamp=account_data["last_unpause_time"],
            lagging_timestamp=account_data["last_pause_time"])
        
        user_summary["on_app_duration"] = _timestamp_durations(
            leading_timestamp=account_data["last_seen"],
            lagging_timestamp=account_data["signup_time"],
            lag_has_microseconds=True)

        return user_summary
    
    def profile_preference_selections(self):
        profile_data = self.get_profile_data()
        preference_data = self.get_preferences_data()

        profile_fields = ["religions", "ethnicities", "smoking", "drinking", "marijuana", "drugs", "children", "family_plans", "education_attained", "politics"] 
        preference_fields = ["religion_preference", "ethnicity_preference", "smoking_preference", "drinking_preference", "marijuana_preference", "drugs_preference", "children_preference", "family_plans_preference", "education_attained_preference", "politics_preference"]

        profile_values = [profile_data[field] for field in profile_fields if field in profile_data]
        preference_values = [preference_data[field] for field in preference_fields if field in preference_data]

        return profile_values, preference_values
    
    def count_displayed_attributes(self):
        profile_data = self.get_profile_data()
        
        categories = {
            "identity": ["gender_identity_displayed", "ethnicities_displayed", "religions_displayed", "politics_displayed", "languages_spoken_displayed", "hometowns_displayed"],
            "lifestyle": ["smoking_displayed", "drinking_displayed", "marijuana_displayed", "drugs_displayed", "vaccination_status_displayed", "pets_displayed", ],
            "career": ["workplaces_displayed", "job_title_displayed", "schools_displayed"],
            "future_plans": ["family_plans_displayed", "dating_intention_displayed", "children_displayed", "relationship_type_displayed"]
        }

        # initialize counters
        display_counts = defaultdict(lambda: {"true": 0, "false": 0})
        
        for category, fields in categories.items():
            for field in fields:
                if field in profile_data:
                    display_value = profile_data[field]
                    display_counts[category]["true" if display_value else "false"] += 1
        return dict(display_counts)

    
def _convert_height(cm):
    inches = cm / 2.54
    feet = int(inches // 12)  # whole feet
    # remaining inches, rounded to 1 decimal place
    remaining_inches = round(inches % 12, 1)  

    return feet, remaining_inches 

def _timestamp_durations(leading_timestamp, lagging_timestamp, lag_has_microseconds=False):
    lead_dt_format = "%Y-%m-%d %H:%M:%S"
    lag_dt_format = lead_dt_format

    # the signup_time contains microseconds, so this handles that special format 
    if lag_has_microseconds:
        lag_dt_format = "%Y-%m-%d %H:%M:%S.%f"

    # parse timestamps
    lag_time = datetime.strptime(lagging_timestamp, lag_dt_format)
    lead_time = datetime.strptime(leading_timestamp, lead_dt_format)

    # calculate difference in days
    days_difference = (lead_time - lag_time).days

    return days_difference