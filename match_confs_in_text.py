# match_confs_in_text.py
from nltk.stem import PorterStemmer
import nltk 
from itertools import permutations
from operators import operators


def match_confs_in_text(text, dictionary):
    stemmer = PorterStemmer()
    stemmed_dict = stem_dictionary(dictionary)
    sorted_keys = sorted(stemmed_dict.keys(), key=len, reverse=True)
    matched_confs = []

    result = []

    stemmed_operators = [
        ([' '.join(stemmer.stem(word) for word in nltk.word_tokenize(op)) for op in ops], symbol)
        for ops, symbol in operators
    ]

    for key in sorted_keys:
        lower_key = key.lower()
        lower_keys = lower_key.split()
        lower_key_permutations = [' '.join(perm) for perm in permutations(lower_keys)]

        for perm in lower_key_permutations:
            if perm.lower() in text:
                perm_start_index = text.find(perm.lower())
                for stemmed_ops, symbol in stemmed_operators:
                    for stemmed_op in stemmed_ops:
                        op_start_index = text.find(stemmed_op)
                        if op_start_index != -1 and 0 <= perm_start_index - op_start_index <= 15:
                            text = text.replace(stemmed_op, '', 1)
                            matched_confs.append(symbol + stemmed_dict[key])
                            break
                    else:
                        continue
                    break
                else:
                    matched_confs.append(stemmed_dict[key])
                text = text.replace(perm.lower(), '')

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

    for key, value in dictionary.items():
        words_in_key = nltk.word_tokenize(key.lower())
        stemmed_key = ' '.join(stemmer.stem(word) for word in words_in_key)

        if isinstance(value, str):
            words_in_value = nltk.word_tokenize(value)
            stemmed_value = ' '.join(stemmer.stem(word) for word in words_in_value)
        else:
            stemmed_value = value

        stemmed_dict[stemmed_key] = stemmed_value
    
    return stemmed_dict

