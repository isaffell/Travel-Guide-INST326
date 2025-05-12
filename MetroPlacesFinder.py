"""This is a python script for the final project, INST 326.

DC Metro Travel Guide for UMD Students

This script is designed to help UMD students discover places to visit near stops
on the Washington, DC Metro Green Line (since this line is the most accessible from campus).
It uses Google Map APIS (Geocoding and New Places) to gather and filter location data.

Users can specify their preferences including:
- type of activity (ie: museum, restaurant, park)
- max acceptable walking distance from the metro station

Driver: Abbey Vanasse
Navigator: Isabel Saffell
Assignment: Final Project, DC Travel Guide 
Date: 4/19/2025

"""
#pip install requests
import requests
import os

def load_api_key(filepath="google_api_key.txt"):
    """ This function loads the Google API key from a local file

    Args:
        filepath(str): path to the file containing the API key. Default is "google_api_key.txt"

    Returns:
        str: the API key as a string
    
    """
    with open(filepath, "r") as f:
        return f.read().strip()

class MetroPlacesFinder:
    """A class for finding and recommending places in the near the Washingotn, DC 
    Metro Green Line based on user preferences such as type of activity and walking distance from the metro.
    """

    def __init__(self, metro_stop_name, api_key):
        """ This method will initialize the MetroPlacesFinder object
        
        Args: 
            metro_stop_name (str): the name of the metro green line stop.
            api_key (str): Google Maps API ky
        """
        self.metro_stop_name = metro_stop_name
        self.api_key = api_key
        self.places_data = []
        self.location = self.get_location_coordinates()

    def get_location_coordinates(self):
        """ This method uses the Geocoding API to get latitude and longitude coordinates
        of the given Metro stop.
        
        Returns:
            dict or None: a dictionary with 'lat' and 'lng' if successful, otherwise, None
        """
        geo_url = f"https://maps.googleapis.com/maps/api/geocode/json"
        parameters = {
            "address": f"{self.metro_stop_name} Metro Station, DMV Area", 
            "key": self.api_key
        }
        response = requests.get(geo_url, params=parameters).json()
        
        if response["results"]:
            location = response["results"][0]["geometry"]["location"]
            print("Location Coordinates:", location)  
            return location
        return None
    
    def get_nearby_places(self, radius_meters=1000, included_types=["tourist_attraction"]):
        """This method uses the Google Nearby Search (New) API to get retrieve nearby places within a certain
        radius of the Metro stop.

        Args:
            radius_meters(int): radius around the metro station in meters to search. Default is 1000.
            included_types(list): List of place types to include in the search. Default is ["tourist_attraction"]

        Returns:
            self.places_data(list): a list of dictionaries with information about each place found
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
        """ This method filters nearby places based on user-defined preferences

        Args:
            user_prefereces (dict): dictionary with keys
                - "type_of_activity" (list of str): desired types of activities
                - "max_walking_distance" (float): maximum walking distance allowed (in meters)

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
        """ This method ranks the list of filtered places to provide the 
        best matches based on the user preferences and weights using a scoring system.

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