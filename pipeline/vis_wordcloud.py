"""
Create a wordcloud for an image, optionally providing a mask
"""

from wordcloud import WordCloud
from PIL import Image
import os
import pandas as pd
import numpy as np

main_path = os.path.join(os.path.dirname(__file__), '../')
wordcloud_path = main_path + 'img/wordclouds/'

def generate_wordcloud(filename, name):
    ''' Generate a wordcloud given a filename and a name '''
    if not os.path.exists(wordcloud_path):
        os.makedirs(wordcloud_path)
    df = pd.read_csv(filename, header=0)
    text = df['clean_text'].str.cat(sep=' ')
    stopwords = set([name]) #ignore the twitter handle when generating
    wordcloud = WordCloud(stopwords=stopwords).generate(text)
    wordcloud.to_file(wordcloud_path + 'wordcloud_{}.png'.format(name))
