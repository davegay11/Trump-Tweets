import numpy as np
import pandas as pd
import json
import os
from data_cleaning import clean_corpus

main_path = os.path.join(os.path.dirname(__file__), './../')
data_path = main_path + 'data/'

def process_individual(name):
    """Do all processing for an individual given a string of their name."""
    clean_corpus(data_path + 'raw_json/' + name + '.json', name)

def main():
    people_names = [ name[:-5] for name in os.listdir(data_path + 'raw_json') ]
    for name in people_names:
        process_individual(name)

if __name__ == "__main__":
    main()
