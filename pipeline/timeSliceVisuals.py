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

def generateBarCharts(ngram, filename, title='Trump ngram', xLabel='Word', yLabel='Frequency', barLabel='ngram1'):
    x = [n[0] for n in ngram]#possible generate all of them 
    y = [n[1] for n in ngram]
    x_axis = np.arange(len(x))
    print x,y
    fig = plt.figure()    
    plt.bar(x_axis, y, label=barLabel)
    plt.xticks(x_axis, x, fontsize = 8)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=75)
    fig.tight_layout()
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.savefig(main_path + img_path + filename)
    plt.close(fig)
    

def computeAverageSentiment(word, df, threshhold=.1):
    count = 0.0
    totalSentiment = 0.0
    for text,sentiment in zip(df["clean_text"],df["compound_polarity"]):
        if word in text and abs(sentiment) > threshhold:
            totalSentiment += sentiment
            count += 1
    if count == 0.0:
        return count
    print word,count
    return totalSentiment/count

def plotSentimentOverTime(sentiments, filename, title="Trump's sentiments over time", xLabel='Time', yLabel='Sentiment'):
    fig = plt.figure()
    for key,val in sentiments.iteritems():
        x = range(len(val))
        y = val
        plt.plot(x, y, label=key)
    fig.tight_layout()
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.savefig(main_path + img_path + filename)   
    plt.close()
    

if __name__ == "__main__":
    sentiments = {"hillary":[], "obama":[], "immigra":[]}
    for i in range(2):
        dataPath = "/data/segmented_tweets/" + str(i) + "_timeSlice.csv"
        cleanTxt = pd.read_csv(main_path + dataPath, header=0)
        trump_grams_1 = gen_ngram(cleanTxt,1,"clean_text")
        ngram = sort_ngram(trump_grams_1)[:20]
        generateBarCharts(ngram, str(i) + '_trumpGram.png')
        for key,val in sentiments.iteritems():
            val.append(computeAverageSentiment(key, cleanTxt))
        print sentiments
    plotSentimentOverTime(sentiments, 'trumpSentiments')
            
    

    