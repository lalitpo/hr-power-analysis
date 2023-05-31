import pandas as pd
import numpy as np
from src.repositories.PowerAndHRRepository import *

athletic_data_db = get_athletic_data()
hr_power_db_conn.close()

# DATA PROFILING : Removing irrelevant columns not required for analysis
cols_to_ignore = configs.get("ignore-columns").data
athletic_data = athletic_data_db.drop(cols_to_ignore.split(","), axis=1)


# DATA CLEANSING : Filling missing data with immediate pre- and post-values' mean
def update_NA_values(lst):
    for i in range(len(lst)):
        if lst[i] is None:
            j = i - 1
            while j >= 0 and lst[j] is None:
                j -= 1
            previous_value = lst[j] if j >= 0 else None
            j = i + 1
            while j < len(lst) and lst[j] is None:
                j += 1
            next_value = lst[j] if j < len(lst) else None
            if previous_value is not None and next_value is not None:
                lst[i] = (previous_value + next_value) / 2
            elif previous_value is not None:
                lst[i] = previous_value
            elif next_value is not None:
                lst[i] = next_value
    return lst


athletic_data['heartrate'] = athletic_data['heartrate'].apply(update_NA_values)
athletic_data['watts'] = athletic_data['watts'].apply(update_NA_values)


# Remove rows with more than half of values as None in heartrate or watts lists
athletic_data = athletic_data[(athletic_data['heartrate'].apply(lambda x: x.count(None) <= len(x) / 2)) &
                              (athletic_data['watts'].apply(lambda x: x.count(None) <= len(x) / 2))]

# Filter the DataFrame based on the activity_id
filtered_data = athletic_data[athletic_data['activity_id'] == 9057354882]

# Get the unique values in the 'watts' list
unique_values = set(filtered_data['watts'].sum())

print(athletic_data)
