# match_confs_in_text.py
from nltk.stem import PorterStemmer
import nltk 
from itertools import permutations
from operators import operators


def match_confs_in_text(text, dictionary):
    stemmer = PorterStemmer()
    stemmed_dict = stem_dictionary(dictionary)
    # Match the longer key first to prevent duplication
    sorted_keys = sorted(stemmed_dict.keys(), key=len, reverse=True)
    matched_confs = []

    result = []

    stemmed_operators = [
        ([' '.join(stemmer.stem(word) for word in nltk.word_tokenize(op)) for op in ops], symbol)
        for ops, symbol in operators
    ]

    # Iterate over the keys in the stemmed dictionary.
    # The keys are sorted in decreasing order of length, so longer keys are checked first.
    for key in sorted_keys:
        
        # Split the lowercase key into individual words.
        keys = key.split()
        
        # Generate all permutations of the words in the key.
        key_permutations = [' '.join(perm) for perm in permutations(keys)]

        # Check each permutation to see if it appears in the text.
        for perm in key_permutations:
            # If the permutation is found in the text,
            if perm in text:
                # Record the start index of the permutation in the text.
                perm_start_index = text.find(perm)
                
                # Check each operator.
                for stemmed_ops, symbol in stemmed_operators:
                    # For each phrase that represents the operator,
                    for stemmed_op in stemmed_ops:
                        # If the phrase is found in the text and is close to the permutation,
                        op_start_index = text.find(stemmed_op)
                        if op_start_index != -1 and 0 <= perm_start_index - op_start_index <= 15:
                            # Remove the operator phrase from the text.
                            text = text.replace(stemmed_op, '', 1)
                            
                            # Add the symbol of the operator and the value of the key to the list of matched configurations.
                            matched_confs.append(symbol + stemmed_dict[key])
                            
                            # Stop checking other phrases for this operator.
                            break
                    else:
                        # If none of the phrases of the operator were found near the permutation, continue to the next operator.
                        continue
                    
                    # If a phrase of an operator was found near the permutation, stop checking other operators.
                    break
                else:
                    # If no operator was found near the permutation, add the value of the key to the list of matched configurations.
                    matched_confs.append(stemmed_dict[key])
                
                # Remove the permutation from the text.
                text = text.replace(perm, '')


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

def stem_dictionary(dictionary):
    stemmer = PorterStemmer()

    stemmed_dict = {}

    # Iterate over the items in the original dictionary.
    for key, value in dictionary.items():
        # Tokenize the key into individual words and convert it to lowercase.
        words_in_key = nltk.word_tokenize(key.lower())
        
        # Stem each word in the key and join them back together into a single string.
        stemmed_key = ' '.join(stemmer.stem(word) for word in words_in_key)

        # If the value is a string, tokenize and stem it just like the key.
        if isinstance(value, str):
            words_in_value = nltk.word_tokenize(value)
            stemmed_value = ' '.join(stemmer.stem(word) for word in words_in_value)
        else:
            # If the value is not a string, don't try to stem it.
            stemmed_value = value

        stemmed_dict[stemmed_key] = stemmed_value
    
    return stemmed_dict

