# Trump's Tweets
## Group Members: 
    * Andrew Cho
    * Bryce Wolery
    * Christopher Sides
    * Dave Gay
    * Jeremy Fox
    * Sean Hudson
    * Zachary Marion

This is the official repository for The Trump's Tweets team in Professor Herron's Humanities: Data Mining + Meaning class at Duke University.

## Data Aquisition and Cleaning

To get the data, run the following script from the root project directory:

`./scripts/get_data.sh`

To clean the data and generate the models, run:

`./pipeline/main.py`

By default it cleans the data, generates word2vec models, and creates wordclouds for each individual. The file is formatted as a command line utility, whose options can be found with:

`/pipeline/main.py --help`

`fields.txt` contains an ascii table describing each field in the cleaned data and what values it can take on.

## Representations / Analysis

Because we had our data cleaned a bit early, we started using it to perform some basic analysis of his tweets. The files `bag_of_words.ipynb`, `n_gram.ipynb`, and `word2vec.ipynb` all create different NLP representations of his tweets, and start to try to make sense of them. As the project progresses we will clean up / add more to these files.

## Required packages

To install the required pip modules we recommend using virtualenv

Initilaize your virtual environment with:

`virtualenv ~/.trump`

Source the environment with:

`source ~/.trump/bin/activate`

Next (in the repository root), install the packages necessary for this project with:

`pip install -r requirements.txt`

NOTE: Because matplotlib is a bit wierd, you need to make the file `~/.matplotlib/matplotlibrc` and in it put "backend: TkAgg". This can be done with:

`echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc`

Specifically from NLTK you need the vader lexicon and stopwords corpus. These can be installed through python using the command `nltk.download()` and following the GUI.

## Licence

This data is made available under the Public Domain Dedication and License version v1.0 whose full text can be found at http://opendatacommons.org/licenses/pddl/ or located in license.txt within this repository.
