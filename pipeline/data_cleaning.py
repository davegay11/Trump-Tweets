import pandas as pd
from nltk.corpus import stopwords
import json
import csv
import os
import re
import nltk

main_path = os.path.join(os.path.dirname(__file__), './../')

def get_raw_data(path):
    '''Get the raw json data downloaded from the tweepy API'''
    tweets = []
    for filename in os.listdir(path):
        with open(path + '/' + filename) as f:
            data = json.load(f)
            tweets += data
    return tweets

def get_input_fields(tweets):
    '''Get all of the fields in the data (rows in the csv header). Note that for the csv 
    file we only include fields that we can put in a csv file
    '''
    all_fields = []
    csv_fields = []
    blacklist = [u'possibly_sensitive', u'quoted_status_id', u'quoted_status_id_str']
    for key, value in tweets[0].iteritems():
        valid_types = (int, float, unicode, str, bool)
        if any([isinstance(value, valid_type) for valid_type in valid_types]) and \
                key not in blacklist:
            csv_fields.append(key)
        all_fields.append(key)
    return (all_fields, csv_fields)

def json_2_csv(json, filename, fields):
    '''Convert a python dict to csv and write it to a file'''
    fail_count = 0
    with open(filename, 'w') as f:
        # First erase all the previous contents of the file
        f.truncate()
        # create the csv writer object
        writer = csv.writer(f)
        rows = 0
        for entry in json:
            if rows == 0:
                header = fields
                writer.writerow(header)
                rows += 1
            try:
                vals = [unicode(entry[key]).encode('utf-8') for key in fields]
                writer.writerow(vals)
            except UnicodeEncodeError:
                fail_count += 1
    print "Could not parse the contents of %d entries" % fail_count

# Now that we know all of the sources, let's map them to a shorter string
def get_source(source):
    '''Return what medium the tweet was sent from'''
    if source is None:
        return ""
    # The source will now be one of the following text fields
    source_list = ['instagram', 'web', 'ipad', 'android', 'iphone', 'ads',
                    'periscope', 'media', 'qanda', 'twitlonger', 'vine', 
                    'blackberry', 'facebook', 'tweetdeck', 'websites']
    if not isinstance(source, str):
        return 'other'
    if not any(word in source for word in source_list):
        return 'other'
    stripped = re.match('<a .*>(.*?)</a>', source).group(1).lower().split()
    return "".join([w for w in stripped if w in source_list])

# Let's put it all together in a function
def clean_text(text, remove_stopwords=True):
    '''Function to remove punctuation and stopwords from text. Note that we keep
    the @ symbol as a hashtag adds meaning'''
    # First let's get rid of links, as they will mess up our bag or words...for 
    # example, one of the links is "https://t.co/BSp685Q9Qf https://t.co/K7yeBZsf6r'",
    # which just turns into gibberish
    # source: http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
    link_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    no_links = re.sub(link_regex, " ", text)
    word_list = re.sub("[^@a-zA-Z]", " ", no_links).lower().split()
    # Searching a set is faster in python
    stops = set(stopwords.words("english")) if remove_stopwords else set()
    # blacklist of words that we should ignore...for example amp is really just &,
    # so it appears a ton but has no semantic value
    blacklist = set(['amp'])
    clean_list = [w for w in word_list if (w not in stops and w not in blacklist)]
    return " ".join( clean_list ) if len(clean_list) > 0 else " "

def clean_corpus(path, clean_data_name):
    ''' Function to clean a given tweet corpus
    filename - Folder where all the tweets are kept
    clean_data_name - Name of the clean data to be saved
    '''
    tweets = get_raw_data(path)
    all_fields, csv_fields = get_input_fields(tweets)
    print (csv_fields)
    # Save the tweets in a csv format
    json_2_csv(tweets, main_path + "tmp/raw_tweets.csv", csv_fields)
    # Now lets read the contents of the file with pandas
    df = pd.read_csv(main_path + "tmp/raw_tweets.csv", header=0)
    # We now add a clean_text column to our df frame
    df['clean_text'] = df.apply(lambda x: clean_text(x['text']), axis=1)
    # We also add a clean_text_with_stopwords as keeping stopwords could be
    # useful for our ngram representation
    df['clean_text_with_stopwords'] = df.apply(lambda x: clean_text(x['text'], False), axis=1)
    # Apply this to the source column
    df['source'] = df["source"].apply(lambda x: get_source(x))
    # Let's also get rid of the id_str field, as it is pretty useless
    df.drop('id_str', axis=1, inplace=True)
    # Saving the data
    df.to_json(main_path + 'data/clean_data/{}.json'.format(clean_data_name), orient="records")
    df.to_csv(main_path + './data/clean_data/{}.csv'.format(clean_data_name), index=False)