"""
Create a wordcloud for an image, optionally providing a mask
"""

from wordcloud import WordCloud
from PIL import Image
import pandas as pd
import numpy as np

def generate_wordcloud(filename, name):
    ''' Generate a wordcloud given a filename and a name '''
    df = pd.read_csv(filename, header=0)
    text = df['clean_text'].str.cat(sep=' ')
    wordcloud = WordCloud().generate(text)
    wordcloud.to_file(os.path.join(d, main_path + 'img/wordcloud_{}.png'.replace(name)))
