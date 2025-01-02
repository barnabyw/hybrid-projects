#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 16:49:25 2024

@author: barnabywinser
"""""
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

# Define two different date ranges
start_date_1 = pd.to_datetime('2023-01-21 00:00:00')
end_date_1 = start_date_1 + pd.Timedelta(days=7)

start_date_2 = pd.to_datetime('2023-07-14 00:00:00')
end_date_2 = start_date_2 + pd.Timedelta(days=7)


folder = '/Users/barnabywinser/Documents/Chile data centre/'
output_f = '/Users/barnabywinser/Documents/Chile data centre/plots/'

scenario = "S1.xlsm"
scenario_2 = "S2.xlsm"

plotname = 'S3'
range = [-29,49]


positive_defaults = ['Solar_generation', 'HD_Hydro_discharge', 'Solar_new_generation', 'Wind_generation', 'Grid_imports', "Diesel_imports", "Solar_vertical_generation"] #'Discharging Power (kW)'
negative_defaults = ['Export_cable_exports', 'HD_Hydro_charge', 'curtailment'] #'Charging Power (kW)',
title = "Site operation for a week in " + start_date_1.strftime("%B") + " (with storage)"

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
    'Diesel_imports': {'color': red, 'label': 'Diesel'},
    'HD_Hydro_charge': {'color': blue, 'label': 'HD Hydro Charge'},
    'Solar_generation': {'color': green, 'label': 'Solar Generation'},
    'Grid_imports': {'color': pink, 'label': 'Import from grid'},
    'curtailment': {'color': orange, 'label': 'Curtailment'},
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

#constrain the plot to these cols
positive_columns = list(set(cols) & set(positive_defaults))
negative_columns = list(set(cols) & set(negative_defaults))

# Track already added legend entries
legend_entries = set()

# Filter the DataFrame based on the two date ranges
filtered_df_1 = df[(df['Datetime'] >= start_date_1) & (df['Datetime'] <= end_date_1)]
filtered_df_2 = df[(df['Datetime'] >= start_date_2) & (df['Datetime'] <= end_date_2)]

# Create subplots with 1 row and 2 columns
fig = make_subplots(
    rows=1, cols=2,
    shared_yaxes=True,  # Share y-axis between the two plots
    column_widths=[0.5, 0.5],  # Equal widths for both columns
    subplot_titles=[
        f"Week Starting {start_date_1.strftime('%B %d, %Y')}",
        f"Week Starting {start_date_2.strftime('%B %d, %Y')}"
    ]
)

def add_traces(fig, filtered_df, columns, row, col, legend_entries):
    
    for col_name in columns:
        legend_label = color_label_mapping.get(col_name, {}).get('label', col_name)
        show_legend = legend_label not in legend_entries
        fig.add_trace(go.Bar(
            x=filtered_df['Datetime'],
            y=filtered_df[col_name],
            name=legend_label,
            marker_color=color_label_mapping.get(col_name, {}).get('color', '#000000'),
            showlegend=show_legend
            ), row=row, col=col)
        legend_entries.add(legend_label)

add_traces(fig, filtered_df_1, positive_columns, 1, 1, legend_entries)
add_traces(fig, filtered_df_1, negative_columns, 1, 1, legend_entries)
add_traces(fig, filtered_df_2, positive_columns, 1, 2, legend_entries)
add_traces(fig, filtered_df_2, negative_columns, 1, 2, legend_entries)
    
# Add the Demand line trace for the first date range
fig.add_trace(go.Scatter(
    x=filtered_df_1['Datetime'],
    y=-filtered_df_1['Demand_Electricity_Load'],
    mode='lines',
    name='Demand',
    line=dict(color='grey', width=2)
), row=1, col=1)

    
# Add the Demand line trace for the first date range
fig.add_trace(go.Scatter(
    x=filtered_df_2['Datetime'],
    y=-filtered_df_2['Demand_Electricity_Load'],
    mode='lines',
    name='Demand',
    line=dict(color='grey', width=2),
    showlegend=False
), row=1, col=2)


# Define a master variable for text size
master_text_size = 24

def create_axis_settings(gridcolor='rgba(128, 128, 128, 0.3)', font_size=24):
    """Create settings for axes to reduce repetition."""
    return dict(
        showgrid=True,
        gridcolor=gridcolor,
        tickfont=dict(color='black', size=font_size),
        zeroline=True,
        zerolinecolor=gridcolor,
        zerolinewidth=1
    )

# Update layout for the figure
fig.update_layout(
    font=dict(family="Barlow", color='black', size=master_text_size),
    barmode='relative',
    annotations=[
        # Title for the first subplot
        dict(
            x=0.25,  # Centered above the first subplot (adjust as needed)
            y=1,  # Position above the plot
            xref="paper",  # Use figure-relative coordinates
            yref="paper",  # Use figure-relative coordinates
            text=f"Week Starting {start_date_1.strftime('%B %d, %Y')}",  # Title for the first plot
            showarrow=False,  # Hide the arrow
            font=dict(size=master_text_size - 2)  # Adjust font size
        ),
        # Title for the second subplot
        dict(
            x=0.75,  # Centered above the second subplot (adjust as needed)
            y=1,  # Position above the plot
            xref="paper",  # Use figure-relative coordinates
            yref="paper",  # Use figure-relative coordinates
            text=f"Week Starting {start_date_2.strftime('%B %d, %Y')}",  # Title for the second plot
            showarrow=False,  # Hide the arrow
            font=dict(size=master_text_size - 2)  # Adjust font size
        )
    ],
    yaxis_title=dict(text="MW", font=dict(size=master_text_size - 2)),
    yaxis=create_axis_settings(),
    yaxis2=dict(
        **create_axis_settings(),
        matches='y'  # Ensure yaxis2 matches yaxis
    ),
    xaxis=create_axis_settings(font_size=master_text_size - 2),
    xaxis2=create_axis_settings(font_size=master_text_size - 2),
    legend=dict(
        orientation="h",  # Horizontal legend
        yanchor="bottom",  # Align legend at the bottom
        y=-0.3,  # Position legend below the plot
        xanchor="center",  # Center the legend horizontally
        x=0.5,  # Place legend at the horizontal center
        font=dict(size=master_text_size - 1),  # Adjust legend text size
        traceorder="normal"  # Optional: control trace order in legend
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
    height=600,  # Figure height
    width=1500,  # Figure width
    bargap=0.05  # Set bar gap
)

# Show the plot
fig.show()
fig.write_image(output_f + start_date_1.strftime("%B") +  scenario + "23.png", width=1500, height=600, scale=4)
