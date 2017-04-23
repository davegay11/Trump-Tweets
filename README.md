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

## Raw data

The raw data can be found in `./data/trump_tweet_data_archive/`, and was pulled from [The Trump Twitter Archive](http://www.trumptwitterarchive.com/)

## Cleaning

`data_cleaning.ipynb` contains the code relating to the cleaning of the tweets saved in the json files in `./data/trump_tweet_data_archive/master_YEAR.json`. It outputs a json and csv file in the `clean_data` directory, representing the final, cleaned data.

`fields.txt` contains an ascii table describing each field in the cleaned data and what values it can take on.

## Representations / Analysis

Because we had our data cleaned a bit early, we started using it to perform some basic analysis of his tweets. The files `bag_of_words.ipynb`, `n_gram.ipynb`, and `word2vec.ipynb` all create different NLP representations of his tweets, and start to try to make sense of them. As the project progresses we will clean up / add more to these files.

## Required packages

> Install with pip install [package_here]

- wordcloud
- nltk
- gensim

Specifically from NLTK you need the vader lexicon and stopwords corpus

## Licence

This data is made available under the Public Domain Dedication and License version v1.0 whose full text can be found at http://opendatacommons.org/licenses/pddl/ or located in license.txt within this repository.
