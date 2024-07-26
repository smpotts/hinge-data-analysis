import unittest
import analytics

USER_FILE_PATH = 'tests/test_user.json'
MATCHES_FILE_PATH = 'tests/test_matches.json'


class AnalyticsTest(unittest.TestCase):
    def test_total_event_count(self):
        test_events = analytics.prepare_uploaded_match_data(MATCHES_FILE_PATH)
        total_events = analytics.total_counts(test_events)
        self.assertEqual(total_events.size, 8)

    def test_invalid_file_type(self):
        with self.assertRaises(ValueError):
            analytics.prepare_uploaded_match_data('tests/matches.csv')

    def test_account_data_import(self):
        results = analytics.import_user_account_data(USER_FILE_PATH)
        self.assertEqual(len(results), 9) # 9 keys in the dictionary


if __name__ == '__main__':
    unittest.main()
