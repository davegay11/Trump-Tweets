import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

main_path = os.path.join(os.path.dirname(__file__), '../')

def get_bag_of_words(path):
    print "reading: " + str(path)
    '''Read in the csv of clean tweet data. Combines all cleaned tweets and
    represents them in BoW format -- a list of strings
    path -- location of csv to read'''
    # the following is a not-so-great way to get the BoW
    data = pd.read_csv(path, usecols=['clean_text']).values.tolist() # comes in as a list of list of strings
    strlist = [string for sublist in data for string in sublist] # list of strings
    # get rid of any NaN values
    strlist = filter(lambda v: v==v, strlist)
    bag_of_words = [ word for sublist in strlist for word in sublist.split() ] # list of words
    return bag_of_words


def similarity_to_trump():
    '''Take all the clean tweets and see how close the corpora are to that of
    realdonaldtrump's. Uses TFIDF embedding, cosine similarity, and a
    linear kernel.'''
    bags = []
    trump_idx = 0
    # only grab csvs
    path = main_path + 'data/clean_data/'
    people = filter(lambda person: person[-3:] == 'csv', os.listdir(path))
    for idx, name in enumerate(people):
        bags.append(get_bag_of_words(path + name))
        if 'realdonaldtrump' in name:
            trump_idx = idx
    # turn into a list of strings so that tfidf can accept it
    bags = [' '.join(sublist) for sublist in bags]
    # sklearn magic. Each corpus becomes one vector, each word an axis.
    tfidf = TfidfVectorizer().fit_transform(bags)
    # calculate similarity of each corpus to that of realdonaldtrump's
    cosine_similarities = linear_kernel(tfidf[trump_idx:trump_idx + 1], tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()[::-1]
    # trim off the csv extension
    people = map(lambda person: person[:-4], people)
    # sort by similarity
    people = np.array(people)[related_docs_indices]
    # put in same order as people
    cosine_similarities = cosine_similarities[related_docs_indices]
    with open(main_path + 'data/tf_idf/scores.csv', 'w') as f:
        f.write('name, similarity_to_trump,\n')
        for person, cosine in zip(people, cosine_similarities):
            f.write(person + ', ' + str(cosine) + ',\n')

if __name__ == "__main__":
    similarity_to_trump()
