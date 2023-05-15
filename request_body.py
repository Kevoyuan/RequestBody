import json

def create_request_bodies(modelTypeCodes, booleanFormulas, dates):
    # Iterate over each model type code
    for i, model in enumerate(modelTypeCodes):
        # Create a dictionary for each request
        request_body = {
            "modelTypeCodes": [model],
            "booleanFormulas": booleanFormulas,
            "dates": dates
        }
        
        # Save to a JSON file
        with open(f'request_body_{i}.json', 'w') as file:
            json.dump(request_body, file)

        print(request_body)
    return "Request bodies saved as JSON files."