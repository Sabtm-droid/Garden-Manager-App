# Imports
import math
#This is a sample of the main python file
# Team Member 1 Code, SAlman: Function #1
# Garden manager App
# add a new plant with these features
# 1. Plant name/species
# 2. Location in home
# 3. Date acquired
# 4. Watering frequency (in days)
# 5. Sunlight needs (Low, Medium, High)
plant_file_name = "gardenapp.csv"
plant_field_name = ["ID", "Name","Location","Date_acquired", "Watering_frequency", "Sunlight_needs"]

# Firstly, we will store the plants in a list of dictionaries
import csv
import datetime
from datetime import date
def new_plant ():
    plant = {}
    # plant ['ID'] = input (" Enter the unique ID of the plant")
    # plant ["name"] = input("Enter plant name/species: ")
    # plant ["Location"] = input ("Enter the location of the plant")
    # plant [ "Date_acquired"] = input (" Enter Date acquired")
    # plant ["Watering_frequency"] = input (" Enter watering frequency in a day ")
    # plant ["Sunlight_needs"] = input (" Enter the sunlight needs: Low, Medium, High")
   
    # ID Loop
    while True:
    
            
        try:
            plant ['ID'] = input (" Enter the unique ID of the plant")
            
            int(plant ['ID']) 
            with open(plant_file_name, "r") as file:
                table = csv.DictReader(file, fieldnames=plant_field_name)
                for item in table:
                    if item["ID"] == plant ['ID']:
                        continue 
                break
       
        # need to fix error here 
        except FileNotFoundError:
            print(f" Error: The file was not found.")

            with open (plant_file_name, "w", newline = '') as file:
                    pass
            print ("creating", plant_file_name)
                
        
        except Exception as err:
            print(err)
            print("enter valid number")
            raise

        
# Name Loop 
    while True:
        try:
            plant ['Name'] = input ("Enter plant name/species: ")
            break

        except:
            print("enter valid name")

# Location Loop
    
    try:
        plant ['Location'] = input ("Enter the location of the plant")
        

    except:
        print("enter valid name")

# Date_acquired Loop
    
    while True:
            plant [ "Date_acquired"] = input("Enter Date_acquired (YYYY-MM-DD) or press Enter for today: ")
            if not plant [ "Date_acquired"].strip():  # Use today's date
                plant [ "Date_acquired"] = date.today().strftime("%Y-%m-%d")
                break
            try:
                datetime.datetime.strptime(plant [ "Date_acquired"], "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

# Watering_frequency Loop
    while True:
        try:
            plant ['Watering_frequency'] = input (" Enter watering frequency in a day ")
            if int(plant ['Watering_frequency'])  >0:
                break
            else:
                print (" Write number more than zero")

        except:
            print("enter valid number")

# Sunlight_needs Loop
    while True:
        try:
            plant ['Sunlight_needs'] = input (" Enter the sunlight needs: Low, Medium, High")
            if (plant ['Sunlight_needs'])  in ('Low', 'Medium', 'High'):
                break
            else:
                print (" Write: Low, Medium, High")

        except:
            print("enter valid name")

    with open(plant_file_name, "w") as file:
        table = csv.DictWriter(file, fieldnames = plant_field_name)
        table.writeheader()
        table.writerow(plant) 

# Team Member 2 Code, Abdulla, Function #2

# Team Member 3 Code, Abdulrahman, Function #3&4

#Team Member 4 Code, Mohammed, Function #5
