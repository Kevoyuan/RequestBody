from itertools import permutations
from dateutil.parser import parse
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

import nltk 
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

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
   
    
    stemmer = PorterStemmer()

    # Create a new dictionary to hold the stemmed keys and values
    stemmed_dict = {}

    # Iterate over the items in the dictionary
    for key, value in dictionary.items():
        # Tokenize and stem the key
        words_in_key = nltk.word_tokenize(key.lower())
        stemmed_key = ' '.join(stemmer.stem(word) for word in words_in_key)

        # Tokenize and stem the value if it's a string
        if isinstance(value, str):
            words_in_value = nltk.word_tokenize(value)
            stemmed_value = ' '.join(stemmer.stem(word) for word in words_in_value)
        else:
            stemmed_value = value

        # Add the stemmed key-value pair to the stemmed dictionary
        stemmed_dict[stemmed_key] = stemmed_value
    print(f'stemmed_dict: {stemmed_dict}')
    # Sort keys from longest to shortest
    
    sorted_keys = sorted(stemmed_dict.keys(), key=len, reverse=True)

    # Create a list to hold matches
    matched_confs = []
    
    # Insert '/' between found key codes
    result = []
    Or = [r'\bor\b', 'one of']
    And = ['and']
    AndNot = ['except']
    OrNot = [r'\bwithout\b']
    
    # Check if any key is in the text
    for key in sorted_keys:
        lower_key = key.lower()
        
        lower_keys = lower_key.split()
        # Generate all permutations of the words
        lower_key_permutations = [' '.join(perm) for perm in permutations(lower_keys)]
        # print(lower_key_permutations)
        

        # Check if any of these permutations are in the text
        for perm in lower_key_permutations:
            if perm.lower() in text:
                perm_start_index = text.find(perm.lower())
                without_start_index = text.find('without')
                # Only consider 'without' if it's within a close range of the key
                if without_start_index != -1 and 0 <= perm_start_index - without_start_index <= 15:
                    text = text.replace('without', '', 1)
                    matched_confs.append('-' + stemmed_dict[key])
                else:
                    matched_confs.append(stemmed_dict[key])
                text = text.replace(perm.lower(), '')
            

    for i in range(len(matched_confs)):
        result.append(matched_confs[i])
    # print(f'\nresult: {len(result)}')
    
    # Adding Or operator if one configuration has 2 option from customer
    if len(result) == 2:
        result.insert(1, '/')
        
    # Check if '/' is in the list
    if '/' in result:
        # Add '(' at the start
        result.insert(0, '(')

        # Add ')' at the end
        result.append(')')
    if result and result[0][0].isalpha():
        result.insert(0, '+')
    
    
        # print("The list is not None")
    # print(text)
    return result



def date_in_text(text):
    # Clean the text
    # Trim leading and trailing whitespaces
    # date_text = text.strip()

    # # Remove multiple whitespaces
    # date_text  = re.sub(r'\s+', ' ', date_text )

    # # Remove symbols 
    # date_text = re.sub(r'\W+', ' ', date_text)

    # Parse the date from the text
    datetime_obj = parse(text , fuzzy=True, dayfirst=True)


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


def stem_text(text):
    stemmer = PorterStemmer()

    # Tokenize the sentence
    words = nltk.word_tokenize(text.lower())

    # Stem each word
    stemmed_words = [stemmer.stem(word) for word in words]

    # Join the stemmed words back into a sentence
    stemmed_text = ' '.join(stemmed_words)

    return stemmed_text

text = "Hello, is the X7 xDrive40i available without a panorama glass roof and with the EU Comfort Package. I need the vehicle on the 8th of November 2024."
# text = 'I want to order a BMW iX with right-hand drive configuration. I will be ordering it at the start of October 2022.'
# text = 'I am planning to order the BMW M8 with a sunroof or panorama glass roof sky lounge, and the M Sport Package or M Sport pro Package on 13th April 2018. Is this configuration possible?'
# text = 'valid for all panoramic roofs or iX xDrive50 with sunroof'


stemmed_text = stem_text(text)

print(stemmed_text)


SteeringWheel_mapping = {
    'Left-Hand': 'LL',
    'Right-Hand': 'RL',
}

AvailablePackages_mapping = {
    'M Sport Package': 'P337A',
    'M Sport Pro Package': 'P33BA',
    'Comfort EU Package': 'P7LGA',
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
print(f'modelTypeCodes: {modelTypeCodes}')

# Configuration

  
  


Roof_matches_code = match_confs_in_text(stemmed_text, Roof_mapping)

AvailablePackages_matches_code = match_confs_in_text(stemmed_text, AvailablePackages_mapping)

SteeringWheel_matches_code = match_confs_in_text(stemmed_text, SteeringWheel_mapping)

conf_list = Roof_matches_code + AvailablePackages_matches_code + SteeringWheel_matches_code

# print(f'Roof_matches_code: {Roof_matches_code}')  
# print(f'AvailablePackages_matches_code: {AvailablePackages_matches_code}')  
# print(f'SteeringWheel_matches_code: {SteeringWheel_matches_code}')  
# print(conf_list)
conf_string = ''.join(conf_list)
print(conf_string)


# Dates
date_string = date_in_text(stemmed_text)
print(date_string)  
