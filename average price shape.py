#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:02:51 2024

@author: barnabywinser
"""

import pandas as pd
import os

# Define the directory where the files are stored
data_directory = "/Users/barnabywinser/Library/CloudStorage/OneDrive-SharedLibraries-Rheenergise/Commercial - Documents/Market data & analysis/Data bank/Market Data/Chile/raw/raw2/"  # Replace with the actual path to your data files

# Initialize an empty DataFrame to collect all data
all_data = pd.DataFrame()

# Loop through the files in the directory
for filename in os.listdir(data_directory):
    if filename.endswith("_costos-marginales-reales.csv"):
        # Load the file into a DataFrame
        file_path = os.path.join(data_directory, filename)
        df = pd.read_csv(file_path)
        
        # Ensure the datetime column is properly formatted
        df.rename(columns={df.columns[0]: 'Datetime'}, inplace=True)
        
        # Replace "24" hour with "00" and increment the date by one day
        def fix_hour_24(datetime_str):
            if datetime_str[-2:] == "24":
                date_part = datetime_str[:-3]  # Extract the date portion
                new_datetime = pd.Timestamp(date_part) + pd.Timedelta(days=1)
                return new_datetime.strftime("%Y-%m-%d 00")
            return datetime_str
        
        # Apply the fix to the Datetime column
        df['Datetime'] = df['Datetime'].apply(fix_hour_24)
        
        # Convert to datetime
        df['Datetime'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H')
        
        # Select only the Atacama region data
        atacama_data = df[['Datetime', 'Atacama']].copy()
        
        # Append the data to the collective DataFrame
        all_data = pd.concat([all_data, atacama_data], ignore_index=True)

# Add a column for year and month
all_data['Year'] = all_data['Datetime'].dt.year
all_data['Month'] = all_data['Datetime'].dt.month

# Define multi-year summer and winter periods
def assign_season_period(row):
    if row['Month'] in [10, 11, 12, 1, 2, 3]:  # Summer
            return f"Summer {row['Year']}"
    elif row['Month'] in [4, 5, 6, 7, 8, 9]:  # Winter
            return f"Winter {row['Year']}"

all_data['Season_Period'] = all_data.apply(assign_season_period, axis=1)

# Filter for only summer and winter data
all_data = all_data[all_data['Season_Period'].notnull()]

# Extract the hour of the day
all_data['Hour'] = all_data['Datetime'].dt.hour

# Calculate the hourly average price shape for each summer/winter period
average_price_shape = all_data.groupby(['Season_Period', 'Hour'])['Atacama'].mean().reset_index()

# Rename columns for clarity
average_price_shape.rename(columns={'Atacama': 'Average Price'}, inplace=True)

# Add the Year column to the final DataFrame
average_price_shape['Year'] = average_price_shape['Season_Period'].apply(
    lambda season: all_data.loc[all_data['Season_Period'] == season, 'Year'].unique()[0]
)


# Save the long-format data to a CSV for Tableau visualization
output_path = "/Users/barnabywinser/Library/CloudStorage/OneDrive-SharedLibraries-Rheenergise/Commercial - Documents/Market data & analysis/Data bank/Market Data/Chile/raw/priceshape.csv"  # Replace with your desired output path
average_price_shape.to_csv(output_path, index=False)

print(f"Average price shape saved to {output_path}")