"""This is a python script for the final project, INST 326.

Driver: Abbey Vanasse
Navigator: Isabel Saffell
Assignment: Final Project, DC Travel Guide 
Date: 4/19/2025
"""

import requests
from bs4 import BeautifulSoup

class WebScraper:
    """A class for scraping and recommending places in the DMV 
    area along the Metro Green Line based on user preferences such 
    as type of activity, walking distance from the metro, Google-based ratings.
    """

    def __init__(self, metro_stop_name):
        """Will initialize the WebScraper instance for a specific 
        stop along the Metro Green Line
        
        Args: 
            metro_stop_name (str): the name of the metro green line stop.
        """

        self.metro_stop_name = metro_stop_name
        self.places_data = []

    def places_scraper(self):
        """This method will scrape data for places near the 
        specific Green Line stop. It will also populate the places_data with dicts 
        containing name, type_of_activity, walking_distance, and rating.
        """

        #placeholder for the scraping logic using requests/BeautifulSoup

    def places_filter(self, user_preferences):
        """ This method will filter the list of places near the specified 
        Green Line stop given the user preferences.

        Args:
            user_prefereces (dict): dictionary with keys such as type_of_activity, 
            max_walking_distance, and min_rating

        Returns:
            list: filtered list of places based off of user_preferences
        """

        filtered_list = []
        for place in self.places_data:
            if (place["type_of_activity"] in user_preferences["type_of_activity"] and
                place["walking_distance"] <= user_preferences["max_walking_distance"] and
                place["rating"] >= user_preferences["min_rating"]):
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
                - min_rating: the min acceptable rating
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
            rating_score = max(0, place["rating"] - user_preferences["min_rating"])
            score += rating_score * weights.get("rating", 1)

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