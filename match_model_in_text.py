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