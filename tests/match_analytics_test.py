import unittest
import match_analytics as ma

test_events = ma.prepare_uploaded_match_data('test_data/test_matches.json')


class MatchAnalyticsTest(unittest.TestCase):
    def test_total_event_count(self):
        total_events = ma.total_counts(test_events)
        self.assertEqual(total_events.size, 8)

    def test_invalid_file_type(self):
        with self.assertRaises(ValueError):
            ma.prepare_uploaded_match_data('test_data/test_matches.csv')

    def test_invalid_file_name(self):
        with self.assertRaises(ValueError):
            ma.prepare_uploaded_match_data('test_data/invalid_file.json')


if __name__ == '__main__':
    unittest.main()
