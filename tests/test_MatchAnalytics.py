import unittest
import app.analytics.MatchAnalytics as MatchAnalytics

USER_FILE_PATH = 'tests/test_user.json'
MATCHES_FILE_PATH = 'tests/test_matches.json'


class AnalyticsTest(unittest.TestCase):
    def test_total_event_count(self):
        test_events = MatchAnalytics.prepare_uploaded_match_data(MATCHES_FILE_PATH)
        total_events = MatchAnalytics.total_counts(test_events)
        self.assertEqual(total_events.size, 8)

    def test_invalid_file_type(self):
        with self.assertRaises(ValueError):
            MatchAnalytics.prepare_uploaded_match_data('tests/matches.csv')

    def test_invalid_match_file_upload(self):
        with self.assertRaises(ValueError):
            MatchAnalytics.prepare_uploaded_match_data(USER_FILE_PATH)

    def test_invalid_user_file_upload(self):
        with self.assertRaises(ValueError):
            MatchAnalytics.import_user_account_data(MATCHES_FILE_PATH)

    def test_account_data_import(self):
        results = MatchAnalytics.import_user_account_data(USER_FILE_PATH)
        self.assertEqual(len(results), 9) # 9 keys in the dictionary

    def test_device_data_import(self):
        results = MatchAnalytics.import_user_device_data(USER_FILE_PATH)
        self.assertEqual(len(results), 5)


if __name__ == '__main__':
    unittest.main()
