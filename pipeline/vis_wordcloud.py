"""
Create a wordcloud for an image, optionally providing a mask
"""

from wordcloud import WordCloud, get_single_color_func
from PIL import Image
import os
import pandas as pd
import numpy as np

main_path = os.path.join(os.path.dirname(__file__), '../')
wordcloud_path = main_path + 'img/wordclouds/'

def single_color_func(color):
    def color_func(word=None, font_size=None, position=None,
                          orientation=None, font_path=None, random_state=None):
        return color
    return color_func

black_color_func = single_color_func('rgb(0, 0, 0)')

def generate_wordcloud(filename, name, color=False):
    ''' Generate a wordcloud given a filename and a name '''
    if not os.path.exists(wordcloud_path):
        os.makedirs(wordcloud_path)
    df = pd.read_csv(filename, header=0)
    text = df['clean_text'].str.cat(sep=' ')
    stopwords = set([name]) #ignore the twitter handle when generating
    wordcloud = None
    if color:
        wordcloud = WordCloud(
            stopwords=stopwords, # Words to ignore when generating the wordcloud
            collocations=False, # Don't include bigrams
            #  relative_scaling=1.0, # Don't take into account relative importance
            scale=4.0 # Scaling the image to make it larger
        )
    else:
        wordcloud = WordCloud(
            stopwords=stopwords, # Words to ignore when generating the wordcloud
            prefer_horizontal=1.0, # only use horizontal words
            background_color="#ffffff", # By default the background color is black
            collocations=False, # Don't include bigrams
            #  relative_scaling=1.0, # Don't take into account relative importance
            color_func=black_color_func, # A simple all-black color function
            #  color_func=get_single_color_func("#000"),
            scale=4.0 # Scaling the image to make it larger
        )
    # Generate the wordcloud and save to a file
    wordcloud = wordcloud.generate(text)
    wordcloud.to_file(wordcloud_path + 'wordcloud_{}.png'.format(name))
