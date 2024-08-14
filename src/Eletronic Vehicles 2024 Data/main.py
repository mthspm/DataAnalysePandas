import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df: pd.DataFrame = pd.read_csv("IEA Global EV Data 2024.csv")

#######DEBUG#######

#print(df.head())
#print(df.columns.unique())
#print(df['region'].unique())
#print(df['category'].unique())
#print(df['parameter'].unique())
#print('mode', df['mode'].unique())
#print(df['powertrain'].unique())
#print(df['year'].unique())
#print(df['unit'].unique())
#print(df['value'].unique())

# Electric Vehicles Sales
EV_df = df[(df['parameter'] == 'EV sales') & (df['category'] == 'Historical')]

# Electric Vehicles Prediction Sales
EVP_df = df[((df['category'] == 'Projection-STEPS') | (df['category'] == 'Projection-APS')) & (df['parameter'] == 'EV sales')]

# All Sells by Type of Vehicle
all_modes = EV_df['mode'].value_counts()
print(all_modes)

# Most power trains sold
power_trains_df = EV_df['powertrain'].value_counts()

# Electric Vehicles Sells Historical and Prediction
ev = {}
ev_p = {}

for car_type in EV_df['mode'].unique():
    ev[car_type] = EV_df[EV_df['mode'] == car_type]['value'].sum()
    ev_p[car_type] = EVP_df[EVP_df['mode'] == car_type]['value'].sum()

# Value Plot - Most power trains sold in E-Vehicles 2011-2023

fig, ax = plt.subplots()
ax.bar(power_trains_df.index, power_trains_df.values)
ax.set_xlabel('Power Trains')
ax.set_ylabel('Amount')
ax.set_title('Most power trains sold')
plt.show()

# Pie Chart - Electric Vehicles Sells 2011-2023 (Historical)

fig, ax = plt.subplots()
ax.pie([ev['Cars'], ev['Buses'], ev['Vans'], ev['Trucks']],
       labels=['Cars', 'Buses', 'Vans', 'Trucks'], autopct='%1.1f%%')
ax.set_title('Electric Vehicles Sells 2011-2023')
plt.show()

# Pie Chart - Electric Vehicles Prediction Sales 2024, 2025, 2030, 2035 (STEPS and APS)

fig, ax = plt.subplots()
ax.pie([ev_p['Cars'], ev_p['Buses'], ev_p['Vans'], ev_p['Trucks']],
       labels=['Cars', 'Buses', 'Vans', 'Trucks'], autopct='%1.1f%%')
ax.set_title('Electric Vehicles Prediction Sales 2024, 2025, 2030, 2035')
plt.show()

# Histogram - Quantity of Electric Vehicles Sells Per Year 2011-2023 (Historical)

e_vehicles_sells = {}
for year in EV_df['year'].unique():
    e_vehicles_sells[year] = EV_df[EV_df['year'] == year]['value'].sum()

fig, ax = plt.subplots()
ax.bar(e_vehicles_sells.keys(), e_vehicles_sells.values())
ax.set_xlabel('Year')
ax.set_ylabel('Amount')
ax.set_title('Quantity of Electric Vehicles Sells Per Year 2011-2023')
plt.show()

# Histogram - Quantity of Electric Vehicles Prediction Sales Per Year 2024, 2025, 2030, 2035 (STEPS and APS)

e_vehicles_prediction_sells = {}
for year in EVP_df['year'].unique():
    e_vehicles_prediction_sells[year] = EVP_df[EVP_df['year'] == year]['value'].sum()

fig, ax = plt.subplots()
ax.bar(e_vehicles_prediction_sells.keys(), e_vehicles_prediction_sells.values())
ax.set_xlabel('Year')
ax.set_ylabel('Amount')
ax.set_title('Quantity of Electric Vehicles Prediction Sales Per Year 2024, 2025, 2030, 2035')
plt.show()
