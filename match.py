from itertools import permutations
from dateutil.parser import parse
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re


def match_model_in_text(text, dictionary):

    matched_models = []

    # First check for exact matches
    for model in dictionary.keys():
        if model.lower() in text.lower():
            matched_models.append(dictionary[model])

    # If no exact match was found, check for partial matches
    if not matched_models:
        for model in dictionary.keys():
            # Split the model name into words
            model_words = model.split()
            # Check if any of these words are in the text
            if any(word.lower() in text.lower() for word in model_words):
                matched_models.append(dictionary[model])
                
    return matched_models   


def match_confs_in_text(text, dictionary):
    # Convert text to lowercase
    text = text.lower()

    # Sort keys from longest to shortest
    sorted_keys = sorted(dictionary.keys(), key=len, reverse=True)

    # Create a dictionary to hold matches
    matches = {}
    matched_confs = []

    # Check if any key is in the text
    for key in sorted_keys:
        lower_key = key.lower()
        
        lower_keys = lower_key.split()
        # Generate all permutations of the words
        lower_key_permutations = [' '.join(perm) for perm in permutations(lower_keys)]
        
        # Check if any of these permutations are in the text
        if any(perm.lower() in text for perm in lower_key_permutations):
        
            # matches[key] = dictionary[key]
            text = text.replace(lower_key, '')
            matched_confs.append(dictionary[key])
    # return matches.values()
    return matched_confs


def date_in_text(text):
    # Clean the text
    # Trim leading and trailing whitespaces
    date_text = text.strip()

    # Remove multiple whitespaces
    date_text  = re.sub(r'\s+', ' ', date_text )

    # Remove symbols 
    date_text = re.sub(r'\W+', ' ', date_text)

    # Parse the date from the text
    datetime_obj = parse(date_text , fuzzy=True, dayfirst=True)


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

