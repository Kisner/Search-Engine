# Ryan Kisner
# CMSC476
# Phase 1  

import math
import glob
import os
import sys
from bs4 import BeautifulSoup

EMPTY_SPACE = '' # blank space  
OUTPUTFORMAT = '.txt'
STOPWORDS = []

here = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(here, 'stoplist.txt')
with open(file_name) as file:
    for word in file:
        STOPWORDS.append(word.rstrip('\n'))

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
    complete_list = []
    
    for file_name in glob.glob(os.path.join(input_dir, "*html")):
        print('Loading file:', file_num, end='\r')
        file_num += 1
        with open(file_name, encoding='Latin-1') as html:
            soup = BeautifulSoup(html, 'html.parser')
            # getting just the text from the html parse and creating a list out of each word
            word_list = soup.get_text()
            word_list = word_list.split()

            # filters out non alpha chars, removes extra white space, and converts to lower case
            word_list = [EMPTY_SPACE.join(filter(str.isalpha,word)) for word in word_list]
            word_list = [word for word in word_list if word]
            word_list = [word.lower() for word in word_list]
            word_list = [word for word in word_list if word not in STOPWORDS]
            complete_list.append([word for word in word_list])
            tf_dict.append(wordListTFDict(word_list))


    freq_dict = frequencyDict(tf_dict)
    print(freq_dict['morning'])
    idf_dict = IDFDict(complete_list, freq_dict)
    tfidf_dict = [TFIDFDict(word, idf_dict) for word in tf_dict]
    print('Completed loading', file_num, 'files')

    counter = 1
    for document in tfidf_dict:
        with open(os.path.join(output_dir, str(f"{counter:03}" + '.txt')), 'w', encoding='utf-8') as output:
            for word in document:
                output.write(word + ' ' + str(document[word]) + '\n')
        counter += 1
        

if __name__== '__main__':

    args = sys.argv
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    tokenize(input_dir, output_dir)



