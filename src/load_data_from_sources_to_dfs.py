import pandas as pd
from transformation_functions import get_rid_of_problematic_charachters_within_string, string_to_list, remove_brackets_and_spaces, calc_duration_time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# --------------------------------------- Source #1 : Israel wars --> dataFrame - df_html_wars --------------------------------------- #

# Read from source and load to a data frame
df_html_wars_orig = pd.read_html('https://en.wikipedia.org/wiki/List_of_wars_involving_Israel')

# Extract relevant table and fields from source
df_html_wars = df_html_wars_orig[1].iloc[:, :9]

# Rename table columns
df_html_wars.columns = ['War Name','Combatant #1', 'Combatant #2', 'Results', 'Israeli Prime Minister',
                        'Defense Minister of Israel', 'Chief of Staff of the IDF', 'IDF Forces Losses', 'Civilians Losses']

# Get rid of problematic characters in strings
df_html_wars = get_rid_of_problematic_charachters_within_string(df_html_wars)

# Replace text in 'Results' column for specific result - Victory, Defeat, Stalemate  
def is_victory(item):
    victory_lower = ['victory','both sides claimed victory','tactical victories','accord']
    for value in victory_lower:
        if value in item.lower():
            return True   
        
df_html_wars['Results'] = df_html_wars['Results'].apply(lambda item : 'Victory' if is_victory(item) else ('Defeat' if 'defeat' in item.lower() else 'Stalemate'))

# Convert string values in 'Combatant #1' and 'Combatant #2' columns to lists
df_html_wars['Combatant #1'] = df_html_wars['Combatant #1'].apply(lambda item : string_to_list(item))
df_html_wars['Combatant #2'] = df_html_wars['Combatant #2'].apply(lambda item : string_to_list(item))

# Replace empty or NULL values with 0 in 'Civilians Losses' column
df_html_wars['Civilians Losses'] = df_html_wars['Civilians Losses'].fillna('0').replace('None', '0') 

# Split war name from war years
df_html_wars[['War Name','War Years']] = df_html_wars['War Name'].str.split('(', expand=True)

# Remove bracket and spaces from 'War Years' column
df_html_wars[['War Name','War Years']] = remove_brackets_and_spaces(df_html_wars[['War Name','War Years']]).applymap(lambda item: item.replace(')', '').rstrip())

# Remove the row where 'War Name' is 'Operation Northern Arrows'
df_html_wars = df_html_wars[df_html_wars['War Name'] != 'Operation Northern Arrows']

# Save to CSV
# df_html_wars.to_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\csv_for_testing\Israel_Wars.csv", encoding='utf-8', index=False)

# --------------------------------------- Source #2 : Israel Wars duration --> dataFrame - df_csv_wars_duration --------------------------------------- #

# Read from source and load to a data frame
df_csv_wars_duration = pd.read_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\sources\csv\Israel_Wars_Duration.csv",encoding='cp1252')

# Get rid of problematic characters in strings
df_csv_wars_duration = get_rid_of_problematic_charachters_within_string(df_csv_wars_duration)

# Save to CSV
# df_csv_wars_duration.to_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\csv_for_testing\Israel_Wars_duration.csv", encoding='utf-8', index=False)

# --------------------------------------- Join Source #1 + Source #2 : Israel wars and Duration --> dataFrame - df_wars_and_duration --------------------------------------- #

# Join sources
df_joined = pd.merge(df_html_wars,df_csv_wars_duration,left_on='War Name',right_on='War Name', how='outer')

# Save to CSV
# df_joined.to_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\csv_for_testing\wars_and_duration_joined.csv", encoding='utf-8', index=False)

# Define columns appearing twice - (without 'War Name' , 'Duration Dates' which appear once)
columns_to_combine = ['Combatant #1', 'Combatant #2', 'Results', 'Israeli Prime Minister',
                    'Defense Minister of Israel', 'Chief of Staff of the IDF', 'IDF Forces Losses', 'Civilians Losses','War Years']

# Make a copy of joined data frame
df_wars_and_duration = df_joined.copy()

# Add new columns to the copy which are the combination of _x and -y
for col in columns_to_combine:
    df_wars_and_duration[col] = df_joined[f"{col}_x"].combine_first(df_joined[f"{col}_y"])

# Drop the _x and _y columns
df_wars_and_duration = df_wars_and_duration.drop(columns=[f"{col}_x" for col in columns_to_combine] +[f"{col}_y" for col in columns_to_combine])

# Calaculate war duration time
df_wars_and_duration['Duration time'] = df_wars_and_duration['Duration Dates'].apply(lambda item : calc_duration_time(item))

# Save to CSV
# df_wars_and_duration.to_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\csv_for_testing\wars_and_duration_merged.csv", encoding='utf-8', index=False)

# --------------------------------------- Source #3 : Israel Demographics --> df_html_demographics --------------------------------------- #

# Read from source and load to a data frame
df_html_demographics_orig = pd.read_html('https://he.wikipedia.org/wiki/%D7%93%D7%9E%D7%95%D7%92%D7%A8%D7%A4%D7%99%D7%94_%D7%A9%D7%9C_%D7%99%D7%A9%D7%A8%D7%90%D7%9C')

# Extract relevant table from source
df_html_demographics = df_html_demographics_orig[4]

# Keep needed columns only : Year, Population
df_html_demographics = df_html_demographics[['שנה', 'אוכלוסייה (אלפים)']]

# Rename column names
df_html_demographics = df_html_demographics.rename(columns={'שנה':'Year', 'אוכלוסייה (אלפים)':'Population (K)'})

# Duplicate row 0 and modify the Year
row_to_insert = df_html_demographics.iloc[0].copy()
row_to_insert['Year'] = 1947

# Insert the modified row at the beginning of the DataFrame
df_html_demographics = pd.concat([pd.DataFrame([row_to_insert]), df_html_demographics], ignore_index=True)

# Save to CSV
# df_html_demographics.to_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\csv_for_testing\Israel_Demographics.csv", encoding='utf-8', index=False)

# --------------------------------------- #
print('Step finished successfully!')
