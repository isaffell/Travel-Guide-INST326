"""This is a python script for the final project, INST 326.

Driver: Isabel Saffell
Navigator: Abbey Vanasse
Assignment: Final Project, DC Travel Guide 
Date: 4/19/2025

Challenges Encountered:
"""
import WebScraper
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
            "min_rating": 0.0
        }

    def calc_distance(self, places):
        """This method will go through the list of all of the places and their corresponding walking
        distance and sort in order of closest to farthest. 

        Args: 
            places (list): list of dictionaries with name value and distance key
            
        Returns:
            sorted_by_distance(dict): a sorted dictionary
        """
        sorted_by_distance = sorted(places, key=lambda x: x['distance'])
        return sorted_by_distance
        
    
    def sort_activity_types(self, places):
        """Sorts the places based on how well they match the user's input preferences.
        
        Args:
            places(list): list of dictionaries with name value and acitivty key
            
        Returns:
            matched_places: places sorted by user preference input
        """
        ranked_places = []
        
        for place in places:
                pass
                #will go through places and get activity type
                #if activity type is in preferences change score, otherwise 0
                
        #return a list of the ranked places
        pass
    
    
    
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
        all_metro_stops = ["Anacostia", "Archives", "Columbia Heights", "Congress Heights", "Fort Trotten", "Gallery PI-Chinatown", 
                           "Georgia Ave-Petworth", "L'Enfant Plaza", "Mt Vernon", "Shaw-Howard U", "U Street", "Waterfront"]
        
        activity_types = ["Food", "Museums and Monuments", "Sporty", "Social", "Nature"]
        
        print(f"Hello {self.users_name}! Welcome to the Green Line Metro Trip Guide!\n")
        print(f"Based on your preferences, you will be provided with the top 5 places to travel to.\n")
        print(f"These are the Green Line Metro stop options, from College Park to D.C. :\n")
        print(f"{all_metro_stops}\n")
        
        metro_stop_name = input("Which metro stop would you like to get off at? Please enter name precisely with '-' if necessary.\n")
        self.metro_stop_name = metro_stop_name
        
        #will use weights to determine what is most important to the user
        #if activity type is the most important, weight matches activity type
        print(f"{self.users_name}, now that you have selected {metro_stop_name}, please select what activity types you like. \n")
        print(f"These are the following activity types{activity_types}")
        user_places = input(f"Please enter the activity type in order from most preferred to least, separating with commas.\n")
        user_places_list = user_places.split(",")
        stripped_activities = []
        for user_places in user_places_list:
            stripped_activities.append(user_places.strip().lower())
        self.preferences["type_of_activity"] = stripped_activities
        
        #if distance is the most important, weight matches distance
        max_distance = float(input("What is the maximum distance you want to walk in miles?\n "))
        self.preferences["max_walking_distance"] = max_distance
        
        #if rating is the most important, weight matches rating
        desired_rating = float(input("What's the minimum rating you desire? Please enter a whole number between 1-5."))
        self.preferences["min_rating"] = desired_rating
        
        
if __name__ == "__main__":

    user = User_Preference()
    user.user_preferences()

    scraper = WebScraper(user.metro_stop_name)
    scraper.places_scraper()

    filtered = scraper.places_filter(user.preferences)
    
    #Define the weights for the scoring system
    #Rank the places
    #Print out the top 5 places accordingly
        
        
    
