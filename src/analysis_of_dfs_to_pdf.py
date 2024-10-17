import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from load_data_from_sources_to_dfs import df_wars_and_duration, df_html_demographics
from transformation_functions import remove_plus_and_hebrew_character, dur_block
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# --------------------------------------- Analyze Sources --------------------------------------- #

# Create a PdfPages object to save plots
pdf_filename = r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\pdf\Isreal_Wars_and_Operations_Analysis.pdf"
with PdfPages(pdf_filename) as pdf: 

    # 1) Count wars per results - bar chart + pie chart # #

    # Group df_wars_and_duration df by 'Results'
    df_combined_agg = df_wars_and_duration['Results'].value_counts()

    # Define color mapping using hex codes for each result
    color_mapping = {
        'Victory': '#B4E5A2',  # Green
        'Stalemate': '#CFC6D9',  # Gray
        'Defeat': '#F17456'  # Red
    }

    # Assign colors based on the index (Results) in df_combined_agg
    colors = [color_mapping.get(result, '#0000FF') for result in df_combined_agg.index]  # Default to blue if result is not in mapping

    # Bar graph 
    plt.figure(figsize=(10, 6))  # Increase the figure size to prevent bars from being cut off
    ax = df_combined_agg.plot(kind='bar', color=colors)

    # Annotate each bar with its count
    for i, count in enumerate(df_combined_agg):
        ax.text(i, count, str(count), ha='center', va='bottom')

    ax.set_xticklabels(ax.get_xticklabels(), rotation=75, ha='right')  # Rotate x-axis labels to 75 degrees
    ax.set_xlabel('')  # Remove x-axis label
    plt.title('Wars Per Results (#)', fontweight='bold')
    plt.tight_layout()  # Adjust layout to prevent cutting off labels or bars
    pdf.savefig()  # Save this plot to PDF
    plt.close()

    # Pie chart 
    plt.figure(figsize=(8, 8))  # Adjust pie chart size if needed
    plt.pie(df_combined_agg, labels=df_combined_agg.index, autopct='%1.1f%%', colors=colors)
    plt.legend(df_combined_agg.index, title="Results")
    plt.title('Wars Per Results (%)', fontweight='bold')

    # Save this plot to PDF
    plt.tight_layout()  
    pdf.savefig()  
    plt.close()

    # --------------------------------------

    # 2) Wars through the years # 

    # add a column of start year
    df_wars_and_duration['War Years'] = df_wars_and_duration['War Years'].astype(str)
    df_wars_and_duration['War Start Year'] = df_wars_and_duration['War Years'].apply(lambda item : item.split("-")[0].replace(" ","")).astype(str).apply(lambda item : item.replace(".0","")).astype(int)

    # create new df that holds necessary data only - War Name & War Start Year
    wars = df_wars_and_duration['War Name']
    start_years = df_wars_and_duration['War Start Year']

    # Set a higher y-coordinate for the dots
    y_position = 1.0

    # Create a timeline plot
    plt.figure(figsize=(10, 5))
    plt.scatter(start_years, [y_position] * len(start_years), color='black', s=40)  # Blue dots at a higher position

    # Set y-ticks to an empty list to hide war names on the y-axis
    plt.yticks([])

    # Use only the unique years from start_years for x-ticks
    unique_years = sorted(set(start_years))
    plt.xticks(unique_years, fontsize=7, rotation=75)

    # Dictionary to track war labels for each year and alternate their positions
    war_position_tracker = {}

    # Add labels above and below each point based on the year
    for i, (war, year) in enumerate(zip(wars, start_years)):
        # Initialize war position tracker for the year if not already done
        if year not in war_position_tracker:
            war_position_tracker[year] = 0
        
        # Alternate the position, spacing out the wars if more than one in the same year
        offset = 0.02 * (war_position_tracker[year] + 1)  # Increase offset for each subsequent war
        va_position = 'bottom' if war_position_tracker[year] % 2 == 0 else 'top'  # Alternate top and bottom
        
        # Update the tracker for the year
        war_position_tracker[year] += 1
        
        # Set war name font size to 5 and rotate 75 degrees
        plt.text(year, y_position + (offset if va_position == 'bottom' else -offset), war, 
                ha='center', va=va_position, fontsize=7, rotation=90)

    plt.title('Wars Timeline', fontweight='bold')

    # Adjust the y-axis limits to make more space below the dots
    plt.ylim(0.7, 1.5)

    # Show the plot
    # plt.show()

    # Save this plot to PDF
    plt.tight_layout()  
    pdf.savefig()  
    plt.close()

    # --------------------------------------

    # 3) Wars vs. Demo Growth # 

    # add columns and needed transformations
    df_wars_and_duration['War Years'] = df_wars_and_duration['War Years'].astype(str)
    df_wars_and_duration['War Start Year'] = df_wars_and_duration['War Years'].apply(lambda item : item.split("-")[0].replace(" ","")).astype(str).apply(lambda item : item.replace(".0","")).astype(int)
    df_wars_and_duration = remove_plus_and_hebrew_character(df_wars_and_duration)
    df_wars_and_duration['Civilians Losses'] = df_wars_and_duration['Civilians Losses'].astype(str)
    df_wars_and_duration['Civilians Losses'] = df_wars_and_duration['Civilians Losses'].replace('2-3','3').str.replace('.0','')
    df_wars_and_duration.loc[13, 'IDF Forces Losses'] = df_wars_and_duration.loc[13, 'IDF Forces Losses'].replace('776-983', '983')
    df_wars_and_duration['IDF Forces Losses'] = df_wars_and_duration['IDF Forces Losses'].apply(lambda item : int(item))
    df_wars_and_duration['Civilians Losses'] = df_wars_and_duration['Civilians Losses'].apply(lambda item : int(item))
    df_wars_and_duration['All Losses'] = df_wars_and_duration['IDF Forces Losses'] + df_wars_and_duration['Civilians Losses']

    # create new df that hold necessary data only - War Name & War Start Year
    losses_data  = df_wars_and_duration[['War Start Year','All Losses']]

    # Sort the losses_data by 'War Start Year' in ascending order
    losses_data = losses_data.sort_values(by='War Start Year', ascending=True)

    df_population = pd.DataFrame(df_html_demographics)
    df_losses = pd.DataFrame(losses_data)

    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Population
    ax1.plot(df_population['Year'], df_population['Population (K)'], color='blue', label='Population (K)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Population (K)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis for losses
    ax2 = ax1.twinx()
    ax2.plot(df_losses['War Start Year'], df_losses['All Losses'], color='red', label='All Losses', linestyle='--')
    ax2.set_ylabel('All Losses', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add titles and legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title('Wars Loses vs. Population Growth', fontweight='bold')

    # Show plot
    # plt.show()
    
    # Save this plot to PDF
    plt.tight_layout()  
    pdf.savefig()  
    plt.close()

    # --------------------------------------

    # 4) Wars per duration #

    # Data transformations
    df_wars_and_duration['Duartion blocks'] = df_wars_and_duration['Duration time'].apply(lambda item: dur_block(item))

    # Aggregate data
    df_combined_agg = df_wars_and_duration['Duartion blocks'].value_counts()

    # Define a custom order for sorting
    custom_order = ['less than a month', '1-11 months', '1 year and above']

    # Create a categorical type with the custom order
    df_combined_agg = df_combined_agg.reindex(custom_order).dropna()  # Reindex and drop any NaNs

    # Extract categories and values separately
    categories = df_combined_agg.index.tolist()  
    values = df_combined_agg.values.tolist()     

    colors = []
    for category in categories:
        if category.lower() == 'less than a month':
            colors.append('#FFB3B3')  # Lightest Red 
        elif category.lower() == '1-11 months':
            colors.append('#FF7575')  # Lighter red  
        elif category.lower() == '1 year and above':
            colors.append('#FF0000')  # red 
        else:
            colors.append('#756035')  # Default color if a new category appears
            
    # Create the bar graph
    bars = plt.bar(categories, values, color=colors)
    plt.xlabel('Duration')
    plt.ylabel('Count')
    plt.title('Duration Categories Bar Graph', fontweight='bold', fontsize=8)

    # Add count of wars above each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=8)

    # Show the plot
    # plt.show()

    # Save this plot to PDF
    plt.tight_layout()  
    pdf.savefig()  
    plt.close()
    

    # --------------------------------------

    # 5) Losses by wars # 

    # IDF 

    # Data transformations
    df_wars_and_duration['IDF Forces Losses'] = df_wars_and_duration['IDF Forces Losses'].apply(lambda item: int(item))

    # Group by 'War Name' and sum the 'IDF Forces Losses'
    df_wars_and_duration_agg = df_wars_and_duration.groupby('War Name')['IDF Forces Losses'].sum().sort_values(ascending=False) 
    
    # Plot bar chart with specific color
    plt.figure(figsize=(10, 6))  # Adjust figure size if needed
    ax = df_wars_and_duration_agg.plot(kind='bar', color='#756035')  

    # Add annotations to each bar
    for i, (war_name, value) in enumerate(df_wars_and_duration_agg.items()):
        ax.text(i, value + 10, str(value), ha='center', va='bottom', fontsize=8)

    # Set labels and title
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.title('IDF Forces Losses by War', fontweight='bold', color='black')

    # Rotate x-axis labels for better visibility
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize = 8)

    # plt.show()

    # Save this plot to PDF
    plt.tight_layout()
    pdf.savefig()  
    plt.close()

    # Civilians Losses

    # Data transformations
    df_wars_and_duration.loc[1, 'Civilians Losses'] = df_wars_and_duration.loc[1, 'Civilians Losses'].astype(str).replace('2-3', '3')
    df_wars_and_duration['Civilians Losses'] = df_wars_and_duration['Civilians Losses'].apply(lambda item: int(item))
    df_wars_and_duration_agg = df_wars_and_duration.groupby('War Name')['Civilians Losses'].sum().sort_values(ascending=False)
    
    # Plot bar chart for Civilians Losses
    plt.figure(figsize=(10, 6))  # Adjust figure size if needed
    ax = df_wars_and_duration_agg.plot(kind='bar', color='#5E5E5E')  

    # Add annotations to each bar
    for i, (war_name, value) in enumerate(df_wars_and_duration_agg.items()):
        ax.text(i, value + 10, str(value), ha='center', va='bottom', fontsize=8)

    # Set labels and title with specific formatting
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.title('Civilians Losses by War', fontweight='bold', color='black')

    # Rotate x-axis labels for better visibility
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # plt.show()

    # Save this plot to PDF
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # All Losses

    # Data transformations
    df_wars_and_duration['Civilians Losses'] = df_wars_and_duration['Civilians Losses'].astype(str)
    df_wars_and_duration.loc[1, 'Civilians Losses'] = df_wars_and_duration.loc[1, 'Civilians Losses'].replace('2-3', '3')
    df_wars_and_duration['IDF Forces Losses'] = df_wars_and_duration['IDF Forces Losses'].apply(lambda item: int(item))
    df_wars_and_duration['Civilians Losses'] = df_wars_and_duration['Civilians Losses'].apply(lambda item: int(item))
    df_wars_and_duration['All Losses'] = df_wars_and_duration['IDF Forces Losses'] + df_wars_and_duration['Civilians Losses']

    df_wars_and_duration_agg = df_wars_and_duration.groupby('War Name')['All Losses'].sum().sort_values(ascending=False)
    
    # Plot bar chart for All Losses
    plt.figure(figsize=(10, 6))  # Adjust figure size if needed
    ax = df_wars_and_duration_agg.plot(kind='bar', color='#000000') 

    # Add annotations to each bar
    for i, (war_name, value) in enumerate(df_wars_and_duration_agg.items()):
        ax.text(i, value + 10, str(value), ha='center', va='bottom', fontsize=8)

    # Set labels and title with specific formatting
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.title('All Losses by War', fontweight='bold', color='black')

    # Rotate x-axis labels for better visibility
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # plt.show()

    # Save this plot to PDF
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # --------------------------------------

    # 6) Wars per Prime Minister # 
    
    # Count the number of each result per Prime Minister
    df_wars_and_duration_agg = df_wars_and_duration.groupby('Israeli Prime Minister')['Results'].value_counts().unstack().fillna(0)

    # Aggregate number of wars and number of 'Victory'
    df_wars_and_duration_agg['Total Wars'] = df_wars_and_duration_agg.sum(axis=1)
    df_wars_and_duration_agg['Victory'] = df_wars_and_duration_agg.get('Victory', 0)

    # Calculate percentage of Victory (rounded to integer)
    df_wars_and_duration_agg['Victory %'] = ((df_wars_and_duration_agg['Victory'] / df_wars_and_duration_agg['Total Wars']) * 100).astype(int)

    # Plotting with customized colors
    ax = df_wars_and_duration_agg[['Total Wars', 'Victory']].plot(
        kind='bar', 
        color=['black', '#B4E5A2'],  # Black for Total Wars, Green (#00B050) for Victory
        figsize=(10, 6)  # Optional: Adjust figure size if necessary
    )

    # Add annotations for 'Victory' only, rotated at 75 degrees with font size 8
    for i, (index, row) in enumerate(df_wars_and_duration_agg.iterrows()):
        # Adjust the y-coordinate to make the text closer to the bars
        ax.text(i + 0.2, row['Victory'] + 0.2,  # Adjust y position slightly
                f"Victory: ({int(row['Victory %'])}%)",  # Ensure integer formatting without decimals
                ha='center', va='bottom', color='#00B050', rotation=75, fontsize=8)

    # Set labels
    ax.set_xlabel('Israeli Prime Minister', fontsize=8)
    ax.set_ylabel('', fontsize=8)
    plt.title('Wars and Victories per Prime Minister', fontweight='bold')

    # Rotate x-axis labels to 75 degrees with font size 8
    ax.set_xticklabels(ax.get_xticklabels(), rotation=75, ha='right', fontsize=8)

    # Disable rounding of y-axis and show exact numbers
    ax.yaxis.get_major_locator().set_params(integer=True)

    # plt.show()

    # Define title
    plt.tight_layout() 
    pdf.savefig() 
    plt.close()

