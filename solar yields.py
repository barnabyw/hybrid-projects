import pandas as pd

folder = "/Users/barnabywinser/Library/CloudStorage/OneDrive-SharedLibraries-Rheenergise/Commercial - Documents/Opportunities/Enlasa/Co-location/inputs/solar data/"
inputfiles = ["vertical_clean.xlsx", "dual_clean.xlsx", "inclined_clean.xlsx", "fixed_clean.xlsx"]

output = 'solar_summary.csv'

results = []

for inputfile in inputfiles:
    af = pd.read_excel(folder + inputfile)
    
    # Ensure datetime column is in datetime format
    af['datetime'] = pd.to_datetime(af['time'])  # Replace 'time' with the actual datetime column name if different
    
    # Define the season based on the month
    af['season'] = af['datetime'].dt.month % 12 // 3 + 1
    af['season'] = af['season'].map({1: 'Summer', 2: 'Autumn', 3: 'Winter', 4: 'Spring'})
    
    # Calculate kWh for each season
    seasonal_kwh = af.groupby('season')['AF'].sum()
    
    # Prepare dictionary to store in results list
    track = inputfile.split("_")[0]
    result_entry = {
        'Track': track,
        'Total_kWh': round(seasonal_kwh.sum(),1),
        'Summer': round(seasonal_kwh.get('Summer', 0),1),
        'Autumn': round(seasonal_kwh.get('Autumn', 0),1),
        'Winter': round(seasonal_kwh.get('Winter', 0),1),
        'Spring': round(seasonal_kwh.get('Spring', 0),1)
    }
    
    results.append(result_entry)

# Convert results to a DataFrame
results_df = pd.DataFrame(results)


# Melt the results DataFrame to convert to long format
long_results_df = pd.melt(
    results_df,
    id_vars=['Track', 'Total_kWh'],  # Columns to keep
    value_vars=['Summer', 'Autumn', 'Winter', 'Spring'],  # Columns to unpivot
    var_name='Season',  # Name of the new column for the season
    value_name='kWh'  # Name of the new column for the values
)

# Display the long-format DataFrame
print(long_results_df)

output_f = "/Users/barnabywinser/Library/CloudStorage/OneDrive-SharedLibraries-Rheenergise/Commercial - Documents/Opportunities/Enlasa/Co-location/results/"

long_results_df.to_csv(output_f+"solar yields.csv")

# Display the DataFrame
print(results_df)

results_df.to_csv(folder+output, index = False)
