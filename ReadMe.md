# Case Study 
This project provides a Python function to process a text and extract car model, configuration, and date information from it. The main function is `main()`, which takes a text string as input and returns a list of request bodies with the extracted information.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The function relies on several Python packages. These packages can be installed via pip:

```python
pip install stem_text
pip install date_in_text
pip install match_model_in_text
pip install match_confs_in_text
pip install request_body
pip install mapping
```

## Function Overview
The main function main() uses several sub-functions to process the text:

`stem_text(text)`: This function takes a string of text as input and returns the stemmed version of the text.
`match_model_in_text(text, Model_mapping)`: This function takes the text and a mapping dictionary as input. It returns the codes of the car models found in the text.
`match_confs_in_text(stemmed_text, Conf_mapping)`: This function takes the stemmed text and a configuration mapping dictionary as input. It returns the codes of the configurations found in the text.
`request_date_if_not_in_text(text)`: This function takes a string of text as input. If a date is found in the text, it is returned. If no date is found, the function prompts the user to input a date.
`create_request_bodies(modelTypeCodes, booleanFormulas, dates)`: This function takes the car model codes, configuration codes, and dates as input and returns a request bodies and save as JSON-file.

## Usage
Here is an example of how to use the function:

```python
from stem_text import stem_text
from date_in_text import date_in_text, request_date_if_not_in_text
from match_model_in_text import match_model_in_text
from match_confs_in_text import match_confs_in_text
from request_body import create_request_bodies
from mapping import SteeringWheel_mapping, AvailablePackages_mapping, Roof_mapping, Model_mapping

def main(text):
    # Function body
    # ...

text = 'Hello, is the X7 xDrive40i available without a panorama glass roof and with the EU Comfort Package. I need the vehicle on the 8th of November 2024.'
result = main(text)
print(result) # output: {'modelTypeCodes': ['21EM'], 'booleanFormulas': ['-S402A+P7LGA'], 'dates': ['2024-11-08']}
```
```json
{
    'modelTypeCodes': ['21EM'], 
    'booleanFormulas': ['-S402A+P7LGA'], 
    'dates': ['2024-11-08']
    }
```

In this example, the main() function will process the text and extract the car model, configuration, and date information from it. The result will be printed to the console.
