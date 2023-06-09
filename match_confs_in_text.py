# match_confs_in_text.py
from nltk.stem import PorterStemmer
import nltk 
from itertools import permutations
from operators import operators

def stem_dictionary(dictionary):
    # This function takes a dictionary of keys and values, and returns a new dictionary where all the keys and values have been stemmed. 
    stemmer = PorterStemmer()
    stemmed_dict = {}

    for key, value in dictionary.items():
        words_in_key = nltk.word_tokenize(key.lower())
        stemmed_key = ' '.join(stemmer.stem(word) for word in words_in_key)
        stemmed_value = stem_value(value)
        stemmed_dict[stemmed_key] = stemmed_value
    return stemmed_dict

def stem_value(value):
    # This function stems a value if it's a string.
    stemmer = PorterStemmer()
    if isinstance(value, str):
        words_in_value = nltk.word_tokenize(value)
        stemmed_value = ' '.join(stemmer.stem(word) for word in words_in_value)
    else:
        stemmed_value = value
    return stemmed_value

def match_confs_in_text(text, dictionary):
    stemmer = PorterStemmer()
    stemmed_dict = stem_dictionary(dictionary)
    # Match the longer key first to prevent duplication
    sorted_keys = sorted(stemmed_dict.keys(), key=len, reverse=True)
    matched_confs = []

    result = []
    
    stemmed_operators = generate_stemmed_operators(operators, stemmer)

    # Iterate over the keys in the stemmed dictionary
    # The keys are sorted in decreasing order of length, so longer keys are checked first.
    for key in sorted_keys:
        match, text = check_permutations(text, key, stemmed_operators, stemmed_dict)
        if match is not None:
            matched_confs.append(match)


    for i in range(len(matched_confs)):
        result.append(matched_confs[i])

    if len(result) > 1:
        result.insert(1, '/')

    if '/' in result:
        result.insert(0, '(')
        result.append(')')

    if result and (result[0][0].isalpha() or result[0][0]=='('):
        result.insert(0, '+')

    return result

def generate_stemmed_operators(operators, stemmer):
    # This function takes a list of operators and a stemmer, and returns a new list where all the operators have been stemmed
    stemmed_operators = [
        ([' '.join(stemmer.stem(word) for word in nltk.word_tokenize(op)) for op in ops], symbol)
        for ops, symbol in operators
    ]
    return stemmed_operators


def check_permutations(text, key, stemmed_operators, stemmed_dict):
    # Split the key into individual words
    keys = key.split()

    # Generate all permutations of the words in the key
    key_permutations = [' '.join(perm) for perm in permutations(keys)]

    # Check each permutation to see if it appears in the text
    for perm in key_permutations:
        # If the permutation is found in the text,
        if perm in text:
            # Record the start index of the permutation in the text
            perm_start_index = text.find(perm)

            # Check each operator.
            for stemmed_ops, symbol in stemmed_operators:
                # For each phrase that represents the operator,
                for stemmed_op in stemmed_ops:
                    # If the phrase is found in the text and is close to the permutation
                    op_start_index = text.find(stemmed_op)
                    if op_start_index != -1 and 0 <= perm_start_index - op_start_index <= 15:
                        # Remove the operator phrase from the text
                        text = text.replace(stemmed_op, '', 1)

                        # Add the symbol of the operator and the value of the key to the list of matched configurations
                        return symbol + stemmed_dict[key], text

            # If no operator was found near the permutation, add the value of the key to the list of matched configurations
            text = text.replace(perm, '')
            return stemmed_dict[key], text

    return None, text
