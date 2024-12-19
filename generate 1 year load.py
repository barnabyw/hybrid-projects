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
    89.22, 89.09, 89.24, 89.92, 90.69, 91.52, 92.68, 96.01,
    98.59, 99.15, 99.50, 99.76, 99.96, 100.00, 99.93, 99.63,
    98.75, 97.01, 95.54, 94.13, 92.39, 90.94, 89.48, 89.37
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
yearly_data.to_csv("/Users/barnabywinser/Library/CloudStorage/OneDrive-SharedLibraries-Rheenergise/Commercial - Documents/Cost Models/ESC Co-Location Model/Case study data/08 Chile fictional data centre/demand data/year.csv", index=False)
