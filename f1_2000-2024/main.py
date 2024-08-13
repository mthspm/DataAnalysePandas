import pandas as pd
import numpy as np
import sqlite3
import os
import matplotlib.pyplot as plt

from typing import List, Tuple, Dict
from utils import *


csvs, dbs = load_files()

pit_df = pd.read_csv(csvs['pitstops'])
results_df = pd.read_csv(csvs['results'])
drivers_df = pd.read_csv(csvs['drivers'])

def get_fastest_pitstop(circuit: str, season: int) -> pd.DataFrame:
    pit_circuit = pit_df[(pit_df['circuitId'] == circuit) & (pit_df['season'] == season)]
    min_time = pit_circuit['duration'].min()
    fastest_pitstop = pit_circuit[pit_circuit['duration'] == min_time].copy()
    return fastest_pitstop

def get_fastest_lap(circuit: str, season: int) -> pd.DataFrame:
    results_df['FastestLapTime'] = results_df['FastestLapTime'].apply(convert_to_seconds)
    results_circuit = results_df[(results_df['Season'] == season) & (results_df['CircuitID'] == circuit)]
    min_time = results_circuit['FastestLapTime'].min()
    fastlap_df = results_circuit[results_circuit['FastestLapTime'] == min_time].copy()
    fastlap_df.loc[:, 'FastestLapTime'] = fastlap_df['FastestLapTime'].apply(convert_to_time_components)
    return fastlap_df

def plot_pitstop_times(pilot: str, circuit: str) -> None:
    pilot_pitstops = pit_df[(pit_df['driverId'] == pilot) & (pit_df['circuitId'] == circuit)]
    pilot_pitstops = pilot_pitstops.sort_values(['season', 'stop'])
    plt.figure(figsize=(10, 6))
    for season in pilot_pitstops['season'].unique():
        season_pitstops = pilot_pitstops[pilot_pitstops['season'] == season]
        plt.plot(season_pitstops['stop'], season_pitstops['duration'], label=f'Season {season}')

    plt.title(f'{pilot} pitstop times at {circuit} over the years')
    plt.xlabel('Stop')
    plt.ylabel('Duration (s)')
    plt.legend()
    plt.show()

def plot_fastestlap_times(pilot: str, circuit: str) -> None:
    pilot_results = results_df[(results_df['DriverID'] == pilot) & (results_df['CircuitID'] == circuit)]
    pilot_results = pilot_results.sort_values(['FastestLapTime'])
    plt.figure(figsize=(10, 6))
    plt.bar(pilot_results['Season'], pilot_results['FastestLapTime'])
    plt.xticks(ticks=range(pilot_results['Season'].min(), pilot_results['Season'].max() + 1, 1))
    plt.title(f'{pilot} fastest lap times at {circuit} over the years')
    plt.xlabel('Season')
    plt.ylabel('Time')
    plt.show()

def plot_pilots_nationalities() -> None:
    plt.figure(figsize=(12, 8))
    drivers = drivers_df['Nationality'].value_counts()
    drivers.plot(kind='barh')
    plt.title('Number of pilots per country')
    plt.xlabel('Number of pilots')
    plt.ylabel('Country')
    plt.show()

def plot_pilots_average_speed(circuit: str) -> None:
    pilots = ['hamilton', 'vettel', 'alonso', 'raikkonen',
              'bottas', 'ricciardo', 'perez', 'norris', 'leclerc', 'sainz',
              'ocon', 'stroll', 'gasly', 'tsunoda', 'latifi', 'russell',
              'max_verstappen']
    pilot_speeds = {}
    for pilot in pilots:
        pilot_results = results_df[(results_df['DriverID'].str.lower() == pilot) & (results_df['CircuitID'] == circuit)]
        number_races = pilot_results.shape[0]
        pilot = f"{pilot} {number_races}"
        pilot_speeds[pilot] = pilot_results['AverageSpeed'].mean()
    pilot_speeds = pd.Series(pilot_speeds)
    pilot_speeds = pilot_speeds.sort_values()
    plt.figure(figsize=(15, 8))
    pilot_speeds.plot(kind='barh')
    plt.title(f'Average speed of pilots on {circuit}')
    plt.xlabel('Average speed (km/h)')
    plt.ylabel('Pilots - Number of Races')
    plt.show()

plot_pilots_average_speed('monza')