# Imports
import math
import csv
from datetime import datetime , timedelta
#This is a sample of the main python file
# Team Member 1 Code, Abulla: Function #1
    
# Team Member 2 Code, Salman, Function #2

# Team Member 3 Code, Abdulrahman, Function #3&4

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
            function_1()
        elif choice == '2':
            function_2()
        elif choice == '3':
            View_plants_due_for_care_per_activity()
        elif choice == '4':
            function_4()
        elif choice == '5':
            function_5()
        elif choice == '6':
            print("Thank you for using Garaden Manegar. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

#Team Member 4 Code, Mohammed, Function #5