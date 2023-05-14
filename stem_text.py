from nltk.stem import PorterStemmer
import nltk 

def stem_text(text):
    stemmer = PorterStemmer()

    # Tokenize the sentence
    words = nltk.word_tokenize(text.lower())

    # Stem each word
    stemmed_words = [stemmer.stem(word) for word in words]

    # Join the stemmed words back into a sentence
    stemmed_text = ' '.join(stemmed_words)

    return stemmed_text