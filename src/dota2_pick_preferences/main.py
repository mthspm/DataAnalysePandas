import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import textwrap
import warnings

warnings.filterwarnings('ignore')

# Load the data
df = pd.read_csv('Current_Pub_Meta.csv')

# Clean up the data
df = df.drop(df.columns[0], axis = 1)
df = df.set_index('Name')

print(df.head())

# Create win df

winCols = [i for i in df.columns if 'Win Rate' in i ]
win_df = df[winCols]
win_df['Lowest Win Rate'] = df[winCols].min(axis = 1)
win_df['Highest Win Rate'] = df[winCols].max(axis = 1)
win_df['Win Rate Delta'] = win_df['Highest Win Rate']/win_df['Lowest Win Rate']
win_df = win_df.sort_values('Win Rate Delta', ascending = False)

# Create pick df

picksCols = [i for i in df.columns if 'Picks' in i]
pick_df = df[picksCols]
pick_df = pick_df.transpose()
pick_df['sums'] = pick_df.sum(axis = 1)

