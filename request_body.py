import json

def create_request_body(modelTypeCodes, booleanFormulas, dates):
    # Create a dictionary
    request_body = {
        "modelTypeCodes": modelTypeCodes,
        "booleanFormulas": booleanFormulas,
        "dates": dates
    }

    # Convert the dictionary to a JSON object
    json_request_body = json.dumps(request_body)

    return json_request_body