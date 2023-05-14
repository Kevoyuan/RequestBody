from itertools import permutations

from nltk.stem import PorterStemmer
import nltk

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from stem_text import stem_text
from date_in_text import date_in_text, request_date_if_not_in_text
from match_model_in_text import match_model_in_text
from match_confs_in_text import match_confs_in_text
from request_body import create_request_bodies
from mapping import SteeringWheel_mapping, AvailablePackages_mapping, Roof_mapping, Model_mapping


# # Model Type
# modelTypeCodes = match_model_in_text(text, Model_mapping)
# # print(f'modelTypeCodes: {modelTypeCodes}')
# print(modelTypeCodes)
# # Configuration


# Roof_matches_code = match_confs_in_text(stemmed_text, Roof_mapping)

# AvailablePackages_matches_code = match_confs_in_text(stemmed_text, AvailablePackages_mapping)

# SteeringWheel_matches_code = match_confs_in_text(stemmed_text, SteeringWheel_mapping)

# conf_list = Roof_matches_code + AvailablePackages_matches_code + SteeringWheel_matches_code

# # print(f'Roof_matches_code: {Roof_matches_code}')
# # print(f'AvailablePackages_matches_code: {AvailablePackages_matches_code}')
# # print(f'SteeringWheel_matches_code: {SteeringWheel_matches_code}')
# # print(conf_list)
# conf_string = ''.join(conf_list).upper()
# print([conf_string])


# # Dates
# date_string = request_date_if_not_in_text(text)
# print([date_string])

# # Test the function
# modelTypeCodes = modelTypeCodes
# booleanFormulas = [conf_string]
# dates = [date_string]


# print(create_request_body(modelTypeCodes, booleanFormulas, dates))
def main(text):
    stemmed_text = stem_text(text)

    # Model Type
    modelTypeCodes = match_model_in_text(text, Model_mapping)

    # Configuration
    Roof_matches_code = match_confs_in_text(stemmed_text, Roof_mapping)
    AvailablePackages_matches_code = match_confs_in_text(
        stemmed_text, AvailablePackages_mapping)
    SteeringWheel_matches_code = match_confs_in_text(
        stemmed_text, SteeringWheel_mapping)
    conf_list = Roof_matches_code + \
        AvailablePackages_matches_code + SteeringWheel_matches_code
    conf_string = ''.join(conf_list).upper()

    # Dates
    date_string = request_date_if_not_in_text(text)

    modelTypeCodes = modelTypeCodes
    booleanFormulas = [conf_string]
    dates = [date_string]

    return create_request_bodies(modelTypeCodes, booleanFormulas, dates)


# text = "Hello, is the X7 xDrive40i available without a panorama glass roof and with the EU Comfort Package. I need the vehicle on the 8th of November 2024."
text = 'I want to order a BMW iX with right-hand drive configuration. I will be ordering it at the end of October 2022.'
# text = 'I am planning to order the BMW M8 with a sunroof or panorama glass roof sky lounge, and the M Sport Package on 12th April 2018. Is this configuration possible?'
# text = 'valid for all panoramic roofs or iX xDrive50 with sunroof or Panorama Glass Roof '
# text = 'valid if the sunroof and at the same time iX xDrive50 or the optional panoramic roof are selected at the end of October 2022'

stemmed_text = stem_text(text)

print(stemmed_text)


result = main(text)
print(result)
