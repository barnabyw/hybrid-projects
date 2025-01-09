#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 11:34:19 2025

@author: barnabywinser
"""

import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

"""Left hand graphs specifications"""

start_date_1 = pd.to_datetime('2023-07-14 00:00:00')
end_date_1 = start_date_1 + pd.Timedelta(days=7)
scenario = "S3.xlsm"

"""Right hand graph specifications"""

scenario_2 = "S4.xlsm"
start_date_2 = pd.to_datetime('2023-07-14 00:00:00')  # Second week
end_date_2 = start_date_2 + pd.Timedelta(days=7)

""""""

# Initialize constants
master_text_size = 36
colors = sns.color_palette("pastel", 10).as_hex()

folder = '/Users/barnabywinser/Documents/Chile data centre/' # where UI scenarios are saved (model runs)
output_f = '/Users/barnabywinser/Documents/Chile data centre/plots/' # where plots will be saved

# the script will plot technologies that are in both the defaults and the relevant scenario
positive_defaults = ['Solar_generation', 'HD_Hydro_discharge', 'Solar_new_generation', 'Wind_generation', 'Grid_imports', "Diesel_imports", "Solar_vertical_generation"]
negative_defaults = ['Export_cable_exports', 'HD_Hydro_charge', 'curtailment']

# Assign colors to categories
color_label_mapping = {
    'Wind_generation': {'color': colors[2], 'label': 'Wind Generation'},
    'HD_Hydro_discharge': {'color': colors[0], 'label': 'HD Hydro Discharge'},
    'Diesel_imports': {'color': colors[3], 'label': 'Diesel'},
    'HD_Hydro_charge': {'color': colors[4], 'label': 'HD Hydro Charge'},
    'Solar_generation': {'color': colors[2], 'label': 'Solar Generation'},
    'Grid_imports': {'color': colors[6], 'label': 'Import from grid'},
    'curtailment': {'color': colors[1], 'label': 'Curtailment'},
    'Solar_vertical_generation': {'color': colors[2], 'label': 'Solar Generation'}
}

# Load data
df1 = pd.read_excel(folder + scenario, sheet_name='Results - Operation')
df1['Datetime'] = pd.to_datetime(df1['Datetime'])

df2 = pd.read_excel(folder + scenario_2, sheet_name='Results - Operation')
df2['Datetime'] = pd.to_datetime(df2['Datetime'])

# Filter data
filtered_df_1 = df1[(df1['Datetime'] >= start_date_1) & (df1['Datetime'] <= end_date_1)]
filtered_df_2 = df2[(df2['Datetime'] >= start_date_2) & (df2['Datetime'] <= end_date_2)]

def add_traces(fig, filtered_df, columns, defaults, row, col, legend_entries):
    # Get the intersection of columns and defaults
    intersected_columns = list(set(columns) & set(defaults))
    
    for col_name in intersected_columns:
        # Get legend label
        legend_label = color_label_mapping.get(col_name, {}).get('label', col_name)
        
        # Determine if the legend should be shown
        show_legend = legend_label not in legend_entries
        
        # Add the trace
        fig.add_trace(
            go.Bar(
                x=filtered_df['Datetime'],
                y=filtered_df[col_name],
                name=legend_label,
                marker_color=color_label_mapping.get(col_name, {}).get('color', '#000000'),
                showlegend=show_legend  # Only show legend if not already added
            ),
            row=row, col=col
        )
        
        # Add the legend label to the set
        legend_entries.add(legend_label)
        
#create subplot layout
fig = make_subplots(
    rows=2, cols=2,
    shared_xaxes=True,
    shared_yaxes=True,
    subplot_titles=[
        "Power flows: on grid, no storage", "Power flows: on grid, with storage",
        "Grid power price", "Grid power price"
    ],
    vertical_spacing=0.1,  # Space between rows (0 to 1)
    horizontal_spacing=0.1,  # Space between columns (0 to 1)
    row_heights=[0.7, 0.3],  # Top row is 70% of height, bottom row is 30%
    column_widths=[0.5, 0.5]  # Both columns have equal width
)

# Customize the subplot titles
for annotation in fig['layout']['annotations']:
    annotation['font'] = dict(
        family="Barlow",  # Font family
        size=master_text_size,  # Font size for titles
        color="black"  # Font color
    )


# Add operation traces for both scenarios
cols1 = list(df1.columns)
cols2 = list(df2.columns)

# Initialize a set to track added legend entries
legend_entries = set()

# Add traces dynamically for each subplot
add_traces(fig, filtered_df_1, cols1, positive_defaults, row=1, col=1, legend_entries=legend_entries)
add_traces(fig, filtered_df_1, cols1, negative_defaults, row=1, col=1, legend_entries=legend_entries)
add_traces(fig, filtered_df_2, cols2, positive_defaults, row=1, col=2, legend_entries=legend_entries)
add_traces(fig, filtered_df_2, cols2, negative_defaults, row=1, col=2, legend_entries=legend_entries)

# Add market price traces for both scenarios
fig.add_trace(
    go.Scatter(
        x=filtered_df_1['Datetime'],
        y=filtered_df_1['Market_Price'],
        mode='lines',
        name='Market Price',
        line=dict(color=colors[6], width=2),
        showlegend=True  # Show legend for the first trace
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=filtered_df_2['Datetime'],
        y=filtered_df_2['Market_Price'],
        mode='lines',
        name='Market Price',
        line=dict(color=colors[6], width=2),
        showlegend=False  # Hide legend for the second trace
    ),
    row=2, col=2
)

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


# Update layout
fig.update_layout(
    font=dict(family="Barlow", color='black', size=master_text_size),
    barmode='relative',
    bargap=0.05,
    height=1400,  # Increase figure height
    margin=dict(l=50, r=50, t=50, b=130),  # Add space below the plot
    yaxis_title=dict(text="MW", font=dict(size=master_text_size - 2)),
    yaxis3_title=dict(text="$/MWh", font=dict(size=master_text_size - 2)),
    width=1800,
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
)

# Update axes
fig.update_xaxes(showgrid=True, gridcolor='rgba(128, 128, 128, 0.3)')
fig.update_yaxes(showgrid=True, gridcolor='rgba(128, 128, 128, 0.3)')

# Show and save the plot
fig.show()
fig.write_image(output_f + start_date_1.strftime("%B") + "quad_plot.png", width=1920, height=1200, scale=3)
