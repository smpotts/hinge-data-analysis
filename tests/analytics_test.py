import unittest
import analytics

test_events = analytics.prepare_uploaded_match_data('tests/test_matches.json')


class MatchAnalyticsTest(unittest.TestCase):
    def test_total_event_count(self):
        total_events = analytics.total_counts(test_events)
        self.assertEqual(total_events.size, 8)

    def test_invalid_file_type(self):
        with self.assertRaises(ValueError):
            analytics.prepare_uploaded_match_data('tests/test_matches.csv')

    def test_invalid_file_name(self):
        with self.assertRaises(ValueError):
            analytics.prepare_uploaded_match_data('tests/invalid_file.json')

    def test_account_data_import(self):
        results = analytics.import_user_account_data()
        self.assertEqual(results.size, 1)


if __name__ == '__main__':
    unittest.main()
