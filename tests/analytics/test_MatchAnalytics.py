import pytest, os, json
from unittest.mock import mock_open, patch

from app.analytics.MatchAnalytics import MatchAnalytics

#########################################################################################
# test values
#########################################################################################
MATCH_FILE_PATH = "fake/file/path/matches.json"
FIRST_MATCH_TIMESTAMP = '2005-04-23 14:53:01'
FIRST_BLOCK_TIMESTAMP = '2005-04-23 16:32:53'
FIRST_LIKE_TIMESTAMP = "2012-11-04 03:24:14"
FIRST_CHAT_MESSAGE = "Hey there!"
MATCH_DATA = '''
[
    {
        "match": [
            {
                "timestamp": "2025-04-23 14:53:01"
            }
        ],
        "chats": [
            {
                "body": "Hey there!",
                "timestamp": "2025-04-23 14:53:22"
            }
        ],
        "block": [
            {
                "block_type": "remove",
                "timestamp": "2025-04-23 16:32:53"
            }
        ]
    },
    {
        "match": [
            {
                "timestamp": "2025-03-06 23:08:31"
            }
        ],
        "chats": [
            {
                "body": "What's up?",
                "timestamp": "2025-03-06 23:11:04"
            }
        ],
        "block": [
            {
                "block_type": "remove",
                "timestamp": "2025-03-15 16:32:49"
            }
        ]
    },
    {
        "match": [
            {
                "timestamp": "2025-04-06 23:09:16"
            }
        ],
        "chats": [
            {
                "body": "Hi!",
                "timestamp": "2025-04-06 23:09:52"
            },
            {
                "body": "Here's another message",
                "timestamp": "2025-04-09 02:41:05"
            },
            {
                "body": "And another message!",
                "timestamp": "2025-04-10 12:27:21"
            },
            {
                "body": "And one last message",
                "timestamp": "2025-04-10 12:27:00"
            }
        ],
        "block": [
            {
                "block_type": "remove",
                "timestamp": "2025-04-15 16:32:45"
            }
        ],
        "like": [
            {
                "timestamp": "2025-03-04 03:24:14",
                "like": [
                    {
                        "timestamp": "2025-03-04 03:24:14"
                    }
                ]
            }
        ]
    }
]
'''
#########################################################################################
# pytest fixtures
#########################################################################################
@pytest.fixture
def match_analytics(monkeypatch):
    monkeypatch.setenv("MATCH_FILE_PATH", MATCH_FILE_PATH)

    with patch("builtins.open", mock_open(read_data=MATCH_DATA)) as mock_file, \
         patch("json.load", return_value=json.loads(MATCH_DATA)) as mock_json_load:

        match_analytics = MatchAnalytics()
    return match_analytics

#########################################################################################
# unit tests
#########################################################################################
def test_exists(match_analytics):
    assert match_analytics is not None

def test_match_file_path_not_set():
    if "MATCH_FILE_PATH" in os.environ:
        del os.environ["MATCH_FILE_PATH"]
    
    with pytest.raises(Exception, match="MATCH_FILE_PATH environment varviable is not set."):
        MatchAnalytics()

def test_match_file_not_json():
    os.environ["MATCH_FILE_PATH"] = "invalid_file.txt"

    with pytest.raises(Exception, match="The match file needs to be a JSON file."):
        MatchAnalytics()

def test_loads_match_data(match_analytics):
    assert isinstance(match_analytics.match_data, list)
    assert len(match_analytics.match_data) == 3 # 3 test matches

def test_get_matches(match_analytics):
    matches = match_analytics.get_match_data()
    assert len(matches) == 3
    assert matches[0].get("timestamp") == FIRST_MATCH_TIMESTAMP 

def test_get_blocks(match_analytics):
    blocks = match_analytics.get_block_data()
    assert len(blocks) == 3
    assert blocks[0].get("timestamp") == FIRST_BLOCK_TIMESTAMP
    assert blocks[0].get("block_type") == "remove"

def test_get_likes(match_analytics):
    likes = match_analytics.get_likes_data()
    assert len(likes) == 1
    assert likes[0].get("timestamp") == FIRST_LIKE_TIMESTAMP 

def test_get_chats(match_analytics):
    chats = match_analytics.get_chat_data()
    assert len(chats) == 6
    assert chats[0].get("body") == FIRST_CHAT_MESSAGE

def test_get_message_count_last_12_months(match_analytics):
    message_counts = match_analytics.get_message_count_last_12_months()
    print(message_counts)
    assert message_counts is not None
    assert len(message_counts) == 3
    assert message_counts[2].get("month") == "2025-04"
    assert message_counts[2].get("message_count") == 4