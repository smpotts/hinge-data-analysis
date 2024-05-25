import unittest
import match_analytics as ma

test_events = ma.prepare_uploaded_match_data('tests/test_data/test_matches.json')


class MatchAnalyticsTest(unittest.TestCase):
    def test_event_count(self):
        total_events = ma.total_counts(test_events)
        self.assertEqual(total_events.size, 8)


if __name__ == '__main__':
    unittest.main()
