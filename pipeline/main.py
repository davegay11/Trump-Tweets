#!/usr/bin/env python

'''
Pipeline to clean the data and generate models from the data. Run the file with:
    `./main.py [flags]`
'''

import numpy as np
import pandas as pd
import json
from pprint import pprint
import os
import argparse
from data_cleaning import clean_corpus
from model_word2vec import create_model
from vis_wordcloud import generate_wordcloud
from tfidf import similarity_to_trump

# Parse options passed in from the command line
parser = argparse.ArgumentParser(
    description="Automate the process of cleaning and creating models for our Trump Tweets project",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

# Basically alias the function to something shorter
add_arg = parser.add_argument
parser.add_argument('--cloud', dest='cloud', action='store_true',
        help="Make a wordcloud")
parser.add_argument('--no-cloud', dest='cloud', action='store_false',
        help="Skip the wordcloud")
parser.add_argument('--vec', dest='vec', action='store_true',
        help="Make a word2vec model of tweets")
parser.add_argument('--no-vec', dest='vec', action='store_false',
        help="Skip the vector embeddings")
parser.add_argument('--clean', dest='clean', action='store_true',
        help="Clean the tweets in the script")
parser.add_argument('--no-clean', dest='clean', action='store_false',
        help="Skip the cleaning stage")
parser.add_argument('--user', type=str, default=None,
        help="Specify a single user. Defaults to all")
parser.add_argument('-c', '--color', dest='color', action='store_true',
        help="Specify whether to include color in the wordcloud")
parser.add_argument('--no-color', dest='color', action='store_false',
        help="Specify to not include color in the wordcloud")
parser.add_argument('--sim', dest='sim', action='store_true',
        help="Perform tf-idf similarity analysis")
parser.add_argument('--no-sim', dest='sim', action='store_false',
        help="Don't perform similarity analysis")
parser.set_defaults(clean=True)
parser.set_defaults(vec=True)
parser.set_defaults(cloud=True)
parser.set_defaults(color=False)
parser.set_defaults(sim=True)
# parse the args
args = parser.parse_args()

# Define paths
main_path = os.path.join(os.path.dirname(__file__), '../')
model_path = main_path + 'models/'
data_path = main_path + 'data/'

def play_with_model(model):
    ''' Play with the word2vec models generated '''
    # Let's look at how the model performs
    for keyword in ['jobs', 'president', 'america', 'trump', 'hillary']:
        print "====> Keyword: {}".format(keyword)
        try:
            pprint(model.most_similar(keyword))
        except KeyError:
            print keyword + " not in vocabulary"

def process_individual(handle, i):
    """Do all processing for an individual given a string of their twitter handle."""
    print "------ PROCESSING @{} ----- ({})".format(handle, i)
    if args.clean:
        is_trump = handle == 'realdonaldtrump'
        size = clean_corpus(data_path + 'raw_json/' + handle, handle, is_trump=is_trump)
        # We don't process the tweets if there are less tha 1000 of them
        if size < 1000: return
    bin_dir = model_path + 'word2vec/'
    if not os.path.exists(data_path + 'clean_data/'):
        os.makedirs(data_path + 'clean_data/')
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
    # Create (and also save) a word2vec model of all of the tweets
    if args.vec:
        model = create_model(
            data_path + 'clean_data/' + handle + '.csv',
            model_path + 'word2vec/' + handle + '.bin',
            min_word_count=5,
            logging=False
        )
    # Let's also generate a wordcloud for each person
    if args.cloud:
        clean_path = main_path + 'data/clean_data/' + handle + '.csv'
        print "Generating wordcloud"
        generate_wordcloud(clean_path, handle, color=args.color)

def main():
    if args.user is not None:
        process_individual(args.user, 0)
    else:
        handles = [ name for name in os.listdir(data_path + 'raw_json') ]
        # First we clean the tweets for each of the individuals
        for i, handle in enumerate(handles):
            #  if handle in ['agscottpruitt']: continue
            process_individual(handle, i)
    # TF-IDF and cosine similarity. Needs to be outside process_individual
    # because the embedding needs to look at everyone at once
    if args.sim:
        similarity_to_trump()
    print "Finished!"

if __name__ == "__main__":
    main()
