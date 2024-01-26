import unittest
from src import match_analytics as ma
from src import data_utility as du
import pandas as pd

test_events = du.load_match_data('tests/test_data/test_matches.json')


class MatchAnalyticsTest(unittest.TestCase):
    def test_event_count(self):
        total_events = ma.total_counts(test_events)
        self.assertEqual(total_events.size, 8)


if __name__ == '__main__':
    unittest.main()
