#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 5 16:49:25 2024

@author: barnabywinser
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

"""Graph specifications"""
# Scenario for the single graph
scenario = "S1.xlsm"
# Start date and range for the graph
start_date = pd.to_datetime('2023-07-14 00:00:00')
end_date = start_date + pd.Timedelta(days=7)

folder = '/Users/barnabywinser/Documents/Chile data centre/'  # Where the scenarios are stored
output_f = '/Users/barnabywinser/Documents/Chile data centre/plots/'  # Where the plot is saved

positive_defaults = ['Solar_generation', 'HD_Hydro_discharge', 'Solar_new_generation', 'Wind_generation', 'Grid_imports', "Diesel_imports", "Solar_vertical_generation"] 
negative_defaults = ['Export_cable_exports', 'HD_Hydro_charge', 'curtailment']

# Generate colors
colors = sns.color_palette("pastel", 10).as_hex()

# Assign colors to categories
green = colors[2]    # Renewable generation
red = colors[3]      # Curtailment
blue = colors[0]     # Charging power
pink = colors[6]     # New solar generation
orange = colors[1]   # Export to grid
purple = colors[4]   # Discharge power
light_blue = colors[9]
grey = colors[7]   # Diesel generation

# Manually specify colors and labels for each column within the excel file
color_label_mapping = {
    'Wind_generation': {'color': green, 'label': 'Wind Generation'},
    'HD_Hydro_discharge': {'color': blue, 'label': 'HD Hydro Discharge'},
    'Diesel_imports': {'color': red, 'label': 'Diesel'},
    'HD_Hydro_charge': {'color': purple, 'label': 'HD Hydro Charge'},
    'Solar_generation': {'color': green, 'label': 'Solar Generation'},
    'Grid_imports': {'color': pink, 'label': 'Import from grid'},
    'curtailment': {'color': orange, 'label': 'Curtailment'},
    'Solar_vertical_generation': {'color': green, 'label': 'Solar Generation'},
    'Wind_new_generation': {'color': green, 'label': 'New Wind Generation'}
}

# Load your data
file = folder + scenario
df = pd.read_excel(file, sheet_name='Results - Operation')
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Filter the DataFrame based on the date range
filtered_df = df[(df['Datetime'] >= start_date) & (df['Datetime'] <= end_date)]

# Create the figure
fig = go.Figure()

# Function to add traces dynamically based on column intersection with defaults
def add_traces(fig, filtered_df, columns, defaults):
    # Get the intersection of columns and defaults
    intersected_columns = list(set(columns) & set(defaults))
    
    for col_name in intersected_columns:
        legend_label = color_label_mapping.get(col_name, {}).get('label', col_name)
        fig.add_trace(go.Bar(
            x=filtered_df['Datetime'],
            y=filtered_df[col_name],
            name=legend_label,
            marker_color=color_label_mapping.get(col_name, {}).get('color', '#000000'),
        ))

# Add traces for positive and negative defaults
add_traces(fig, filtered_df, list(df.columns), positive_defaults)
add_traces(fig, filtered_df, list(df.columns), negative_defaults)

# Add the Demand line trace
fig.add_trace(go.Scatter(
    x=filtered_df['Datetime'],
    y=-filtered_df['Demand_Electricity_Load'],
    mode='lines',
    name='Demand',
    line=dict(color='grey', width=2)
))

# Update layout for the figure
fig.update_layout(
    title="Power flows",
    font=dict(family="Barlow", color='black', size=16),
    barmode='relative',
    yaxis_title="MW",
    xaxis_title="Time",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    height=600,
    width=1000,
    bargap=0.05
)

# Save the plot
fig.write_image(output_f + start_date.strftime("%B") + scenario + ".png", width=1200, height=600, scale=2)
