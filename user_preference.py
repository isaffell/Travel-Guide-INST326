"""This is a python script for the final project, INST 326.

Driver: Isabel Saffell
Navigator: Abbey Vanasse
Assignment: Final Project, DC Travel Guide 
Date: 4/19/2025

Challenges Encountered:
"""
import MetroPlacesFinder
import pandas as pd


class User_Preference: 
    """A class for obtaining the user preferences for a travel guide from Green Line Metro stops."""
    def __init__(self, users_name = "Guest"):
        """Assigns attributes with defualt values and instanstiates them. 
        
        Args: 
            users_name(str): The users name, with default value of "Guest"
            
        """
        
        #sets the users name and default metro stop
        self.users_name = users_name
        self.metro_stop_name = None
        
        #sets preferences with default values
        self.preferences = {
            "type_of_activity": [],
            "max_walking_distance": 0.0,
        
        }
    
    def map_activity_types_to_google_places_api(self, user_activity_types):
        """Maps user-friendly activity types to Google Places API types."""
        google_api_types = {
            "food": ["restaurant", "cafe", "bakery", "meal_takeaway", "meal_delivery"],
            "museums and monuments": ["museum", "art_gallery", "historical_landmark", "tourist_attraction"],
            "sporty": ["gym", "stadium", "park", "sports_club"],
            "social": ["bar", "night_club", "cafe"],
            "nature": ["park", "campground", "natural_feature"]
        }
        
        mapped_types = []
        for user_type in user_activity_types:
            if user_type in google_api_types:
                mapped_types.extend(google_api_types[user_type])
        
        # Remove duplicates by converting to a set and back to a list
        return list(set(mapped_types))

    def sort_activity_types(self, places):
        """Sorts the places based on how well they match the user's input preferences.
        
        Args:
            places(list): list of dictionaries with name value and acitivty key
            
        Returns:
            matched_places: places sorted by user preference input
        """
        ranked_places = []
        
        for place in places:
                score = 0
                
                if place["type_of_activity"].lower() in self.preferences["type_of_activity"]:
                    rank = self.preferences["type_of_activity"].index(place["type_of_activity"].lower())
                    score += (len(self.preferences["type_of_activity"]) - rank ) *5
                    
                distance_score = max(0, self.preferences["max_walking_distance"] - place.get("walking_distance", 0))
                score += distance_score*3
                rating_score = max(0, place.get("rating", 0) - self.preferences.get("min_rating", 0))
                score += rating_score *1
                
                ranked_places.append({**place, "score": score})
        return sorted(ranked_places, key=lambda x:x["score"], reverse = True)
    
    def user_preferences(self):
        """
            Prompts the user for their travel preferences to help recommend top places 
            to visit near a Metro Green Line stop. 

            Args:
                self (UserPreferences): The instance of the UserPreferences class.
                    self.users_name (str): The name of the user.
                    self.metro_stop_name (str): The metro stop the user chooses to get off at.
                    self.preferences (dict): A dictionary storing user-selected:
                    type_of_activity (list of str): Ordered list of preferred activities.
                    max_walking_distance (float): Max distance the user wants to walk.
                    min_rating (float): Minimum rating the user wants for a place.
        """
        all_metro_stops = ['Anacostia', 'Archives', 'Columbia Heights', 'Congress Heights', 'Fort Trotten', 'Gallery PI-Chinatown', 
                           'Georgia Ave-Petworth', 'L''Enfant Plaza', 'Mt Vernon', 'Shaw-Howard U', 'U Street', 'Waterfront']
        
        activity_types = ["Food", "Museums and Monuments", "Sporty", "Social", "Nature"]
      
        self.users_name = input(f"Hello, what is your name?" + "\n")
        print(f"Hello {self.users_name}! Welcome to the Green Line Metro Trip Guide!\n")
        print(f"Based on your preferences, you will be provided with the top 5 places to travel to.\n") 
        print(f"These are the Green Line Metro stop options, from College Park to D.C. :\n")
        print(", ".join(all_metro_stops) + "\n")
        
        metro_stop_name = input("Which metro stop would you like to get off at? Please enter name precisely with '-' if necessary.\n")
        self.metro_stop_name = metro_stop_name
        
        #will use weights to determine what is most important to the user
        #if activity type is the most important, weight matches activity type
        
        print(f"{self.users_name}, now that you have selected {metro_stop_name}, please select what activity types you like. \n")
        print("These are the following activity types: " + ", ".join(activity_types) + "\n")
       
        
        user_places = input(f"Please enter the activity type in order from most preferred to least, separating with commas.\n")
        user_places_list = user_places.split(",")
        stripped_activities = []
        
        for user_places in user_places_list:
            stripped_activities.append(user_places.strip().lower())
        self.preferences["type_of_activity"] = stripped_activities
        
        #if distance is the most important, weight matches distance
        max_distance = float(input("What is the maximum distance you want to walk in miles?\n "))
        self.preferences["max_walking_distance"] = max_distance
    
   # def load_api_key(filepath="google_api_key.txt"):
        """ This function loads the Google API key from a local file

        Args:
            filepath(str): path to the file containing the API key. Default is "google_api_key.txt"

        Returns:
            str: the API key as a string
        
        """
        #with open(filepath, "r") as f:
        #    return f.read().strip()
        
# In user_preference (1).py, within the if __name__ == "__main__": block:

if __name__ == "__main__":

    API_KEY = MetroPlacesFinder.load_api_key()
    
    user = User_Preference()
    user.user_preferences()

    scraper = MetroPlacesFinder.MetroPlacesFinder(user.metro_stop_name, API_KEY)
    
    # Map the user's preferred activity types to Google Places API types
    google_places_types = user.map_activity_types_to_google_places_api(user.preferences["type_of_activity"])

    # Pass the mapped types to get_nearby_places
    scraper.get_nearby_places(included_types=google_places_types)
    
    # Now calculate walking distances for each place
    scraper.calculate_walking_distance()

    ranked_places = user.sort_activity_types(scraper.places_data)   
    print("\nTop 5 recommendations for you are:")
    for place in ranked_places[:5]:
        # Convert meters to miles (1 mile = 1609.34 meters)
        distance_in_miles = place['walking_distance'] / 1609.34
        print(f"- {place['name']}, {place['type_of_activity'].title()}, {distance_in_miles:.1f} miles")