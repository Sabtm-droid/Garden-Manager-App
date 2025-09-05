# Imports
import csv
from datetime import date, datetime , timedelta

# Initializing Lists
care_file_name  = r"garden_activity.csv"
care_field_name = ["ID","Date", "Activity","image_path"]
activity_types = ["watering", "fertilizing", "repotting", "pruning","image"]
plant_file_name = "gardenapp.csv"
plant_field_name = ["ID", "Plant_Name","Location","Date", "Frequency", "Sunlight_Need"]

# Team Member 1 Code, Salman: Function #1
# FUNCTION 1 =====================================
def new_plant():
    # ADD DOC string
    
    plant = {}  
    
    # ID
    plant['ID'] = nextID() #Autogenerating sequential IDs 
        
    # 1.Name Loop 
    while True:
        try:
            plant['Plant_Name'] = input("Enter the plant's name/species: ")
            if plant['Plant_Name'].strip() != "":
                break
            else:
                print("ERROR: Name cannot be empty!")
        except:
            print("ERROR: Enter a valid name!")

    # 2.Location 
    while True:
        try:
            plant['Location'] = input("Enter the plant's location: ")
            if plant['Location'].strip() != "":
                break
            else:
                print("ERROR: Location cannot be empty!")
        except:
            print("ERROR: Enter a valid location!")

    # 3.Date_acquired Loop
    while True:
        plant['Date'] = input("Enter the Date (YYYY-MM-DD), or press Enter for today: ")
        if not plant['Date'].strip():  # Use today's date
            plant['Date'] = date.today().strftime("%Y-%m-%d")
            break
        try:
            datetime.strptime(plant['Date'], "%Y-%m-%d")
            break
        except ValueError:
            print("ERROR: Invalid date format! Please use YYYY-MM-DD.")

    # 4.Watering_frequency Loop
    while True:
        try:
            plant['Frequency'] = input("Enter the watering frequency (per day): ")
            if int(plant['Frequency']) >0:
                break
            else:
                print("ERROR: Write a number greater than zero!")
        except:
            print("ERROR: Enter a valid number!")

    # 5.Sunlight_needs Loop
    while True:
        try:
            plant['Sunlight_Need'] = input("Enter the sunlight needs (Low, Medium, High): ")
            if (plant['Sunlight_Need'].strip().lower()) in ('low', 'medium', 'high'):
                break
            else:
                print("ERROR: Please choose from: (Low, Medium, High).")
        except:
            print("ERROR: Enter a valid number!")

    # Appending plant's data into the CSV file
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
        # print(f"ERROR: File {plant_file_name} was not found!")
        with open(plant_file_name, "w", newline='') as file:
            pass
        print(f"{plant_file_name} is created.")
        return []
        
def get_care_content():
    """Extract content of plant table and return it as list of dict"""
    try:    
        with open(care_file_name, "r", newline='') as file:
            table = csv.DictReader(file, fieldnames=care_field_name)
            return list(table)
    except FileNotFoundError:
        # print(f"ERROR: File {care_file_name} was not found")
        with open(plant_file_name, "w", newline='') as file:
            pass
        print(f"{care_file_name} is created.")
        return []

def nextID():
    """Find next ID based on CSV table"""
    last_id = 0 
    for item in get_plant_content():
        try:
            if int(item[plant_field_name[0]]) > last_id:
                last_id = int(item[plant_field_name[0]])
        except:
            pass
    return last_id + 1

def check_id(pid):
    """
    Check if plant ID exist in table
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
    # ADD DOC string
    
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
        add_new_record(pid, activity_type,activity_date)

# FUNCTION 2 =====================================     
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

# FUNCTION 4 =====================================
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

# FUNCTION 5 =====================================
def show():
    try:
        #This function will show all the plants in the garden
        with open('gardenapp.csv', 'r') as file:
            csv1= csv.reader(file)
            for i in csv1:
                print(i)
    except:
        print("File does not exist!")

# FUNCTION 3 =====================================
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

# ==========================================================================
# ==========================================================================

# This function is not defined to use solely, ONLY inside main()
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
