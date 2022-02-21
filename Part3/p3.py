# Ryan Kisner
# CMSC476
# Phase 3  

import math
import glob
import os
import sys
from bs4 import BeautifulSoup

MIN = 2
EMPTY_SPACE = '' # blank space  
OUTPUTFORMAT = '.txt'
STOPWORDS = []

here = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(here, 'stoplist.txt')
with open(file_name) as file:
    for word in file:
        STOPWORDS.append(word.rstrip('\n'))


def inverted_index(text):
    inverted = {}
    for index, word in word_helper(text):
        locations = inverted.setdefault(word,[])
        locations.append(index)
    return inverted

def inverted_index_add(inverted,doc_id, doc_index):
    for word, locations in doc_index.items():
        indices = inverted.setdefault(word,{})
        indices[doc_id] = locations
    return inverted

def split(text):
    word_list = []
    current_word = []
    index_word = []

    for i, c in enumerate(text):
        if c.isalpha():
            current_word.append(c)
            index_word = i
        elif current_word:
            word = ''.join(current_word)
            word_list.append((index_word -  len(word) + 1, word))
            current_word = []
    
    if current_word:
        word = ''.join(current_word)
        word_list.append((index_word - len(word) + 1, word))

    return word_list

def cleanup(words):
    clean_words = []
    for index, word in words:
        if len(word) <= MIN or word.lower() in STOPWORDS:
            continue
        clean_words.append((index, word))
    return clean_words

def normalize(words):
    normal_words = []
    for index, word in words:
        normal_word = word.lower()
        normal_words.append((index, normal_word))
    return normal_words


#######################
def _split(text):
    word_list = []
    current_word = []

    for i, c in enumerate(text):
        if c.isalpha():
            current_word.append(c)
        elif current_word:
            word = u''.join(current_word)
            word_list.append(word)
            current_word = []
    
    if current_word:
        word = u''.join(current_word)
        word_list.append(word)

    return word_list

def _cleanup(words):
    clean_words = []
    for word in words:
        if len(word) <= MIN or word in STOPWORDS:
            continue
        clean_words.append(word)
    return clean_words

def _normalize(words):
    normal_words = []
    for word in words:
        normal_word = word.lower()
        normal_words.append(normal_word)
    return normal_words

def _word_helper(text):
    words = _split(text)
    words = _normalize(words)
    words = _cleanup(words)
    return words

###################

def word_helper(text):
    words = split(text)
    words = normalize(words)
    words = cleanup(words)
    return words

# params: word_list - list of tokened words from current document 
# returns a TF dictionary for each word list
def wordListTFDict(word_list):
    review_TF_dict = {}
    for word in word_list:
        if word in review_TF_dict:
            review_TF_dict[word] += 1
        else:
            review_TF_dict[word] = 1
    #calculating the TF for each word
    for word in review_TF_dict:
        review_TF_dict[word] = review_TF_dict[word] / len(word_list)
    return review_TF_dict

# params: tf_weights - dictionary of tf's used to count the amount of words
# returns the frequency as a dictionary 
def frequencyDict(review_TF_dict):
    freq_dict = {}
    for tf in review_TF_dict:
        for word in tf:
            if word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
    return freq_dict

# params: word_list - list of tokened words from current document 
# params: freq_dict - dict of token freqeuncies 
# calculates the IDF value of each token
def IDFDict(word_list, freq_dict):
    idf_dict = {}
    for word in freq_dict:
        idf_dict[word] = math.log(len(word_list) / freq_dict[word])
    return idf_dict

# params: tf_weights - dictionary of tf's used to count the amount of words
# params: idf_dict - dictionary of IDF values
# calculates the TF-IDF map
def TFIDFDict(review_TF_dict, idf_dict):
    tfidf_dict = {}
    for i in review_TF_dict:
        tfidf_dict[i] = review_TF_dict[i] * idf_dict[i]
    return tfidf_dict

# params: input_dir - input directory of files
# params: output_dir - output directory of files
# takes in html files and tokenizes the text from the html
# outputs the tokenized words to text documents 
def tokenize(input_dir, output_dir):
    file_num = 1 # current number of scanned files
    #tf_weights = [] # complete dictionary of all tokens from all documents 
    tf_dict = []
    # complete_list = []
    documents = {}
    inverted = {}

    for file_name in glob.glob(os.path.join(input_dir, "*html")):
        print('Loading file:', file_num, end='\r')
        with open(file_name, encoding='Latin-1') as html:
            soup = BeautifulSoup(html, 'html.parser')
            # getting just the text from the html parse and creating a list out of each word
            word_list = soup.get_text()

            documents[str(f"{file_num:03}")] = word_list
            tf_dict.append(wordListTFDict(_word_helper(word_list)))
        file_num += 1
    for doc_id, text in documents.items():
        doc_index = inverted_index(text)
        inverted_index_add(inverted, doc_id, doc_index)

    print('Completed loading', file_num, 'files')
    print("Starting to export")

    print('Exporting postings_file.txt')
    index_list = [1]
    with open(os.path.join(output_dir, 'postings_file.txt'), 'w', encoding='utf-8') as output:
        counter = 1
        for word,doc_locations in sorted(inverted.items()):
            for i in range(len(tf_dict)):
                if str(word) in tf_dict[i]:
                    output.write(str(f"{i+1:003}") +',' + str(tf_dict[i][str(word)]) + '\n')
                    counter = counter + 1 
            index_list.append(counter)
    print('Complete')

    print("Exporting dictionary_records.txt")
    with open(os.path.join(output_dir, 'dictionary_records.txt'), 'w', encoding='utf-8') as output:
        index = 0
        for word,doc_locations in sorted(inverted.items()):
            output.write(str(word) + '\n')
            counter = 0
            for __ in doc_locations:
                counter = counter + 1 
            output.write(str(counter) + '\n' + str(index_list[index]) + '\n')
            index = index + 1
    print('Complete')
            
if __name__== '__main__':

    args = sys.argv
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    tokenize(input_dir, output_dir)



