import pandas as pd
import numpy as np
import json
import sys
import os

def gen_ngram(textData,gramLength,textField):
    grams = {}
    #Iterate through each tweet to create the n-grams
    count = 0
    for tweetTxt in textData[textField]:
        #Print which tweet is currently being analyzed (every 2000)
        count +=1
        if count%2000==0:
            print("Analyzing tweet " + str(count) + " for grams of length " + str(gramLength))
            print("Currently have  " + str(len(grams))+ " unique grams")
            sys.stdout.flush()
        #Split each tweet into words
        words = tweetTxt.split()
        #Iterate through all the n-grams in each tweet
        for i in range(0,len(words)-gramLength+1):
            #Create the current n-gram (of length gramLength)
            #Gram starts at word[i] and goes to word[i+gramLength-1]
            curGram = ""
            for j in range(0,gramLength):
                curGram = curGram + words[i+j] + " "
            #Remove trailing space from n-gram
            curGram = curGram[:-1]
            #Update dictionary with n-gram and gram count
            if grams.get(curGram)!=None:
                grams[curGram] = grams.get(curGram) + 1
            else:
                grams[curGram] = 1
    return grams

def sort_ngram(gram_dict):
    sortedGrams = []
    #Make a list of grams ordered by frequency
    for gram,val in gram_dict.iteritems():
        sortedGrams.append([gram,val])
    sortedGrams.sort(key=lambda x: x[1],reverse=True)
    return sortedGrams

#Save gram file as json to saved_n_grams directory
def save_ngram(gram_dict,filename):
    #Create directory if neccesary 
    directory = os.path.abspath("saved_n_grams")
    if not os.path.exists(directory):
            os.makedirs(directory)
    
    #write tweet objects to JSON
    with open(directory+"/"+filename+'.json', 'w') as saveFile:
        json.dump(gram_dict, saveFile)
    print "Done"

def load_ngram(filename):
    with open("saved_n_grams/"+filename) as loadFile:
        gram_dict = json.load(loadFile)
    return gram_dict