#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:30:33 2024

@author: barnabywinser
"""

import pandas as pd
import numpy as np

# Updated data for one day (24 hours)
hourly_data = [
95.13, 95.05, 95.20, 95.31, 95.65, 96.10, 96.70, 97.59,     
98.47, 99.04, 99.44, 99.71, 99.90, 100.00, 99.83, 99.58,    
 99.28, 98.90, 98.30, 97.42, 96.57, 96.01, 95.54, 95.36
]

# Total hours in a year
hours_in_year = 8760

# Repeat the daily pattern to fill a year's worth of data
repeated_data = hourly_data * (hours_in_year // len(hourly_data))

# Create a DataFrame with hourly data and timestamps starting from 2023
timestamps = pd.date_range(start="2023-01-01 00:00:00", periods=hours_in_year, freq="h")
yearly_data = pd.DataFrame({'Timestamp': timestamps, 'Value': repeated_data})

# Display the first few rows
print(yearly_data.head())

# Save to a CSV file (optional)
yearly_data.to_csv("/Users/barnabywinser/Library/CloudStorage/OneDrive-SharedLibraries-Rheenergise/Commercial - Documents/Cost Models/ESC Co-Location Model/Case study data/08 Chile fictional data centre/demand data/year2.csv", index=False)
