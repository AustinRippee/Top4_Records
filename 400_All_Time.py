#////////////////////////////////////////////////////////////////////
#
#
#
#       Best Grand Blanc 400 Meter Teams by Top 4 Average
#               Written by Austin Rippee
#                    Sep 28, 2023
#
# The main function of this program is to find what were the best
# 1600 meter teams from Grand Blanc were based on a top 4 average to 
# show speed and depth.
#
#////////////////////////////////////////////////////////////////////

import pandas as pd
import math
import matplotlib.pyplot as plt

# Function to convert "m:ss" format to seconds as a float
def time_str_to_seconds(time_str):
    try:
        if ':' in time_str:
            minutes, seconds = time_str.split(':')
            total_seconds = int(minutes) * 60 + float(seconds)
            return total_seconds
        else:
            return float(time_str)  # Handle cases where time format is not valid
    except ValueError:
        return 0  # Handle invalid time format gracefully
    
def seconds_to_time_str(total_seconds):
    if math.isnan(total_seconds):
        return None
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds % 1) * 100)
    return f"{seconds:02d}.{milliseconds:01d}"

try:
    df = pd.read_csv('400_All_Time.csv')
except FileNotFoundError:
    print("The file does not exist.")
except pd.errors.EmptyDataError:
    print("The file is empty.")
except pd.errors.ParserError as e:
    print(f"An error occurred while parsing the CSV: {e}")
else:
    print("CSV file read successfully.")

# apply the time_str_to_seconds function which converts
# the string into seconds which then can not be numerical.
df['Converted'] = df['Time'].apply(time_str_to_seconds)


# I then sorted the values in which I then wrote 
# another method to only take the top 4 of each year.
df1 = df.sort_values(by=['Converted'], ascending=[True])
def top_n(group):
    return group.head(4)
result = df1.groupby('Year', group_keys=False, sort=False).apply(top_n)

# I then took the average of each year then reset the index back. 
result = result.groupby('Year')['Converted'].mean().reset_index()

# I resorted the values again after the changes to find the
# fastest year's average
result = result.sort_values(by=['Converted'], ascending=[True])

# I ran another method to create a column that displays
# the conversion's time in M:SS.X format and reset the index
# so that it displays in 1-X order.
result['conv'] = result['Converted'].apply(seconds_to_time_str)
result = result.reset_index(drop=True)
result.index += 1

# Printed result
print(df)

#===============================================================================

# Convert 'Year' column to integers
result['Year'] = result['Year'].astype(int)

# Sort the DataFrame by 'Year' column in ascending order
result = result.sort_values(by=['Year'])

# # Get the maximum value from the 'Converted' column
min_value = result['Converted'].min() + 23
max_value = result['Converted'].max() - 60

# # Calculate the y-ticks
y_ticks = list(range(0, int(min_value), 2))

# # Calculate the x-ticks
x_ticks = list(result['Year'])
#x_ticks = (list(range(0, int(max_value), 1)))

# #x_ticks = list(result['Year'].unique())
# # unique_years = result['Year'].unique()
# # x_ticks = list(result['Year'].unique()[::5])

# # Sort the DataFrame in descending order based on 'Converted' column
result = result.sort_values(by=['Converted'], ascending=[False])

# # Creates a bar graph to visualize the average times for each year
plt.figure(figsize=(24, 10))
plt.bar(result['Year'], result['conv'], color='red')
plt.xlabel('Year')
plt.ylabel('Average Time (seconds)')
plt.title('Average 800 Meter Times for Each Year (Top 4)')

# # Customize y-axis ticks to display values every 5 ticks
plt.yticks(y_ticks)

# # # Customize y-axis ticks to display values every 5 ticks
plt.xticks(x_ticks, rotation=45, fontsize=7.8)

plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# # Show the graph
#plt.tight_layout()
#plt.show()
plt.savefig('best4.png')