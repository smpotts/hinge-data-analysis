import pytest
import os
import json
from unittest.mock import mock_open, patch

from app.analytics.UserAnalytics import UserAnalytics

#########################################################################################
# test values
#########################################################################################
USER_FILE_PATH = "fake/file/path/users.json"
USER_DATA = '''
{
    "devices": [
        {
            "ip_address": "174.234.168.00",
            "device_model": "unknown",
            "device_platform": "ios",
            "device_os_versions": "16.5.1"
        },
        {
            "ip_address": "130.279.438.00",
            "device_model": "unknown",
            "device_platform": "ios",
            "device_os_versions": "16.5.1"
        }
    ],
    "account": {
        "signup_time": "2024-01-01 03:27:17.539",
        "last_pause_time": "2020-09-04 03:04:32",
        "last_unpause_time": "2020-09-10 16:53:40",
        "last_seen": "2024-01-17 04:07:39",
        "device_platform": "ios",
        "device_os": "16.6.1",
        "device_model": "unknown",
        "app_version": "9.30.0",
        "push_notifications_enabled": false
    },
    "profile": {
        "first_name": "Fake User",
        "age": 99,
        "height_centimeters": 213,
        "gender": "female",
        "gender_identity_displayed": false,
        "ethnicities": "[Prefer Not to Say]",
        "ethnicities_displayed": false,
        "religions": "[Prefer Not to Say]",
        "religions_displayed": true,
        "workplaces_displayed": false,
        "schools_displayed": true,
        "job_title": "Astronaut",
        "job_title_displayed": true,
        "hometowns_displayed": false,
        "smoking": "[Prefer Not to Say]",
        "drinking": "[Prefer Not to Say]",
        "drugs": "[Prefer Not to Say]",
        "marijuana": "[Prefer Not to Say]",
        "children": "[Prefer Not to Say]",
        "family_plans": "[Prefer Not to Say]",
        "smoking_displayed": false,
        "drinking_displayed": true,
        "marijuana_displayed": false,
        "drugs_displayed": false,
        "children_displayed": false,
        "family_plans_displayed": true,
        "politics_displayed": false,
        "vaccination_status_displayed": true,
        "dating_intention_displayed": false,
        "languages_spoken_displayed": true,
        "relationship_type_displayed": false,
        "education_attained": "Undergraduate",
        "languages_spoken": "English",
        "ethnicities": "Prefer Not to Say",
        "pets": "Dog",
        "politics": "Prefer Not to Say",
        "religions": "Prefer Not to Say",
        "hometowns": "moon",
        "relationship_types": "Prefer Not to Say",
        "dating_intention": "Prefer Not to Say",
        "workplaces": "Space"
    },
    "preferences": {
        "distance_miles_max": 50,
        "age_min": 98,
        "age_max": 99,
        "age_dealbreaker": true,
        "height_dealbreaker": false,
        "ethnicity_preference": "[Open to All]",
        "ethnicity_dealbreaker": false,
        "religion_preference": "[Open to All]",
        "religion_dealbreaker": false,
        "smoking_preference": "[Open to All]",
        "smoking_dealbreaker": false,
        "drinking_preference": "[Open to All]",
        "drinking_dealbreaker": false,
        "marijuana_preference": "[Open to All]",
        "marijuana_dealbreaker": false,
        "drugs_preference": "[Open to All]",
        "drugs_dealbreaker": false,
        "children_preference": "[Open to All]",
        "children_dealbreaker": false,
        "family_plans_preference": "[Open to All]",
        "family_plans_dealbreaker": false,
        "education_attained_preference": "[Open to All]",
        "education_attained_dealbreaker": false,
        "politics_preference": "[Open to All]",
        "politics_dealbreaker": false
    },
    "location": {
        "latitude": 65.00,
        "longitude": 18.00,
        "country": "Iceland",
        "locality": "New York",
        "sublocality": "Brooklyn",
        "neighborhood": "Flatbush"
    }
}
'''
COUNT_DISPLAYED_ATTRIB_OUTPUT = {'identity': {'true': 2, 'false': 4}, 'lifestyle': {'true': 2, 'false': 3}, 'career': {'true': 2, 'false': 1}, 'future_plans': {'true': 1, 'false': 3}}
STRINGENCY_COUNTS = {'physical': {'true': 1, 'false': 1}, 'identity': {'true': 0, 'false': 3}, 'lifestyle': {'true': 0, 'false': 4}, 'career': {'true': 0, 'false': 1}, 'future_plans': {'true': 0, 'false': 2}}
GEOLITE_DB_PATH = 'data/db_path.mmdb'

