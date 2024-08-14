import pandas as pd
import numpy as np

df: pd.DataFrame = pd.read_csv("IEA Global EV Data 2024.csv")

####DEBUG####

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


# Data Filter

# Electric Vehicles Sales
EV_df = df[(df['parameter'] == 'EV sales')]

# Clear Prediction Sales
years_to_remove = [2025, 2030, 2035]
EV_df = EV_df[~EV_df['year'].isin(years_to_remove)]

# Electric Cars Dataframe and sells amount
EC_df = EV_df[EV_df['mode'] == 'Cars']
EC_sells_amount = len(EC_df)

# Electric Buses Dataframe and sells amount
EB_df = EV_df[EV_df['mode'] == 'Buses']
EB_sells_amount = len(EB_df)

ECB_sells_amount = EC_sells_amount + EB_sells_amount

# Most selled powertrains tecnologies in Electric Vehicles Category
power_trains_df = EV_df['powertrain'].value_counts()

print(power_trains_df)