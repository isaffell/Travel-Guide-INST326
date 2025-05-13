Isabel Saffell, Abbey Vanasse
Professor Cruz
INST 326
12 May 2025
Documentation

Our final project for INST326 is a travel guide in DC meant for UMD students who are taking the Green Line Metro. We use the Google Maps API platform to gather data on place attributes like distance and activity type. 
Using this data and the user preferences, our code formulates a guide specific to each user with their top 5 places to visit. 

Our youtube video with a live demo: INST326 Travel Guide

Running our Code: 
To run our code from the command line, first start by making sure the API key .txt file is in the same folder as user_preference.py and MetroPlacesFinder.py. 
Also make sure the API key is in a separate file and correctly named “google_api_key.txt” or our code won’t be able to open the file. 

After this begin with the “python3 user_preference.py” arguments and press enter

The code should prompt you for your name, and you can enter your name. 

Then the code will introduce you to the project and ask for which metro stop you would like to get off at. 
Type in one stop exactly as printed by the list of places in the terminal. 

After this it will ask which activity type you prefer, enter in one activity type. 
Then it will ask about maximum walking distance, enter an integer.  
The code will then output the location coordinates of the stop in longitude and latitude. 
The code will then output the top 5 recommendations, formatted in a list with name, activity type, and distance from stop. 

An example of a code output that worked is: 
Name: Isabel
Metro Stop: Archives
Activity Type: Food 
Maximum Distance: 5

How to Interpret: 
The top 5 recommendations are listed based on the activity type and maximum distance entered by the user. 
In this example, because the user entered “Archives”, “Food” and “5” the program recommended 5 food places to visit within a 5 mile radius of the Archives metro stop. 