#########################################################################################
# pytest fixtures
#########################################################################################
@pytest.fixture
def user_analytics(monkeypatch):
    monkeypatch.setenv("USER_FILE_PATH", USER_FILE_PATH)
    monkeypatch.setenv("GEOLITE_DB_PATH", GEOLITE_DB_PATH)

    with patch("builtins.open", mock_open(read_data=USER_DATA)) as mock_file, \
         patch("json.load", return_value=json.loads(USER_DATA)) as mock_json_load:

        user_analytics = UserAnalytics()
    return user_analytics

#########################################################################################
# unit tests
#########################################################################################
def test_exists(user_analytics):
    assert user_analytics is not None

def test_user_file_path_not_set():
    if "USER_FILE_PATH" in os.environ:
        del os.environ["USER_FILE_PATH"]

    with pytest.raises(Exception, match="USER_FILE_PATH environment variable is not set."):
        UserAnalytics()

def test_user_file_not_json():
    os.environ["USER_FILE_PATH"] = "invalid_file.txt"  # invalid value

    with pytest.raises(Exception, match="The user file needs to be a JSON file."):
        UserAnalytics()

def test_user_analytics_loads_data(user_analytics):
    assert isinstance(user_analytics.user_data, dict)
    assert "devices" in user_analytics.user_data
    assert "account" in user_analytics.user_data

def test_device_data(user_analytics):
    device = user_analytics.get_devices_data()[0]
    assert device["ip_address"] == "174.234.168.00"
    assert device["device_platform"] == "ios"
    assert device["device_os_versions"] == "16.5.1"

def test_account_data(user_analytics):
    account = user_analytics.get_account_data()
    assert account["device_os"] == "16.6.1"
    assert account["app_version"] == "9.30.0"
    assert account["push_notifications_enabled"] is False

def test_profile_data(user_analytics):
    profile = user_analytics.get_profile_data()
    assert profile["first_name"] == "Fake User"
    assert profile["age"] == 99
    assert profile["height_centimeters"] == 213

def test_preferences_data(user_analytics):
    preferences = user_analytics.get_preferences_data()
    assert preferences["distance_miles_max"] == 50
    assert preferences["age_min"] == 98
    assert preferences["age_max"] == 99

def test_location_data(user_analytics):
    locations = user_analytics.get_location_data()
    assert locations["latitude"] == 65.00
    assert locations["longitude"] == 18.00
    assert locations["country"] == "Iceland"

def test_build_user_summary_dict(user_analytics):
    result = user_analytics.build_user_summary_dict()
    assert result["first_name"] == "Fake User"
    assert result["age"] == 99
    assert result["height_feet"] == 6
    assert result["height_inches"] == 11.9
    assert result["gender"] == "female"
    assert result["job_title"] == "Astronaut"
    assert result["education_attained"] == "Undergraduate" 
    assert result["languages_spoken"] == "English"
    assert result["politics"] == "Prefer Not to Say" 
    assert result["pets"] == "Dog"
    assert result["last_pause_duration"] == 6
    assert result["on_app_duration"] == 16

def test_build_user_location_dict(user_analytics):
    result = user_analytics.build_user_location_dict()
    assert result["city"] == "Brooklyn"
    assert result["latitude"] == 65.00
    assert result["longitude"] == 18.00
    assert result["country"] == "Iceland"
    assert result["neighborhood"] == "Flatbush"
    assert result["locality"] == "New York"
    
def test_count_displayed_attributes(user_analytics):
    result = user_analytics.count_displayed_attributes()
    assert result == COUNT_DISPLAYED_ATTRIB_OUTPUT 

def test_profile_preference_selections(user_analytics):
    profile, prefs = user_analytics.profile_preference_selections()
    assert len(profile) == len(prefs)
    assert len(profile) == 10

# TODO: this needs to be mocked out and better tests added
# def test_collect_location_from_ip(user_analytics):
#     result = user_analytics.collect_location_from_ip() 
#     assert result is not None

def test_count_stringeny_attributes(user_analytics):
    results = user_analytics.count_stringeny_attributes()
    print(results)

    assert list(results.keys()) == ['physical', 'identity', 'lifestyle', 'career', 'future_plans']
    assert results == STRINGENCY_COUNTS 