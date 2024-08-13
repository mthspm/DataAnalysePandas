from pathlib import Path
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Analyzer:
    def __init__(self):
        self.data_csv = Path(__file__).parent.parent / "data" / "World population growth rate by cities 2024.csv"
        self.data: pd.DataFrame = pd.read_csv(self.data_csv)
        self.debug_mode = True

    def debug(self):
        print(self.data.info()) # Check the data types and null value s
        print(self.data.describe().T) # Check the statistics of the data
        print(self.data.dtypes) # Check the data types
        print(self.data.isna().mean()) # #Check if there is null values in data

        for col in self.data.columns: # Check the unique values in each column
            print(f"Counts of items in {col} -->> \n {self.data[col].value_counts()}")
            print("-"*25)

        print(self.data.describe(include="0").T)



    def save_statistics(self, name: str, path: str = Path(__file__).parent.parent / "data"):
        """
        Save statistics in Excel file
        :param name: Name of the file
        :param path: Path to save the file (default: ../data folder)
        :return: None
        """
        excel_statistics_path = Path(path) / f"{name}.xlsx"
        data_statistics = self.data.describe().T
        data_statistics.to_excel(excel_statistics_path)


    def plot_most_populated_cities(self,
                                   year: str = "Population (2024)",
                                   country: List[str] = None,
                                   continent: List[str] = None,
                                   range_cities: int = 10):
        """
        Plot the most populated cities in given parameters
        :param year: Year to plot (default: "Population (2024)") - Example : "Population (2023)"
        :param country: List of countries to filter (default: None) - Example : ['Brazil', 'Argentina']
        :param continent: List of continents to filter (default: None) - Example : ['South America']
        :param range_cities: Number of cities to plot (default: 10) - Example : 20
        :return: None
        """

        temp_data = self.data.copy()
        if country:
            temp_data = self.data[self.data['Country'].isin(country)]

        if continent:
            temp_data = self.data[self.data['Continent'].isin(continent)]

        top_cities = temp_data.nlargest(range_cities, year)
        location = ', '.join(country) if country else ', '.join(continent) if continent else 'The World'

        plt.figure(figsize=(12, 8))
        sns.barplot(x='City', y=year, data=top_cities, palette='viridis', legend=False, hue='City')
        plt.xticks(rotation=45)
        plt.title(f'Top {range_cities} most populated cities in {year.split()[-1]} in {location}')
        plt.xlabel('City')
        plt.ylabel(f'Population {year.split()[-1]}')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    analyzer = Analyzer()
    if analyzer.debug_mode: analyzer.debug()