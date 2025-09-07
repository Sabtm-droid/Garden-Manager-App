# Imports
import csv
from datetime import datetime , timedelta, date
from IPython.display import Image, display
from tabulate import tabulate

# Initializing Lists
care_file_name  = r"garden_activity.csv"
care_field_name = ["ID","Date", "Activity","image_path"]
activity_types = ["watering", "fertilizing", "repotting", "pruning","image"]

plant_file_name = "gardenapp.csv"
plant_field_name = ["ID", "Plant_Name","Location","Date", "Frequency", "Sunlight_Need"]

seasonal_changes_file_name = 'seasonal_changes.csv'
seasonal_changes_field_name = ["ID","Hot_Season", "Cool_Season","Transitions"]
seasons_months = {
    'Cool': ['Dec', 'Jan', 'Feb'],
    'Hot':['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep','Oct'],
    'Transitions': ['Mar', 'Nov']
    }

# =====================================     
# Team Member 3 Code, Abdulrahman: Strech #2, #4 and extra needed for it to work
# ===================================== 
def enter_to_continue():
    input('Press enter to continue:')

def auto_update_plant_frequencies():
    '''This function updates the frequency of each plant, based on the season 
    and notifies the user if so; creates Seasonal_Changes.csv if not found.'''

    seasonal_dict = {}

    # Try reading Seasonal_Changes.csv, if not found create it with defaults
    try:
        with open(seasonal_changes_file_name, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                seasonal_dict[row["ID"]] = {
                    "Hot": int(row["Hot_Season"]),
                    "Cool": int(row["Cool_Season"]),
                    "Transitions": int(row["Transitions"])
                }
    except FileNotFoundError:
        # File missing → create with plants frequencies
        with open(plant_file_name, newline="") as plants_file:
            plant_reader = csv.DictReader(plants_file)
            plant_rows = list(plant_reader)

        with open(seasonal_changes_file_name, "w", newline="") as season_file:
            fieldnames = ["ID", "Hot_Season", "Cool_Season", "Transitions"]
            writer = csv.DictWriter(season_file, fieldnames=fieldnames)
            writer.writeheader()
            for plant in plant_rows:
                pid = plant["ID"]
                base_freq = plant["Frequency"]  # use plant's frequency as default
                writer.writerow({
                    "ID": pid,
                    "Hot_Season": base_freq,
                    "Cool_Season": base_freq,
                    "Transitions": base_freq
                })
        print("Seasonal_Changes.csv created with plant frequencies as defaults.")
        return  # no need to continue, since there is nothing to update

    updated_plants = []
    #get the current month
    current_month = datetime.now().strftime("%b")

    with open(plant_file_name, newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for plant in reader:
            plant_id = plant["ID"]
            current_freq = int(plant["Frequency"])  # existing frequency
            new_freq = current_freq  # default to current

            if plant_id in seasonal_dict:
                season_freqs = seasonal_dict[plant_id]
                # Determine season
                current_season = None
                for season, months in seasons_months.items():
                    if current_month in months:
                        current_season = season
                        new_freq = season_freqs[season]
                        break

                # Update only if different
                if current_freq != new_freq:
                    plant["Frequency"] = new_freq
                    print(f"\nNote: Plant ID {plant_id} frequency changed to {new_freq} ({current_season} season)\n")

            updated_plants.append(plant)

    #Write updated plants back to CSV
    with open(plant_file_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_plants)

def get_int_larger_then_zero(quastion):
    '''Checks if the input is a number larger then zero'''
    while True:
        try:
            value = int(input(quastion))
            if value > 0:
                return value
            else:
                print("The number must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")

def add_seasonal_change(id_value, freq, answer):
    '''Add a seasonal changes to the frequency, if the user want to add,
       the user can choose a frequency for each season, 
       else all seasons will have the previously inputed frequency'''

    with open(seasonal_changes_file_name, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=seasonal_changes_field_name)

        # If file is empty, write header
        if file.tell() == 0:
            writer.writeheader()

        if answer.lower() in ("no", "n"):
            # All columns = freq
            row = {
                "ID": id_value,
                "Hot_Season": freq,
                "Cool_Season": freq,
                "Transitions": freq
            }
            writer.writerow(row)

        else:
            # Ask user for each seasonal frequency
            hot = get_int_larger_then_zero("Enter frequency for hot seasons: ")
            cool = get_int_larger_then_zero("Enter frequency for cool seasons: ")
            transitions = get_int_larger_then_zero("Enter frequency for transitions between seasons: ")

            row = {
                "ID": id_value,
                "Hot_Season": hot,
                "Cool_Season": cool,
                "Transitions": transitions
            }
            writer.writerow(row)

def update_season_care_freq():
    '''Enables the user to update seasonal frequency for each season for the choosen plant id by the user'''

    rows = []
    found = False   # To track if ID exists in Seasonal_Changes.csv

    while True:  # ID input while checking ig it exist in the main table
        p_id = input("Enter plant ID: ").strip()
        if check_id(p_id):
            break
        else:
            print("Plant not found in Plants.csv. Please try again.")

    # Ask user for each seasonal frequency
    u_hot = get_int_larger_then_zero("Enter frequency for hot seasons: ")
    u_cool = get_int_larger_then_zero("Enter frequency for cool seasons: ")
    u_transitions = get_int_larger_then_zero("Enter frequency for transitions between seasons: ")

    # Read all rows into rows list
    with open(seasonal_changes_file_name, 'r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

        for row in reader:
            if row['ID'] == str(p_id):   # Match ID
                row['Hot_Season'] = u_hot
                row['Cool_Season'] = u_cool
                row['Transitions'] = u_transitions
                found = True
            rows.append(row)

    # If not found, append new row
    if not found:
        rows.append({
            "ID": p_id,
            "Hot_Season": u_hot,
            "Cool_Season": u_cool,
            "Transitions": u_transitions
        })

    # Write everything back
    with open(seasonal_changes_file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    if found:
        print(f"Updated seasonal care for Plant ID {p_id}")
    else:
        print(f"Added new seasonal care record for Plant ID {p_id}")

# =====================================
# Team Member 1 Code, Salman: Function #1
# =====================================
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
                print("\033[1;31;48m ERROR: Name cannot be empty!\033[0m")
        except:
            print("\033[1;31;48m ERROR: Enter a valid name!\033[0m")

    # 2.Location 
    while True:
        try:
            plant['Location'] = input("Enter the plant's location: ")
            if plant['Location'].strip() != "":
                break
            else:
                print("\033[1;31;48m ERROR: Location cannot be empty!\033[0m")
        except:
            print("\033[1;31;48m ERROR: Enter a valid location!\033[0m")

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
            print("\033[1;31;48m ERROR: Invalid date format! Please use YYYY-MM-DD.\033[0m")

    # 4.Watering_frequency Loop
    while True:
        try:
            plant['Frequency'] = input("Enter the watering frequency (per day): ")
            if int(plant['Frequency']) >0:
                break
            else:
                print("\033[1;31;48m ERROR: Write a number greater than zero!\033[0m")
        except:
            print("\033[1;31;48m ERROR: Enter a valid number!\033[0m")

    # 5.Sunlight_needs Loop
    while True:
        try:
            plant['Sunlight_Need'] = input("Enter the sunlight needs (Low, Medium, High): ")
            if (plant['Sunlight_Need'].strip().lower()) in ('low', 'medium', 'high'):
                break
            else:
                print("\033[1;31;48m ERROR: Please choose from: (Low, Medium, High).\033[0m")
        except:
            print("\033[1;31;48m ERROR: Enter a valid number!\033[0m")

# =====================================     
# Team Member 3 Code, Abdulrahman: added this for the strech #4
# ===================================== 
    while True:
        answer = input('Do you want to add seasonal care schedules?(yes or no): ')
        if answer.strip().lower() in ('yes', 'no', 'y', 'n'):
            add_seasonal_change(id_value = plant['ID'], freq = plant['Frequency'], answer = answer)
            break
        else:
            print("Invalid answer. Please enter yes or no.")
# ===================================== 

    # Appending plant's data into the CSV file
    with open(plant_file_name, "a", newline="") as file:
        table = csv.DictWriter(file, fieldnames = plant_field_name)
        #table.writeheader()
        table.writerow(plant) 

    print("\033[1;32;48m Your plant has been added successfully!\033[0m")

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

# =====================================     
# Team Member 2 Code, Abdulla: Function #2
# =====================================  

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
        print("\033[1;31;48m Error while process the files.\033[0m")
        return False

def nextavailablefilename():
    """find available image name to avoid name conflict"""
    return "image"+str(len(get_care_content())+1)
   
def record_plant_care():
    """allow user to record activity for plants"""

    activity_type=''
    while True: #ID loop
        pid = input("Enter plant ID: ").strip()
        if check_id(pid):
            break
        else:
            print("\033[1;31;48m Plant not found. please try again.\033[0m")

    while True: #activity type loop
        activity = input("Enter activity type: ").strip().lower()
        if activity in activity_types:
            break
        else:
            print("\033[1;31;48m Not valid activity type. please try again.\033[0m")
    
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
            
            print("\033[1;31;48m not Valid date. try again or press Enter for today date.\033[0m")
    image_path = ""
    if activity == "image" :
        while True : #image loop
            try:
                image_path = input("Enter image path")
                with open(image_path, "rb") as original: # check if image exists
                    extension  = image_path.split(".")[-1]
                    new_image_path = "./images/"+nextavailablefilename()+ "." + extension
                    with open(new_image_path, "wb") as copy:
                        copy.write(original.read())
                    image_path = new_image_path
                    break
            except FileNotFoundError as e:
                print(e)
                print("\033[1;31;48m Enter valid image path.\033[0m")

    add_new_record(pid, activity_type=activity, activity_date=activity_date,
                   image_path=image_path)
    
    print("\033[1;32;48m Care recorded has been updated.\033[0m")

# =====================================
# Team Member 3 Code, Adbulrahman: Function #3
# =====================================
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

    enter_to_continue()

# =====================================
# Team Member 4 Code, Komail: Function #4
# =====================================
def Search_Plants():
    ''' Search for plants from database by their name or location '''

    # Intializing name and location
    name=''
    location=''
    
    while True:
        try:
            search_by = input("Enter your search method: 1 for plant's name, 2 for plant's location. ")
            if search_by == '1':
                name = input("Enter the plant's name: ")
                break
            elif search_by == '2':
                location = input("Enter the plant's location: ")
                break
            else:
                print("\033[1;31;48m ERROR: Enter either 1 or 2!\033[0m")
        except:
            print("\033[1;31;48m ERROR: Enter a valid number!\033[0m")

    with open('gardenapp.csv', 'r') as file:
        content = csv.DictReader(file)
        found = False
        for plant in content:
            # To check if matching either by name or location
            if plant['Plant_Name'] == name.strip().lower() or plant['Location'] == location.strip().lower():
                print(plant)
                found = True
            
        if not found: 
            print("\033[1;31;48m Sorry, there is no plant with such name or location.\033[0m")
    enter_to_continue()
# =====================================
# Team Member 5 Code, Mohammed: Function #5
# =====================================
def show():
    try:
        # Abdulrahman added this to make the resault pretty
        #This function will show all the plants in the garden
        with open("gardenapp.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        # First row is usually the header
        headers = rows[0]
        data = rows[1:]

        # Print formatted table
        print(tabulate(data, headers=headers, tablefmt="pretty"))



        for item in get_care_content():
            if item["Activity"] != "image":
                print(f'plant {item["ID"]} get {item["Activity"]} at {item["Date"]}')
        print("image gallery")
        for item in get_care_content():
            try:
                if item["Activity"] == "image" and item["image_path"].strip() != '':
                    print(f'image for plant {item["ID"]} get {item["Activity"]} at {item["Date"]}')
                    display(Image(filename=item["image_path"]))
            except:
                pass
    except:
        print("\033[1;31;48m File does not exist!\033[0m")
        enter_to_continue()

# =====================================     
# Team Member 4 Code, Komail: Strech #1
# ===================================== 
def add_plant_length(pid: int, length: float):
    ''' To add plant length to the main CSV file'''
    with open('gardenapp.csv', 'r') as file:
        content = csv.DictReader(file)
        for plant in content:
            if plant['ID'] == pid:
                plant['length'] = length

# Needs mechanism to determine how the length is changing, either by time, care records, or plant type

# =====================================     
# Team Member 2 Code, Abdulla: Strech #3
# =====================================    
def enter_to_continue():
    input('Press enter to continue:')

def add_new_record(pid, activity_type,activity_date=None, image_path=''):
    """ This function updates the care CSV file by taking the inputs from user."""
    
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
        print("\033[1;31;48m Error while save the file.\033[0m")
    except FileNotFoundError:
        print(f"creating {care_file_name}")
        add_new_record(pid, activity_type,activity_date)

# =====================================    
# Team Member 1 Code, Salman: Strech #5
# =====================================
def plant_diagnoses():
    print("Welcome to diagnose common plant problems!")
    
    while True:
        print("\n Plant Diagnosis System ")
        print("1. Yellow leaves")
        print("2. No fruits")
        print("3. Wilting")
        print("4. Brown spots on leaves")
        print("5. Holes in leaves")
        print("6. White powder on leaves")
        print("7. Dropping leaves")
        print("8. Exit")
    
        choice = input("Enter your choice from 1 to 8: ").strip()
    
        if choice == '1':
            print("Diagnosis: Overwatering, poor drainage, or nitrogen deficiency.\nFix: Reduce watering, check soil drainage, and consider fertilizer.")
        elif choice == '2':
            print("Diagnosis: Lack of pollination, insufficient sunlight, or too much nitrogen.\nFix: Ensure 6–8 hours of sunlight, encourage pollinators, reduce nitrogen fertilizer.")
        elif choice == '3':
            print("Diagnosis: Underwatering, root rot (from overwatering), or heat stress.\nFix: Water regularly, improve soil drainage, provide shade in extreme heat.")
        elif choice == '4':
            print("Diagnosis: Fungal infection, bacterial leaf spot, or sunburn.\nFix: Remove affected leaves, improve air circulation, avoid overhead watering.")
        elif choice == '5':
            print("Diagnosis: Insect pests like caterpillars, beetles, or slugs.\nFix: Inspect leaves, remove pests manually, or use organic pest control.")
        elif choice == '6':
            print("Diagnosis: Powdery mildew (fungal disease).\nFix: Improve airflow, avoid overcrowding, apply fungicide if severe.")
        elif choice == '7':
            print("Diagnosis: Sudden temperature change, low light, or overwatering.\nFix: Place plant in stable conditions with proper light and watering schedule.")
        elif choice == '8':
            print("Thank you for using Diagnosing Feature. Take care of your plant!")
            break
        else:
            print("\033[1;31;48m Invalid choice. Please enter a number between 1 and 8.\033[0m")
        enter_to_continue()


# ==========================================================================
# ==========================================================================

# This function is not defined to use solely, ONLY inside main()
def display_menu():
    """Display the main menu options."""
    auto_update_plant_frequencies()
    print("\n=== Garaden Manegar ===")
    print("1. Add a new plant to the collection")
    print("2. Record a plant care activity")
    print("3. View plants due for care")
    print("4. Search plants by name or location")
    print("5. View all plants")
    print("6. Update seasonal care schedule for a plant")
    print("7. Diagnose Plant Symptoms")
    print("8. Exit")
    return input("\nEnter your choice (1-8): ")

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
            update_season_care_freq()
        elif choice == '7':
            plant_diagnoses()
        elif choice == '8':
            print("\nThank you for using Garaden Manegar. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 8.")
