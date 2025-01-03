#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:06:31 2024

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio
import kaleido
import plotly.graph_objects as go
from plotly.subplots import make_subplots


UI = "y"

colors = sns.color_palette("pastel", 10).as_hex()

start_date = pd.to_datetime('2023-08-14 00:00:00')
end_date = start_date + pd.Timedelta(days=7)

baseline = ''

range = [-35,55]

if baseline == 'y':
    positive_defaults = ['Solar_generation', 'HD_Hydro_discharge', 'Solar_new_generation', 'Wind_generation', 'Grid_imports', "Diesel_imports", "Solar_vertical_generation"] #'Discharging Power (kW)'
    negative_defaults = ['Grid_exports', 'HD_Hydro_charge', 'curtailment'] #'Charging Power (kW)',
    title = "Site operation for a week in " + start_date.strftime("%B") + " (without storage)"
    scenario = 'Result'
else:
    positive_defaults = ['Solar_generation', 'HD_Hydro_discharge', 'Solar_new_generation', 'Wind_generation', 'Grid_imports', "Diesel_imports", "Solar_vertical_generation"] #'Discharging Power (kW)'
    negative_defaults = ['Grid_exports', 'HD_Hydro_charge', 'curtailment'] #'Charging Power (kW)',
    title = "Site operation for a week in " + start_date.strftime("%B") + " (with storage)"
    scenario = 'S1.xlsm'

# Assign colors to categories
green = colors[2]    # Renewable generation
red = colors[3]      # Curtailment
blue = colors[0]     # Charging power
pink = colors[6]     # New solar generation
orange = colors[1]   # Export to grid
purple = colors[4]   # Discharge power
light_blue = colors[9]
grey = colors[7]   # Diesel generation

# Manually specify colors and labels for each column
color_label_mapping = {
    'Wind_generation': {'color': green, 'label': 'Wind Generation'},
    'HD_Hydro_discharge': {'color': purple, 'label': 'HD Hydro Discharge'},
    'curtailment': {'color': red, 'label': 'Curtailment'},
    'HD_Hydro_charge': {'color': blue, 'label': 'HD Hydro Charge'},
    'Solar_generation': {'color': green, 'label': 'Solar Generation'},
    'Grid_imports': {'color': orange, 'label': 'Import from grid'},
    'Grid_exports': {'color': pink, 'label': 'Export to grid'},
    'Solar_vertical_generation': {'color': green, 'label': 'Solar Generation'},
    'Wind_new_generation': {'color': green, 'label': 'New Wind Generation'}
}

folder = '/Users/barnabywinser/Library/CloudStorage/OneDrive-SharedLibraries-Rheenergise/Commercial - Documents/Opportunities/Enlasa/Co-location/results/'
    

if UI == 'y':
    file = '/Users/barnabywinser/Documents/Co-location-directory/co-location-model-Final/co-location-model-Final/UI.xlsm'

else:
    
    file = folder + scenario

# Load your data (replace with your actual file path)
df = pd.read_excel(file, 
                   sheet_name='Results - Operation')
# Convert 'Datetime' column to datetime
df['Datetime'] = pd.to_datetime(df['Datetime'])

#scan for which columns are present
cols = list(df.columns)

# Define a master variable for text size
master_text_size = 36

#constrain the plot to these cols
positive_columns = list(set(cols) & set(positive_defaults))
negative_columns = list(set(cols) & set(negative_defaults))

# Filter the DataFrame based on the start and end dates
filtered_df = df[(df['Datetime'] >= start_date) & (df['Datetime'] <= end_date)]

# Create a subplot figure with 2 rows
fig_combined = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,  # Share the x-axis between the two plots
    vertical_spacing=0.1,  # Adjust spacing between plots
    row_heights=[0.7, 0.3]  # Set relative heights of the plots
)

# Add positive values to the plot with manually specified colors and labels
for col in positive_columns:
    fig_combined.add_trace(
        go.Bar(
            x=filtered_df['Datetime'], 
            y=filtered_df[col], 
            name=color_label_mapping.get(col, {}).get('label', col),  
            marker_color=color_label_mapping.get(col, {}).get('color', '#000000')
        ),
        row=1, col=1
    )

# Add negative values to the plot
for col in negative_columns:
    fig_combined.add_trace(
        go.Bar(
            x=filtered_df['Datetime'], 
            y=filtered_df[col], 
            name=color_label_mapping.get(col, {}).get('label', col),  
            marker_color=color_label_mapping.get(col, {}).get('color', '#000000')
        ),
        row=1, col=1
    )

# Add the `Demand_Electricity_Load` column as a line trace
fig_combined.add_trace(
    go.Scatter(
        x=filtered_df['Datetime'],
        y=-filtered_df['Demand_Electricity_Load'],
        mode='lines',
        name='Demand',
        line=dict(color='grey', width=2)
    ),
    row=1, col=1
)

# Add the Market_Price line to the second subplot
fig_combined.add_trace(
    go.Scatter(
        x=filtered_df['Datetime'],
        y=filtered_df['Market_Price'],
        mode='lines',
        name='Grid price',
        line=dict(color=pink, width=2)
    ),
    row=2, col=1
)

# Update layout
fig_combined.update_layout(
    font=dict(
        family="Barlow",
        color='black',
        size=master_text_size
    ),
    barmode='relative',
    bargap = 0.05,
    yaxis=dict(  # Y-axis for the first plot
        title=dict(
            text="MW",  # Specify the title text
            font=dict(
                size=master_text_size,  # Set the font size
                color='black'  # Optional: Set the font color
            )
        ),
        tickformat=".0f",
        showgrid=True,
        gridcolor='rgba(128, 128, 128, 0.3)',
        tickfont=dict(color='black', size=master_text_size - 1),
        #range=range,
    ),
    xaxis=dict(
    showgrid=True,  # Enable horizontal grid lines
    gridcolor='rgba(128, 128, 128, 0.3)',  # Style grid lines
    tickfont=dict(color='black', size=master_text_size - 1),
    zeroline=True,  # Enable the y-axis line
zerolinecolor='rgba(128, 128, 128, 0.3)',  # Set the color of the y-axis line
zerolinewidth=1  # Set the width of the y-axis lin
),
    yaxis2=dict(  # Y-axis for the second plot
        title=dict(
            text="Grid price ($/MWh)",  # Specify the title text
            font=dict(
                size=master_text_size,  # Set the font size
                color='black'  # Optional: Set the font color
            )
        ),
        showgrid=True,  # Enable horizontal grid lines
        gridcolor='rgba(128, 128, 128, 0.3)',  # Style grid lines
        tickfont=dict(color='black', size=master_text_size - 1),
        zeroline=True,  # Enable the y-axis line
    zerolinecolor='rgba(128, 128, 128, 0.3)',  # Set the color of the y-axis line
    zerolinewidth=1  # Set the width of the y-axis li
    ),
    xaxis2=dict(
        showgrid=True,  # Enable horizontal grid lines
        gridcolor='rgba(128, 128, 128, 0.3)',  # Style grid lines
        tickfont=dict(color='black', size=master_text_size - 1),
        zeroline=True,  # Enable the y-axis line
    zerolinecolor='rgba(128, 128, 128, 0.3)',  # Set the color of the y-axis line
    zerolinewidth=1  # Set the width of the y-axis lin
    ),
    showlegend=False,
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(size=master_text_size)),
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    height=800
)

# Show the combined plot
fig_combined.show()

# Save the combined plot as an image
fig_combined.write_image("/Users/barnabywinser/Documents/" + start_date.strftime("%B") + scenario + "_combined.png", width=1200, height=1200, scale=4)
