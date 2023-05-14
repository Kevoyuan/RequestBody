from nltk.stem import PorterStemmer
import nltk 
from itertools import permutations


def match_confs_in_text(text, dictionary):
   
    stemmer = PorterStemmer()
    
    stemmed_dict = stem_dictionary(dictionary)
    
    # Sort keys from longest to shortest
    sorted_keys = sorted(stemmed_dict.keys(), key=len, reverse=True)

    # Create a list to hold matches
    matched_confs = []
    
    # Insert '/' between found key codes
    result = []
    Or = [r'\bor\b', 'one of']
    And = ['and']
    AndNot = ['except']
    # OrNot = [r'\bwithout\b']
    
    negations = ['without', 'not including', 'excluding']
    # Stem the negations
    stemmed_negations = [' '.join(stemmer.stem(word) for word in nltk.word_tokenize(negation)) for negation in negations]
    
    
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
                for negation in negations:
                    negation_start_index = text.find(negation)
                    # Only consider the negation word if it's within a close range of the key
                    if negation_start_index != -1 and 0 <= perm_start_index - negation_start_index <= 15:
                        text = text.replace(negation, '', 1)
                        matched_confs.append('-' + stemmed_dict[key])
                        break
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
    if result and (result[0][0].isalpha() or result[0][0]=='('):
        result.insert(0, '+')
    
    
        # print("The list is not None")
    # print(text)
    return result

def stem_dictionary(dictionary):
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
    # print(f'stemmed_dict: {stemmed_dict}')
    
    return stemmed_dict