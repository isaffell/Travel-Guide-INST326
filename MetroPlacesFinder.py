"""This is a python script for the final project, INST 326.

Driver: Abbey Vanasse
Navigator: Isabel Saffell
Assignment: Final Project, DC Travel Guide 
Date: 4/19/2025

"""
#pip install requests
import requests
import os

def load_api_key(filepath="google_api_key.txt"):
    with open(filepath, "r") as f:
        return f.read().strip()

class MetroPlacesFinder:
    """A class for scraping and recommending places in the DMV 
    area along the Metro Green Line based on user preferences such 
    as type of activity, walking distance from the metro, Google-based ratings.
    """

    def __init__(self, metro_stop_name, api_key):
        """ This method will initialize the metro stop name and the api key
        
        Args: 
            metro_stop_name (str): the name of the metro green line stop.
            api_key (str)
        """

        self.metro_stop_name = metro_stop_name
        self.api_key = api_key
        self.places_data = []
        self.location = self.get_location_coordinates()

    def get_location_coordinates(self):
        """ This method uses the Geocoding API to get latitude and longitude coordinates
        
        Args:
        """
        geo_url = f"https://maps.googleapis.com/maps/api/geocode/json"
        parameters = {
            "address": f"{self.metro_stop_name} Metro Station, DMV Area", 
            "key": self.api_key
        }
        response = requests.get(geo_url, parameters=parameters).json()
        
        if response["results"]:
            location = response["results"][0]["geometry"]["location"]
            print("Location Coordinates:", location)  
            return location
        return None
    
    def get_nearby_places(self, radius_meters=1000, included_types=["tourist_attraction"]):
        """This method uses the Nearby Search (New) API to get places within a specified area.

        Args:

        """

        if not self.location:
            print("Error: Could not get location coordinates.")
            return

        url = "https://places.googleapis.com/v1/places:searchNearby"
        headers = {
            "Content-Type": "application/json",
            "Google-Api-Key": self.api_key,
            "Google-FieldMask": "places.displayName,places.primaryType,places.location"
            #Field masks are a way for API callers to list fields that a request should return or update. 
            #Using a FieldMask allows the API to avoid unnecessary work and improves performance
        }   

        body = {
            "includedTypes": included_types, 
            "maxResultCount": 10, 
            "locationRestriction": {
                "circle": {
                    "center":{
                        "latitude":self.location["lat"],
                        "longitude": self.location["lng"]
                    },
                    "radius": radius_meters
                }
            }
        }   

        response = requests.post(url, headers=headers, json=body).json()
        print("API Response:", response)

        if "places" in response:
            for place in response["places"]:
                self.places_data.append({
                    "name": place.get("displayName", {}).get("text", "Unknown Name"),
                    "type_of_activity": place.get("primaryType", "Unknown Type of Activity")
                })

        print("Processed Places Data:", self.places_data)

    def places_filter(self, user_preferences):
        """ This method will filter the list of places near the specified 
        Green Line stop given the user preferences.

        Args:
            user_prefereces (dict): dictionary with keys such as type_of_activity, 
            max_walking_distance ():

        Returns:
            list: filtered list of places based off of user_preferences
        """

        filtered_list = []
        for place in self.places_data:
            if (place["type_of_activity"] in user_preferences["type_of_activity"] and
                place["walking_distance"] <= user_preferences["max_walking_distance"]):
                filtered_list.append(place)
        return filtered_list
    
    def places_ranker(self, filtered_places, user_preferences, weights):
        """ This method will sort the list of filtered places to provide the 
        best matches based on the usee preferences and weights.

        Args:
            filtered_places (list): the list of places from places_filter
            user_preferences (dict): dict with keys including
                - type_of_activity" list of preferred activity types (in order of preference)
                - max_walking_distance: max acceptable walking distance
            weights (dict): weight values for each factor. for example (activity:5, distance: 3, rating: 1)

        Returns:
            list: list of recommended places, sorted from best to worst match for the user.
        """

        def calculate_score(place):
            score = 0

            #type of activity score (higher number for higher ranked activity type)
            if place["type_of_activity"] in user_preferences["type_of_activity"]:
                rank_of_activity = user_preferences["type_of_activity"].index(place["type_of_activity"])
                score += (len(user_preferences["type_of_activity"]) - rank_of_activity) * weights.get("activity", 1)

            #distance score
            distance_score = max(0, user_preferences["max_distance"] - place["walking_distance"])
            score += distance_score * weights.get("distance", 1)

            #rating score
            #rating_score = max(0, place["rating"] - user_preferences["min_rating"])
            #score += rating_score * weights.get("rating", 1)

            return score
        
        #add scores to each place
        # ** unpacks the key-value pairs in a dictionary. allows you to not need to add every key manually
        scored_places = [
            {**place, "score": calculate_score(place)}
            for place in filtered_places
        ]

        #return the sorted list by score
        #key=lambda x: x["score"] tells python how to sort (ie: for each x look at its score and then use it to sort)
        #reverse=True means sorting from highest to lowest score
        return sorted(scored_places, key=lambda x: x["score"], reverse=True)
    
        # expected output [ {"name": "restaurant", "score": 10}, {"name": "museum", "score": 8},{"name": "park", "score": 6}]

if __name__ == "__main__":
    API_KEY = load_api_key() 
    scraper = MetroPlacesFinder("Columbia Heights", API_KEY)
    scraper.get_nearby_places()
    print(scraper.places_data)