import numpy as np
import pandas as pd
import json
import os

main_path = './../'
data_path = main_path + 'data/'

def process_individual(name):
    """Do all processing for an individual given a string of their name."""
    with open(data_path + 'raw_json/' + name) as json_file:
        data = json.load(json_file)


def main():
    people_names = [ name[:-4] for name in os.list(data_path + 'raw_json') ]


if __name__ == "__main__":
    main()
