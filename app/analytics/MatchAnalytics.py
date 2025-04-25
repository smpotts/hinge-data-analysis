import json, os
from datetime import datetime, timedelta

class MatchAnalytics:
    def __init__(self):
        self.match_file_path = os.environ.get("MATCH_FILE_PATH")

        if self.match_file_path is None:
            raise Exception("MATCH_FILE_PATH environment variable is not set.")
        
        if '.json' not in self.match_file_path:
            raise Exception("The match file needs to be a JSON file.")

        with open(self.match_file_path, 'r') as file:
            match_data = json.load(file)
        self.match_data = match_data

    def get_match_data(self):
        all_matches = []
        for entry in self.match_data:
            matches = entry.get("match", [])
            all_matches.extend(matches)
        return all_matches
    
    def get_block_data(self):
        all_blocks = []
        for entry in self.match_data:
            blocks = entry.get("block", [])
            all_blocks.extend(blocks)
        return all_blocks 
    
    def get_likes_data(self):
        all_likes = []
        for entry in self.match_data:
            likes = entry.get("like", [])
            all_likes.extend(likes)
        return all_likes
    
    def get_chat_data(self):
        all_chats = []
        for entry in self.match_data:
            chats = entry.get("chats", [])
            all_chats.extend(chats)
        return all_chats 

    def get_message_count_last_12_months(self):
        now = datetime.now()
        one_year_ago = now - timedelta(days=365)

        msg_counts_per_month = []
        for entry in self.match_data:
            match = entry.get("match", [])
            chats = entry.get("chats", [])
            if match:
                match_time = datetime.fromisoformat(match[0]["timestamp"])
                if match_time >= one_year_ago:
                    month = match_time.strftime("%Y-%m")
                    msg_counts_per_month.append({
                        "month": month,
                        "message_count": len(chats)
                    })
        return msg_counts_per_month

    def get_response_latency(self):
        latency_data = []
        for entry in self.match_data:
            match = entry.get("match", [])
            chats = entry.get("chats", [])

            if match and chats:
                match_time = datetime.fromisoformat(match[0]["timestamp"])
                first_message_time = datetime.fromisoformat(chats[0]["timestamp"])
                latency = (first_message_time - match_time).total_seconds() / (3600 * 24)

                latency_data.append({
                    "match_time": match_time,
                    "first_message_time": first_message_time,
                    "latency_days": latency
                })
        return latency_data
    
    def get_match_durations(self):
        durations = []
        for entry in self.match_data:
            match = entry.get("match", [])
            block = entry.get("block", [])

            if match and block:
                match_time = datetime.fromisoformat(match[0]["timestamp"])
                block_time = datetime.fromisoformat(block[0]["timestamp"])
                duration_days = (block_time - match_time).days

                durations.append({
                    "match_time": match_time,
                    "block_time": block_time,
                    "duration_days": duration_days
                })
        return durations

    def get_match_rm_counts(self):
        records = []

        for entry in self.match_data:
            match_time = entry.get("match", [{}])[0].get("timestamp")
            block_time = entry.get("block", [{}])[0].get("timestamp")
            chats = entry.get("chats", [])

            if match_time and block_time:
                match_dt = datetime.fromisoformat(match_time)
                block_dt = datetime.fromisoformat(block_time)
                delta_days = (block_dt - match_dt).days
                message_count = len(chats)

                records.append({
                    "message_count": message_count,
                    "duration_days": delta_days
                })

        return records