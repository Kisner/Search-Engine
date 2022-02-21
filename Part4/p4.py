import math
import glob
import os
import sys

term_weights = {}
doc_score = {}
weight_flag = False

def execute(tokens):
    dict_list = []
    temp_dict = {}
    here = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(here,'dictionary_records.txt')
    file_name = os.path.join(here,'dictionary_records.txt')
    with open(file_name) as file:
        for record in file:
            dict_list.append(record.rstrip('\n'))


    for i in range(len(dict_list)):
        if not i + 2  >= len(dict_list):
            temp_dict[dict_list[i]] = (dict_list[i+1], dict_list[i+2])
            i = i+2

    for term in tokens:
        term = term.lower()
        for word in temp_dict:
            if word == term:
                freq = int(temp_dict[word][0])
                start = int(temp_dict[word][1])
                readPostings(start, start+freq+1, term)
                break

    if len(doc_score) == 0:
        print("No relevant documents were found for the provided query.")
    else:
        counter = 0        
        for token in sorted(doc_score.items(), key = lambda x: str(x[1]), reverse= True):
            if counter == 10:
                break
            print(token[0], token[1])
            counter = counter + 1

def readPostings(start, end, term):
    here = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(here,'postings_file.txt')
    with open(file_name) as file:
        for __ in range(start, end):
            doc_with_score = str(file.readline()).rstrip('\n')
            doc = doc_with_score.split(',')[0]
            score = doc_with_score.split(',')[1]
            update(doc,score,term)

def update(doc, score, term):
    weight = float(term_weights.get(term))
    updated_score = weight * float(score)
    if doc in doc_score:
        doc_score[doc] = int(float(doc_score[doc])) + int(float(updated_score))
    else:
        doc_score[doc] = updated_score

def getTerms(args, terms, weights):
    for i in range(1, len(args)):
        if i % 2 == 0:
            terms.append(args[i])
        else:
            weights.append(args[i])

def weightMap(terms, weights):
    for i in range(len(terms)):
        if weight_flag:
            term_weights[terms[i].lower()] = weights[i]
        else:
            term_weights[terms[i].lower()] = 1.0



if __name__ == '__main__':
    terms = []
    weights = []
    args = sys.argv[1:]
    if args[0] == 'Wt':
        weight_flag = True
        getTerms(args, terms, weights)
    else:
        terms = args
    weightMap(terms, weights)
    execute(terms)
