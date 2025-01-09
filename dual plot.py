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


"""Left hand graphs specifications"""

#scenario for left hand graph
scenario = "S3.xlsm"
# start date and range for left hand graph
start_date_1 = pd.to_datetime('2023-07-14 00:00:00')
end_date_1 = start_date_1 + pd.Timedelta(days=7)


"""Right hand graph specifications"""

#scenario for right hand graph
scenario_2 = "S4.xlsm"
# start date and range for right hand graph
start_date_2 = pd.to_datetime('2023-07-14 00:00:00')
end_date_2 = start_date_2 + pd.Timedelta(days=7)

""""""

UI = "n" # If 'y', then the file path containing the UI is used

folder = '/Users/barnabywinser/Documents/Chile data centre/' #where the scenarios are stored (this is a renamed UI.xlsm file)
output_f = '/Users/barnabywinser/Documents/Chile data centre/plots/' #where the plot is saved

scenario = "A1.xlsm" # name of excel file for left graph
scenario_2 = "A2.xlsm" # name of excel file for right graph

positive_defaults = ['Solar_generation', 'HD_Hydro_discharge', 'Solar_new_generation', 'Wind_generation', 'Grid_imports', "Diesel_imports", "Solar_vertical_generation"] 
negative_defaults = ['Export_cable_exports', 'HD_Hydro_charge', 'curtailment']

#generate colors
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
    

if UI == 'y':
    file = '/Users/barnabywinser/Documents/Co-location-directory/co-location-model-Final/co-location-model-Final/UI.xlsm'

else:
    file = folder + scenario
    file_2 = folder + scenario_2

# Load your data
df = pd.read_excel(file, sheet_name='Results - Operation')
df['Datetime'] = pd.to_datetime(df['Datetime'])

df2 = pd.read_excel(file_2, sheet_name='Results - Operation')
df2['Datetime'] = pd.to_datetime(df2['Datetime'])

# Scan for which columns are present
cols = list(df.columns)
cols2 = list(df2.columns)

# Create subplots with 1 row and 2 columns
fig = make_subplots(
    rows=1, cols=2,
    shared_yaxes=True,  # Share y-axis between the two plots
    column_widths=[0.5, 0.5],  # Equal widths for both columns
    subplot_titles=[
        "Off grid, no storage",
        "Off grid + storage"
    ]
)

# Track already added legend entries - this ensures they only appear once on the legend
legend_entries = set()

# Filter the DataFrame based on the two date ranges
filtered_df_1 = df[(df['Datetime'] >= start_date_1) & (df['Datetime'] <= end_date_1)]
filtered_df_2 = df2[(df2['Datetime'] >= start_date_2) & (df2['Datetime'] <= end_date_2)]

# Function to add traces (bars) dynamically based on column intersection with defaults
def add_traces(fig, filtered_df, columns, defaults, row, col, legend_entries):
    # Get the intersection of columns and defaults
    intersected_columns = list(set(columns) & set(defaults))
    
    for col_name in intersected_columns:
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

# Add traces dynamically for each subplot, positive and negative separately
add_traces(fig, filtered_df_1, cols, positive_defaults, 1, 1, legend_entries)
add_traces(fig, filtered_df_1, cols, negative_defaults, 1, 1, legend_entries)
add_traces(fig, filtered_df_2, cols2, positive_defaults, 1, 2, legend_entries)
add_traces(fig, filtered_df_2, cols2, negative_defaults, 1, 2, legend_entries)
    
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
master_text_size = 36

def create_axis_settings(gridcolor='rgba(128, 128, 128, 0.3)', font_size=36):
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
            x=0.22,  # Centered above the first subplot (adjust as needed)
            y=1,  # Position above the plot
            xref="paper",  # Use figure-relative coordinates
            yref="paper",  # Use figure-relative coordinates
            text="Off grid, no storage",  # Title for the first plot
            showarrow=False,  # Hide the arrow
            font=dict(size=master_text_size - 2)  # Adjust font size
        ),
        # Title for the second subplot
        dict(
            x=0.78,  # Centered above the second subplot (adjust as needed)
            y=1,  # Position above the plot
            xref="paper",  # Use figure-relative coordinates
            yref="paper",  # Use figure-relative coordinates
            text="Off grid + storage",  # Title for the second plot
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

# save the plot
fig.write_image(output_f + start_date_1.strftime("%B") +  scenario + ".png", width=1920, height=800, scale=3)
