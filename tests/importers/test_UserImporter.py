import pytest
import os
import json
from unittest.mock import mock_open, patch

from app.importers.UserImporter import UserImporter


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
        }
    ],
    "account": {
        "signup_time": "2001-06-29 03:27:17.539",
        "last_pause_time": "2003-09-04 03:04:32",
        "last_unpause_time": "2020-12-10 16:53:40",
        "last_seen": "2024-01-17 04:07:39",
        "device_platform": "ios",
        "device_os": "16.6.1",
        "device_model": "unknown",
        "app_version": "9.30.0",
        "push_notifications_enabled": false
    }
}
'''

#########################################################################################
# pytest fixtures
#########################################################################################
@pytest.fixture
def user_importer(monkeypatch):
    monkeypatch.setenv("USER_FILE_PATH", USER_FILE_PATH)

    with patch("builtins.open", mock_open(read_data=USER_DATA)) as mock_file, \
         patch("json.load", return_value=json.loads(USER_DATA)) as mock_json_load:

        user_importer = UserImporter()
    return user_importer


#########################################################################################
# unit tests
#########################################################################################
def test_exists(user_importer):
    assert user_importer is not None

def test_user_file_path_not_set():
    if "USER_FILE_PATH" in os.environ:
        del os.environ["USER_FILE_PATH"]

    with pytest.raises(Exception, match="USER_FILE_PATH environment variable is not set."):
        UserImporter()

def test_user_file_not_json():
    os.environ["USER_FILE_PATH"] = "invalid_file.txt"  # invalid value

    with pytest.raises(Exception, match="The user file needs to be a JSON file."):
        UserImporter()

def test_user_importer_loads_data(user_importer):
    assert isinstance(user_importer.user_data, dict)
    assert "devices" in user_importer.user_data
    assert "account" in user_importer.user_data

def test_device_data(user_importer):
    device = user_importer.user_data["devices"][0]
    assert device["ip_address"] == "174.234.168.00"
    assert device["device_platform"] == "ios"
    assert device["device_os_versions"] == "16.5.1"

def test_account_data(user_importer):
    account = user_importer.user_data["account"]
    assert account["device_os"] == "16.6.1"
    assert account["app_version"] == "9.30.0"
    assert account["push_notifications_enabled"] is False
