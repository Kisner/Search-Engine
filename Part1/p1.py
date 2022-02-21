# Ryan Kisner
# CMSC476
# Phase 1  

import glob
import os
from bs4 import BeautifulSoup
import time

# params: input_dir - input directory of files
# params: output_dir - output directory of files
# takes in html files and tokenizes the text from the html
# outputs the tokenized words to text documents 
def tokenize(input_dir, output_dir):

    file_num = 1 # current number of scanned files
    complete_dict = {} # complete dictionary of all tokens from all documents 
    
    for file_name in glob.glob(os.path.join(input_dir, "*html")):
        print('Loading file:', file_num, end='\r')
        file_num += 1
        solo_dict = {} # dictionary for tokens of a single document 
        with open(file_name, encoding='Latin-1') as html:
            soup = BeautifulSoup(html, 'html.parser')
            # getting just the text from the html parse and creating a list out of each word
            word_list = soup.get_text()
            word_list = word_list.split()

            # adding each word to a dict. converting to lowercase and removing non alpha characters
            # duplicates are not allowed, adding 1 to value if key matches word.
            for word in word_list:
                new_word = ''.join(filter(str.isalpha,word))
                if new_word.lower() in solo_dict:
                    solo_dict[new_word.lower()] += 1
                else:
                    solo_dict[new_word.lower()] = 1
            for word in word_list:
                new_word = ''.join(filter(str.isalpha,word))
                if new_word.lower() in complete_dict:
                    complete_dict[new_word.lower()] += 1
                else:
                    complete_dict[new_word.lower()] = 1
        
        # taking collected tokens and outputting to file in order of most used to least used
        results_name = os.path.basename(file_name)
        results_name = os.path.splitext(results_name)[0] + '.txt'
        with open(os.path.join(output_dir, results_name), 'w') as output:
            for word in sorted(solo_dict.items(), key = lambda x: x[1], reverse = True):
                output.write(word[0] + '\n')

    # creating a file with all tokens order from most cused to least used
    with open(output_dir + '\\frequencySorted.txt', 'w') as output:
        for word in sorted(complete_dict.items(), key = lambda x: x[1], reverse = True):
            output.write(word[0] + ':' + str(word[1]) + '\n')

    # creating a file with all tokens in alphabetical order
    with open(output_dir + '\\tokenSorted.txt', 'w') as output:
        for word in sorted(complete_dict.items(), key = lambda x: x[0], reverse = False):
            output.write(word[0] + ':' + str(word[1]) + '\n')

    print('Completed loading', file_num, 'files')

if __name__== '__main__':

    input_dir = input('Please enter the input file path: ')
    output_dir = input('Please enter the output file path: ')

    tokenize(input_dir, output_dir)
