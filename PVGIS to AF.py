#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 12:38:37 2024

@author: barnabywinser
"""

import pandas as pd

# Assuming a full-year dataset with UTC time in 30-minute intervals


folder = "/Users/barnabywinser/Library/CloudStorage/OneDrive-SharedLibraries-Rheenergise/Commercial - Documents/Opportunities/Enlasa/Co-location/inputs/solar data/"
inputfile = "vertical.csv"
outputfile = "test.xlsx"
data = pd.read_csv(folder + inputfile, skiprows=10, usecols=[0, 1], skipfooter=12)

df = pd.DataFrame(data)

timezn = 'America/Santiago'

"This section converts to the local timezone"

# Convert 'time' to datetime format
df['time'] = pd.to_datetime(df['time'], format='%Y%m%d:%H%M')

# Convert from UTC to Chilean local time
df['time'] = df['time'].dt.tz_localize('UTC').dt.tz_convert(timezn)

# Step 1: Shift the time backwards by 30 minutes to align it with full hours
df['time'] = df['time'] - pd.Timedelta(minutes=30)

# Step 2: Remove the timezone information but keep the local time in Chile
df['time'] = df['time'].dt.tz_localize(None)

# Step 3: Set 'time' as the index and resample to hourly intervals (average the data)
df.set_index('time', inplace=True)

"Finds AF and saves"

# Add a calculated field
df['AF'] = df['P'] / 1000

# Save the result to an Excel file
df.to_excel(folder + outputfile)

"Checks for missing times and NaN values"

# Check for missing times in the DataFrame
full_time_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq='H')
missing_times = full_time_index.difference(df.index)

if not missing_times.empty:
    print(f"Missing times detected: {missing_times}")
else:
    print("No missing times detected in the data.")
    
# Check for NaN values in other columns
nans_in_columns = df.isna().sum()

# Log columns with NaN values and their locations
if nans_in_columns.any():
    print("NaN values detected in the following columns:")
    for column in df.columns:
        nan_rows = df[df[column].isna()]
        if not nan_rows.empty:
            print(f"\nColumn '{column}' has {len(nan_rows)} NaN(s) at the following times:")
            print(nan_rows.index.tolist())
else:
    print("No NaN values detected in columns.")

# Fill NaNs with the average of the previous and next values
df.interpolate(method='linear', inplace=True)

# Verify if all NaNs are filled
remaining_nans = df.isna().sum()
if remaining_nans.any():
    print("Warning: Some NaN values could not be filled.")
else:
    print("All NaN values have been filled.")