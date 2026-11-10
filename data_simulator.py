import random
import csv

def simulate():

    # Define column headings/field names

    fieldnames = ['day', 'heart_rate', 'blood_oxygen', 'core_bodyTemp', 'systolic_bloodPressure', 'sleep_hours', 'radiation_exposure']
    data = []



    # Loop runs from 1 through 14, representing 14 days/2 weeks.
    # For each iteration, a random realistic value is generated and saved in a dictionary 'row'. This row is appended to a list 'data'.
    # In the second iteration, the day=2, more data is generated and saved in 'row'. row keeps appending to the list 'data'.

    for i in range(1, 15):

        row = {
            'day': i,
            'heart_rate': random.randint(39, 115),
            'blood_oxygen': random.randint(90, 105),
            'core_bodyTemp': round(random.uniform(35, 43), 2),
            'systolic_bloodPressure': random.randint(97, 115),
            'sleep_hours': random.randint(3, 7),
            'radiation_exposure': random.randint(80, 250)
        }
        data.append(row)

# Now, the list 'data' consists of 14 rows of data dictionaries.
# csv function writes this data and organizes it into a table.


    with open('astronaut_vitals.csv', "w", newline="", encoding="utf-8") as vitals:
        writer = csv.DictWriter(vitals, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(data)


# Using the csv module, read the table that was just generated. Return the last/most recent dated data.

def latest():
    with open('astronaut_vitals.csv', "r", encoding="utf-8") as vitals:
        reader = csv.DictReader(vitals)
        recent_data = list(reader)

        if recent_data:
            return recent_data[-1]      # Returns in dictionary
        else:
            return None

simulate()
print(latest())