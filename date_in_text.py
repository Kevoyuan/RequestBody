from dateutil.parser import parse, ParserError
from datetime import datetime
import re
from dateutil.relativedelta import relativedelta
import datefinder


def date_in_text(text):

    # Parse the date from the text
    # Initialize datetime_obj to None
    datetime_obj = None
    datetime_objs = datefinder.find_dates(text)
    for datetime_obj in datetime_objs:
        print(datetime_obj)

    # If no date was found, return None
    if datetime_obj is None:
        return None
    
    # Get the date part only
    day = datetime_obj.day
    month = datetime_obj.month
    year = datetime_obj.year

    # Extract the date string and add the day
    date_str = f"1 {month} {year}"

    # parse the date with month as a number
    date = datetime.strptime(date_str, '%d %m %Y')

    # Check if the text matches the pattern "end Month Year"
    match_end = re.search(r'end', text, re.IGNORECASE)    
    match_start = re.search(r'start', text, re.IGNORECASE)    

    format_string = '%Y-%m-%d'

    if match_end:
        # Add one month to the date, and then subtract one day to get the last day of the original month
        last_day = date + relativedelta(months=1) - relativedelta(days=1)
        formatted_date = last_day.strftime(format_string)
        
    elif match_start:
        formatted_date = date.strftime(format_string)

    else:
        formatted_date = datetime_obj.strftime(format_string)
        
    return formatted_date

def request_date_if_not_in_text(text):
    # Try to extract a date from the text
    extracted_date = date_in_text(text)
    if extracted_date is None:
        # If no date was found in the text, ask the user for one
        extracted_date = input("Please enter a date (YYYY-MM-DD): ")
    return extracted_date