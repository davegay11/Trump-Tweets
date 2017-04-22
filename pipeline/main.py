#!/usr/bin/env python

import numpy as np
import pandas as pd
import json
import os
import argparse
from data_cleaning import clean_corpus
from model_word2vec import create_model

# Parse options passed in from the command line
parser = argparse.ArgumentParser(
    description="Automate the process of cleaning and creating models for our Trump Tweets project",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

# Basically alias the function to something shorter
add_arg = parser.add_argument
parser.add_argument('--clean', dest='clean', action='store_true')
parser.add_argument('--no-clean', dest='clean', action='store_false')
parser.set_defaults(feature=True)
# parse the args
args = parser.parse_args()

# Define paths
main_path = os.path.join(os.path.dirname(__file__), './../')
model_path = main_path + 'models/'
data_path = main_path + 'data/'

def process_individual(handle):
    """Do all processing for an individual given a string of their name."""
    print "------ PROCESSING @{} -----".format(handle)
    if handle == "realdonaldtrump": return #erroring for some reason
    clean_corpus(data_path + 'raw_json/' + handle, handle)
    #  model = create_model(data_path + 'clean_data/' + handle + '.csv', \
            #  model_path + 'word2vec/' + handle + '.bin', min_word_count=1)
    #  # Let's look at how the model performs
    #  for keyword in ['jobs', 'president', 'America', 'trump', 'hillary']:
        #  try:
            #  print model.most_similar(keyword)
        #  except KeyError:
            #  print keyword + " not in vocabulary"

def main():
    handles = [ name for name in os.listdir(data_path + 'raw_json') ]
    # First we clean the tweets for each of the individuals
    for handle in handles:
        process_individual(handle)

if __name__ == "__main__":
    main()
