# Imports
import csv
from datetime import datetime , timedelta
from datetime import date
#This is a sample of the main python file

care_file_name  = r"garden_activity.csv"
care_field_name = ["ID","Date", "Activity","image_path"]
activity_types = ["watering", "fertilizing", "repotting", "pruning","image"]
plant_file_name = "gardenapp.csv"
plant_field_name = ["ID", "Plant_Name","Location","Date", "Frequency", "Sunlight_Need"]

# Team Member 1 Code, SAlman: Function #1
# Garden manager App
# add a new plant with these features
# 1. Plant name/species
# 2. Location in home
# 3. Date acquired
# 4. Watering frequency (in days)
# 5. Sunlight needs (Low, Medium, High)

# Firstly, we will store the plants in a list of dictionaries
def new_plant ():
    plant = {}
    # plant ['ID'] = input (" Enter the unique ID of the plant")
    # plant ["Plant_Name"] = input("Enter plant name/species: ")
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
                        print("ID is exsited. Enter another one.")
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
            plant ['Plant_Name'] = input ("Enter plant name/species: ")
            break
        except:
            print("enter valid name")

    # Location Loop
    try:
        plant ['Location'] = input ("Enter the location of the plant")
    except:
        print("enter valid location")

    # Date_acquired Loop
    while True:
            plant [ "Date"] = input("Enter Date_acquired (YYYY-MM-DD) or press Enter for today: ")
            if not plant [ "Date"].strip():  # Use today's date
                plant [ "Date"] = date.today().strftime("%Y-%m-%d")
                break
            try:
                datetime.strptime(plant [ "Date"], "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    # Watering_frequency Loop
    while True:
        try:
            plant ['Frequency'] = input (" Enter watering frequency in a day ")
            if int(plant ['Frequency'])  >0:
                break
            else:
                print (" Write number more than zero")

        except:
            print("enter valid number")

    # Sunlight_needs Loop
    while True:
        try:
            plant ['Sunlight_Need'] = input (" Enter the sunlight needs: Low, Medium, High")
            if (plant ['Sunlight_Need'])  in ('Low', 'Medium', 'High'):
                break
            else:
                print (" Write: Low, Medium, High")

        except:
            print("enter valid name")

    with open(plant_file_name, "a", newline="") as file:
        table = csv.DictWriter(file, fieldnames = plant_field_name)
        #table.writeheader()
        table.writerow(plant) 

def get_plant_content():
    """Extract content of plant table and return it as list of dict"""
    try: 
        with open(plant_file_name, "r") as file:
            table = csv.DictReader(file, fieldnames=plant_field_name)
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
            table = csv.DictReader(file, fieldnames=care_field_name)
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
            if item[plant_field_name[0]] == pid:
                return True
        return False
    except KeyError:
        print("Error while process the files")
        return False

def add_new_record(pid, activity_type,activity_date=None, image_path=''):
    if activity_date == None: # if no date provided use current date
        activity_date = date.today().strftime("%Y-%m-%d")
    try:
        with open(care_file_name, "a", newline="") as file:
            table = csv.DictWriter(file,fieldnames=care_field_name)
            table.writerow({
                care_field_name[0]: pid,
                care_field_name[2]: activity_type,
                care_field_name[1]: activity_date,
                "image_path":image_path
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
                activity_date = datetime.strptime(user_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                break
        except Exception as e:
            
            print("not Valid date. try again or press Enter for today date")
    image_path = ""
    if activity == "image" :
        while True : #image loop
            try:
                image_path = input("Enter image path")
                with open(image_path, "r") as file: # chack if image exist
                    break
            except:
                print("Enter valid image path")

    add_new_record(pid, activity_type=activity, activity_date=activity_date,
                   image_path=image_path)
#Team Member 4 Code, Komail, Function #4
def Search_Plants():
    ''' Search for plants from database by their name or location '''
    name = input("Enter the plant's name: ")
    location = input("Enter the plant's location: ")

    with open('gardenapp.csv', 'r') as file:
        content = csv.DictReader(file)
        for plant in content:
            # To check if matching either by name or location
            if plant['Plant_Name'] == name or plant['Location'] == location:
                print(plant)

def show():
    try:
        #This function will show all the plants in the garden
        with open('gardenapp.csv', 'r') as file:
            csv1= csv.reader(file)
            for i in csv1:
                print(i)
    except:
        print("File does not exist!")


def View_plants_due_for_care_per_activity():
    '''This function lists all the plants that needs care and what care they need'''
    # Reading the file
    with open('gardenapp.csv', 'r', newline='') as file:
        plants = list(csv.DictReader(file))    

    plant_ids = []
    
    for plant in plants:
        plant_ids.append({'ID': plant['ID'], 'Date': plant['Date'], 'Frequency': plant['Frequency']})
    
    with open('garden_activity.csv', 'r', newline='') as file:
        plants_activities = list(csv.DictReader(file))
        
    activities = ('Watering', 'Fertilizing', 'Repotting', 'Pruning')

    due_plantes_list = []
    for plant in plant_ids:
        p_id = plant['ID']
        p_date = plant['Date']
        p_freq = plant['Frequency']

        activities_needed = []
        for activity in activities:
            max_date = datetime.strptime('1000-01-01', '%Y-%m-%d')
            p_records = []
            for p in plants_activities:
                if p["ID"] == p_id and p["Activity"].lower() == activity.lower():
                    p_records.append(p)
            if not p_records:
                max_date = datetime.strptime(p_date, '%Y-%m-%d')
            else:
                for record in p_records:
                    r_date = datetime.strptime(record['Date'], '%Y-%m-%d')
                    if r_date > max_date:
                        max_date = r_date
            today_date = datetime.today()
            due_date = max_date + timedelta(days=int(p_freq))
            if due_date <= today_date:
                activities_needed.append({'Activity': activity, 'last_date': max_date.strftime('%Y-%m-%d')})
        
        if activities_needed:
            due_plantes_list.append({'ID':p_id, 'Frequency': p_freq, 'Activities_needed': activities_needed})

    print('-----------------------------------------------------------------------------')
    if due_plantes_list:
        print(f'Plants that need care:')
        print('-----------------------------------------------------------------------------\n')
        for plant in due_plantes_list:
            an_for_plant = plant['Activities_needed']
            print(f"Plant with ID: {plant['ID']}, needs:")
            for needed in an_for_plant:
                print(f"    -{needed['Activity']},   last care date: {needed['last_date']}")
            print('-----------------------------------------------------------------------------\n')
    else:
        print(f'No plants need care, Nice Job!')
    print('-----------------------------------------------------------------------------')

def display_menu():
    """Display the main menu options."""
    print("\n=== Garaden Manegar ===")
    print("1. Add a new plant to the collection")
    print("2. Record a plant care activity")
    print("3. View plants due for care")
    print("4. Search plants by name or location")
    print("5. View all plants")
    print("6. Exit")
    return input("Enter your choice (1-6): ")

def main():
    """Main application function."""
    print("Welcome to Garaden Manegar!")
    print("This app helps you plant and maintain your garden plants.")

    while True:
        choice = display_menu()

        if choice == '1':
            new_plant()
        elif choice == '2':
            record_plant_care()
        elif choice == '3':
            View_plants_due_for_care_per_activity()
        elif choice == '4':
            Search_Plants()
        elif choice == '5':
            show()
        elif choice == '6':
            print("Thank you for using Garaden Manegar. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

#Team Member 4 Code, Mohammed, Function #5



