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


# def match_confs_in_text(text, dictionary):
#     # Convert text to lowercase
#     text = text.lower()

#     # Sort keys from longest to shortest
#     sorted_keys = sorted(dictionary.keys(), key=len, reverse=True)

#     # Create a dictionary to hold matches
#     matches = {}
#     matched_confs = []
    
#     # Check if any key is in the text
#     for key in sorted_keys:
#         lower_key = key.lower()
        
#         lower_keys = lower_key.split()
#         # Generate all permutations of the words
#         lower_key_permutations = [' '.join(perm) for perm in permutations(lower_keys)]
        

#         # Check if any of these permutations are in the text
#         if any(perm.lower() in text for perm in lower_key_permutations):
        
#             # matches[key] = dictionary[key]
#             text = text.replace(lower_key, '')    

#             matched_confs.append(dictionary[key])
            
#             # match_or = re.search(r'or|one of', text, re.IGNORECASE)    
#             # if match_or:
#             #     # replace only the first occurrence
#             #     text = text.replace(match_or.group(), '',1)  
#             #     matched_confs.append('/')
        
#     print(text)
#     # return matches.values()
#     return matched_confs

# def match_confs_in_text(text, dictionary):
#     # Convert text to lowercase
#     text = text.lower()

#     # Sort keys from longest to shortest
#     sorted_keys = sorted(dictionary.keys(), key=len, reverse=True)

#     # Create a list to hold matches
#     matched_confs = []

#     # Check if any key is in the text
#     for key in sorted_keys:
#         lower_key = key.lower()
        
#         lower_keys = lower_key.split()
#         # Generate all permutations of the words
#         lower_key_permutations = [' '.join(perm) for perm in permutations(lower_keys)]
        
#         # Check if any of these permutations are in the text
#         for perm in lower_key_permutations:
#             if perm.lower() in text:
#                 text = text.replace(perm.lower(), '')
#                 matched_confs.append(dictionary[key])
#                 break  # Once a match is found, break the loop to avoid replacing other occurrences

#     # Insert '/' between found key codes
#     result = []
#     Or = ['or', 'one of']
#     And = ['and']
#     AndNot = ['except']
#     OrNot = ['or']
#     for i in range(len(matched_confs)):
#         result.append(matched_confs[i])
#         if i != len(matched_confs) - 1 and any(op in text for op in Or):  # Only add '/' if any operator is in the remaining text
#             result.append('/')
#             for op in Or:
#                 if op in text:
#                     text = text.replace(op, '', 1)  # Remove one occurrence of operator from the text
#                     break
            
#     print(text)
#     return result

def match_confs_in_text(text, dictionary):
    # Convert text to lowercase
    text = text.lower()

    # Sort keys from longest to shortest
    sorted_keys = sorted(dictionary.keys(), key=len, reverse=True)

    # Create a list to hold matches
    matched_confs = []

    # Define operators
    # operators = ['or', 'one of']

    # Check if any key is in the text
    for key in sorted_keys:
        lower_key = key.lower()
        
        lower_keys = lower_key.split()
        # Generate all permutations of the words
        lower_key_permutations = [' '.join(perm) for perm in permutations(lower_keys)]
        
        # Check if any of these permutations are in the text
        for perm in lower_key_permutations:
            if perm.lower() in text:
                text = text.replace(perm.lower(), '')
                matched_confs.append(dictionary[key])
                break  # Once a match is found, break the loop to avoid replacing other occurrences

    result = []
    
    # Insert '/-' between found key codes if 'or ... without' pattern is present
    OrNot_pattern = r'\bor .*? without\b'
    OrNot_match = re.search(OrNot_pattern, text)
    OrNot_operator = '/-'
    
    Or_pattern = r'\bor\b'
    Or_match = re.search(Or_pattern, text)
    Or_operator = '/'
    
    Not_pattern = r'\bwithout\b'
    Not_match = re.search(Not_pattern, text)
    Not_operator = '-'
    
    And_operator = '+'
    
    if OrNot_match:
        
        result.append('+' + OrNot_operator.join(matched_confs))
    elif Or_match:
        
        result.append('+' + Or_operator.join(matched_confs))
    elif Not_match:
        
        result.append('+' + Not_operator.join(matched_confs))
    else:
        
        result.append('+' + And_operator.join(matched_confs))    


    return result

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


text = "I am planning to order the IX with a sunroof or panorama glass roof sky lounge, and the EU Comfort Package or M Sport Package on 12th April 2018. Is this configuration possible?"

SteeringWheel_mapping = {
    'Left-Hand': 'LL',
    'Right-Hand': 'RL',
}

AvailablePackages_mapping = {
    'M Sport': 'P337A',
    'M Sport Pro': 'P33BA',
    'Comfort EU': 'P7LGA',
}

Roof_mapping = {
    'Panorama Glass Roof': 'S402A',
    'Panorama Glass Roof Sky Lounge': 'S407A',
    'Sunroof': 'S403A',
}

Model_mapping = {
    'iX xDrive50': '21CF',
    'iX xDrive40': '11CF',
    'X7 xDrive40i': '21EM',
    'X7 xDrive40d': '21EN',
    'M8': 'DZ01',
    '318i': '28FF'
}

# Model Type
modelTypeCodes = match_model_in_text(text, Model_mapping)
print(modelTypeCodes)

# Configuration
Roof_matches_code = match_confs_in_text(text, Roof_mapping)
AvailablePackages_matches_code = match_confs_in_text(text, AvailablePackages_mapping)
SteeringWheel_matches_code = match_confs_in_text(text, SteeringWheel_mapping)
# conf_list = Roof_matches_code + AvailablePackages_matches_code + SteeringWheel_matches_code

print(f'Roof_matches_code: {Roof_matches_code}')  
print(f'AvailablePackages_matches_code: {AvailablePackages_matches_code}')  
print(SteeringWheel_matches_code)  
# print(conf_list)

# Dates
date = date_in_text(text)
print(date)  
