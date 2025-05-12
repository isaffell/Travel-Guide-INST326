import unittest
from MetroPlacesFinder import MetroPlacesFinder, load_api_key

class TestMetroPlacesFinder(unittest.TestCase):
    def setUp(self):
        """ Sets up the MetroPlacesFinder instance and any initial test data included."""
        self.finder = MetroPlacesFinder("Navy-Yard Ballpark", api_key="dummy_test_key")

        #manually set mock places data (skipping actual API calls)
        self.finder.places_data = [
            {"name": "Bluejacket", "type_of_activity": "brewery", "walking_distance": 0.3},
            {"name": "Diamond Teague Park", "type_of_activity": "park", "walking_distance": 0.4},
            {"name": "Nationals Park", "type_of_activity": "sports", "walking_distance": 0.1},
        ]
        
        #user preferences
        self.user_preferences = {
            "type_of_activity": ["park", "brewery", "sports"],
            "max_walking_distance": 1.0,
            "max_distance": 0.7
        }

        #weights for scoring
        self.weights = {
            "activity": 5,
            "distance": 3
        }

    def test_places_filter(self):
        """This tests the places_filter method and returns only places that match user preferences"""
        filtered = self.finder.places_filter(self.user_preferences)
        
        # locations are within the distance and match a listed activity type
        self.assertEqual(len(filtered), 3)
        self.assertTrue(all(place["type_of_activity"] in self.user_preferences["type_of_activity"]
                            for place in filtered))
        # assertEqual(a,b) checks whether a == b 
        # should return 3 places that match the filter. Once we web scrape, may include more.
    
    def test_places_ranker(self):
        """This tests the places_ranker method and returns places ordered by score."""
        filtered = self.finder.places_filter(self.user_preferences)
        ranked = self.finder.places_ranker(filtered, self.user_preferences, self.weights)
        
        # With "park" ranked highest in preferences, Diamond Teague Park should score best
        self.assertEqual(ranked[0]["name"], "Diamond Teague Park")
        self.assertTrue(ranked[0]["score"] >= ranked[-1]["score"])

if __name__ == "__main__":
    unittest.main()
    
    

        
        