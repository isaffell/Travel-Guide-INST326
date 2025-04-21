import unittest
from WebScraper import WebScraper

class TestWebScraper(unittest.TestCase):
    def setUp(self):
        """ Sets up the WebScraper instance and any initial test data included."""
        self.scraper = WebScraper("Navy-Yard Ballpark")

        #dummy places data for testing since we haven't web scraped yet
        self.scraper.places_data = [
            {"name": "Bluejacket", "type_of_activity": "brewery", "walking_distance": 0.3, "rating": 4.1},
            {"name": "Diamond Teague Park", "type_of_activity": "park", "walking_distance": 0.4, "rating": 4.6},
            {"name": "Nationals Park", "type_of_activity": "sports", "walking_distance": 0.1, "rating": 4.7},

        ]
        self.user_preferences = {
            "type_of_activity": ["park", "brewery", "sports"],
            "max_walking_distance": 1.0,
            "min_rating": 4.0
        }
        self.weights = {"activity": 5, "distance": 3, "rating": 2}

    def test_places_filter(self):
        """This tests the places_filter method"""
        filtered = self.scraper.places_filter(self.user_preferences)
        self.assertEqual(len(filtered), 2) 
        # assertEqual(a,b) checks whether a == b 
        # should return 2 places that match the filter. Once we web scrape, may include more.
    
    def test_places_ranker(self):
        """This tests the places_ranker method"""
        filtered = self.scraper.places_filter(self.user_preferences)
        ranked = self.scraper.places_ranker(filtered, self.user_preferences, self.weights)
        self.assertEqual(ranked[0]["name"], "Diamond Teague Park")

if __name__ == "__main__":
    unittest.main()
    
    

        
        