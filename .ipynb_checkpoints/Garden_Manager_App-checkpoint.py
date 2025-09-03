# Imports
import math
#This is a sample of the main python file
# Team Member 1 Code, Abulla: Function #1

# Team Member 2 Code, Salman, Function #2

# Team Member 3 Code, Abdulrahman, Function #3

#Team Member 4 Code, Komail, Function #4
 def SearchPlants(name: str, location: str):
    ''' Search for plants from database by their name or location '''

    name = input("Enter the plant's name: ")
    location = input("Enter the plant's location: ")

    with open('gardenapp.csv', 'r') as file:
        content = csv.DictReader(file)
        for plant in content:
            # To check if matching either by name or location
            if plant['Plant_name'] == name or plant['Location'] == location:
                print(plant)

#Team Member 5 Code, Mohammed, Function #5
