from user_preference import User_Preference
import unittest

class TestUserPreference(unittest.TestCase):
    def setUp(self):
        self.user = User_Preference("Bob")
        self.places = [
            {"name": "DC Food", "distance": 0.3, "activity_type": "food"},
            {"name": "DC Sport", "distance": 0.5, "activity_type": "sporty"},
            {"name": "DC Nature", "distance": 0.9, "activity_type": "nature"},
        ]
        
    def test_init(self):
        #tests attribute instantiation
        self.assertEqual(self.user.users_name, "Bob")
        self.assertIsNone(self.user.metro_stop_name)
        self.assertEqual(self.user.preferences["type_of_activity"], [])
        self.assertEqual(self.user.preferences["max_walking_distance"], 0.0)
        self.assertEqual(self.user.preferences["min_rating"], 0.0)

    def test_calc_distance(self):
        #tests if the distance is sorted correctly
        sorted_places = self.user.calc_distance([
            {"name": "Cafe", "distance": 0.5},
            {"name": "Museum", "distance": 0.1},
            {"name": "Concert Venue", "distance": 0.2},
        ])
        self.assertEqual([p["name"] for p in sorted_places], ["Museum", "Concert Venue", "Café"])
    
    def test_sort_activity_types(self):
        #tests if activity types sort correctly based on user preferences
        self.user.preferences["type_of_activity"] = ["sporty", "nature", "food"]
        ranked = self.user.sort_activity_types(self.places)
        self.assertEqual([p["name"] for p in ranked], ["DC Sport", "DC Nature", "DC Food"])

if __name__ == '__main__':
    unittest.main()