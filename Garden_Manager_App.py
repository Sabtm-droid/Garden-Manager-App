# Imports
import math
import csv
#Team Member 5 Code, Mohammed, Function #5
def show():
    try:
        #This function will show all the plants in the garden
        with open(r'C:\Users\158585\Desktop\gardenapp.csv', 'r') as file:
            csv1= csv.reader(file)
            for i in csv1:
                print(i)
    except:
        print("File does not exist!")


show()
