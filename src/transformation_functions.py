from datetime import datetime

# Get rid of problematic characters in strings
def get_rid_of_problematic_charachters_within_string(df_name_or_df_name_and_columns):
    df = df_name_or_df_name_and_columns.replace({
        r'\[\d{1,3}\]': '',  # Remove references like [1], [23], etc.
        '–': '-',  # Replace en-dash with hyphen
        r'[\u05B2\u00A0]': ''  # Remove Unicode characters: \u05B2 and \u00A0
    }, regex=True) 
    return df   

# Convert string to list
def string_to_list(item):
    splited_item = item.split()
    return splited_item

# Remove bracket and spaces
def remove_brackets_and_spaces(df_name_or_df_name_and_columns):
    df = df_name_or_df_name_and_columns.replace({
    r'[\[\]()]': '',  # Remove square and round brackets
    r'\s+': ' '  # Replace multiple spaces with a single space
    }, regex=True) 
    return df   

# Calaculate war duration time
def calc_duration_time(duration_dates):
    # Check if duration_dates is a string
    if not isinstance(duration_dates, str):
        return "Invalid duration"  # or return None or another default value

    # Split the string into two parts: start date and end date
    if "Ongoing" in duration_dates:
        start_date_str = duration_dates.split(" - ")[0]
        start_date = datetime.strptime(start_date_str, "%B %d, %Y")
        end_date = datetime.now()  # today
    else:
        start_date_str, end_date_str = duration_dates.split(" - ")
        start_date = datetime.strptime(start_date_str, "%B %d, %Y")
        end_date = datetime.strptime(end_date_str, "%B %d, %Y")

    # Calculate the duration in days
    duration_days = (end_date - start_date).days

    # Determine the appropriate format (days, months, years)
    if duration_days < 30:
        # Less than a month, display in days
        return f"Duration: {duration_days} days"
    elif duration_days < 365:
        # Less than a year, display in months
        months = duration_days // 30  # Approximate month calculation
        return f"Duration: {months} months"
    else:
        # More than a year, display in years, months, and days
        years = duration_days // 365
        remaining_days = duration_days % 365
        months = remaining_days // 30
        days = remaining_days % 30
        return f"Duration: {years} years"  # You can customize this output         

# Remove plus signs, Hebrew character \u05B2, and non-breaking space \u00A0 
def remove_plus_and_hebrew_character(df_name_or_df_name_and_columns):
    df = df_name_or_df_name_and_columns.replace({
        r'[+,\u05B2\u00A0]': '' ,
        r'[+,\u05B2\u00A0~]':''
    }, regex=True)
    return df

# Calculate war duration
def dur_block(item):
    if '1 months' in item or 'days' in item:
        return 'less than a month'
    elif 'months' in item:
        return '1-11 months'
    else:
        return '1 year and above'