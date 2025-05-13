from user_preference import User_Preference
import unittest


class TestUserPreference(unittest.TestCase):
    def setUp(self):
        #Creates an instance of the user_preference class with basic attributes for testing
        
        self.user = User_Preference("Bob")
        self.user.prefernces = {
            "type_of_activity": ["sporty", "nature", "food"],
            "max_walking_distance": 1.0,
            "min_rating": 3.0
        }
        self.places = [
            {"name": "DC Food", "walking_distance": 0.3, "type_of_activity": "food"},
            {"name": "DC Sport", "walking_distance": 0.5, "type_of_activity": "sporty"},
            {"name": "DC Nature", "walking_distance": 0.9, "type_of_activity": "nature"},
        ]
        
    def test_init(self):
        """tests the basic attribute instantiation to ensure the init method is set up correctly. 
        If the init method had issues it would greatly impact the rest of the code."""
        
        user = User_Preference("Bob")
        self.assertEqual(user.users_name, "Bob")
        self.assertIsNone(user.metro_stop_name)
        self.assertIn("type_of_activity", user.preferences)
        self.assertIn("max_walking_distance", user.preferences)
        self.assertEqual(user.preferences["type_of_activity"], [])
        self.assertEqual(user.preferences["max_walking_distance"], 0.0)
   
    def test_distance_ranks(self): 
        """Tests that a closer distance will rank higher than a farther distance of the same activity type. 
        This is important in terms of outputting the final travel guide with ranked places. 
        """
        places = [
            {"name": "Close", "walking_distance": 0.1, "type_of_activity": "sporty", "rating": 0},
            {"name": "Far", "walking_distance": 1.2, "type_of_activity": "sporty", "rating": 0}
        ]
        ranked = self.user.sort_activity_types(places)
        self.assertEqual(ranked[0]["name"], "Close")
        
    def test_multiple_activity_types_to_api_types(self):
        """Test mapping of of the labels we assigned to activity types to Google Maps API activity type names.
        This is important to test in accurately matching the user's preference to the AI place data."""
        user_types = ["food", "nature"]
        mapped = self.user.map_activity_types_to_google_places_api(user_types)
        # Should include values from both categories
        expected_types = ['restaurant', 'cafe', 'bakery', 'meal_takeaway', 'meal_delivery',
                          'park', 'campground', 'natural_feature']
        self.assertCountEqual(mapped, expected_types)
        
    def test_single_activity_types_to_api_types(self):
        """Test mapping of of the labels we assigned to activity types to Google Maps API activity type names.
        This is important to test in accurately matching the user's preference to the AI place data."""
        user_type = ["food"]
        mapped = self.user.map_activity_types_to_google_places_api(user_type)
        # Should include only values from food category
        expected_types = ['restaurant', 'cafe', 'bakery', 'meal_takeaway', 'meal_delivery']
        self.assertCountEqual(mapped, expected_types)
        
    def test_user_preferences_input_structure(self):
        """Test that preferences are updated correctly from input that the user gave. 
        This is critical in making sure the travel guide actually takes in the user's preferences
        and provides them with options matched to them."""
        
        #example user preferences and tests they are stored correctly
        self.user.metro_stop_name = "Archives"
        self.user.preferences["type_of_activity"] = ["food", "sporty"]
        self.user.preferences["max_walking_distance"] = 4
        self.assertEqual(self.user.metro_stop_name, "Archives")
        self.assertIn("food", self.user.preferences["type_of_activity"])
        self.assertEqual(self.user.preferences["max_walking_distance"], 4)


if __name__ == '__main__':
    unittest.main()