# Imports
import math
#This is a sample of the main python file
# Team Member 1 Code, Salman: Function #1

# Team Member 2 Code, Abdulla, Function #2
plant_file_name = r"gardenapp.csv"
care_file_name  = r"garden_activity.csv"
plant_column_header = ["id", "name", "date_planted", "water_freq", "sunlight"]
care_column_header = ["id","date", "activity"]
activity_types = ["test1"]
import csv
import datetime
from datetime import date
def get_plant_content():
    """Extract content of plant table and return it as list of dict"""
    try: 
        with open(plant_file_name, "r") as file:
            table = csv.DictReader(file, fieldnames=plant_column_header)
            return list(table)
    except FileNotFoundError:
        print(f"file {plant_file_name} not found")
        with open(plant_file_name, "w", newline='') as file:
            pass
        print("creating", plant_file_name)
        return []
        
def get_care_content():
    """Extract content of plant table and return it as list of dict"""
    try:    
        with open(care_file_name, "r", newline='') as file:
            table = csv.DictReader(file, fieldnames=care_column_header)
            return list(table)
    except FileNotFoundError:
        print(f"file {care_file_name} not found")
        with open(plant_file_name, "w", newline='') as file:
            pass
        print("creating", care_file_name)
        return []
        
def check_id(pid):
    """check if plant ID exist in table
    return True if id found or return False otherwise
    """
    try:
        
        for item in get_plant_content():
            
            if item[plant_column_header[0]] == pid:
                
                return True
        return False
    except KeyError:
        print("Error while process the files")
        return False

def add_new_record(pid, activity_type,activity_date=None):
    if activity_date == None: # if no date provided use current date
        activity_date = date.today().strftime("%Y-%m-%d")
    try:
        with open(care_file_name, "a", newline="") as file:
            table = csv.DictWriter(file,fieldnames=care_column_header)
            table.writerow({
                care_column_header[0]: pid,
                care_column_header[2]: activity_type,
                care_column_header[1]: activity_date
            })
    except KeyError:
        print("Error while save the file")
    except FileNotFoundError:
        print(f"creating {care_file_name}")
        add_new_record(pid, activity_type,activity_date
                      )
def record_plant_care():
    """allow user to record activity for plants"""
    
    activity_type=''
    while True: #ID loop
        pid = input("Enter plant ID: ").strip()
        if check_id(pid):
            break
        else:
            print("Plant not found. please try again")

    while True: #activity type loop
        activity = input("Enter activity type: ").strip().lower()
        if activity in activity_types:
            break
        else:
            print("Not valid activity type. please try again")
    
    while True: # activity date loop
        try:
            user_date = input("please Enter date in format YYYY-MM-DD or press Enter for today date").strip()
            if not user_date.strip():  # Use today's date
                activity_date = date.today().strftime("%Y-%m-%d")
                break
            else:
                activity_date = datetime.datetime.strptime(user_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                break
        except Exception as e:
            
            print("not Valid date. try again or press Enter for today date")
    
    add_new_record(pid, activity_type=activity, activity_date=activity_date)
record_plant_care()
def add_new_plant():
    # find next ID
    if len(get_plant_content()) == 0:
        pass
    next_id = 1
    for row in get_plant_content():
        row["id"]
            



# Team Member 3 Code, Abdulrahman, Function #3

#Team Member 4 Code, Komail, Function #4

#Team Member 5 Code, Mohammed, Function #5
