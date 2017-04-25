import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from n_gram import gen_ngram, sort_ngram, save_ngram
import numpy as np
import pandas as pd
import os

'''
import numpy as np
import json
import sys
'''

main_path = os.path.join(os.path.dirname('timeSliceVisuals.py'), '../')
img_path = '/img/charts/'

def generateBarCharts(ngram, name):
    x = [n[0] for n in ngram]#possible generate all of them 
    y = [n[1] for n in ngram]
    x_axis = np.arange(len(x))
    print x,y
    fig = plt.figure()    
    plt.bar(x_axis, y, label='ngram1')
    plt.xticks(x_axis, x)
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.title('nGram test')
    plt.legend()
    plt.savefig(main_path + img_path + name)
    plt.close(fig)  


if __name__ == "__main__":
    cleanTxt = pd.read_csv(main_path + "/data/segmented_tweets/0_timeSlice.csv", header=0)
    trump_grams_1 = gen_ngram(cleanTxt,1,"clean_text")
    ngram = sort_ngram(trump_grams_1)[:20]
    generateBarCharts(ngram, 'trumpGram.png')
    

    