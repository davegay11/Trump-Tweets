import pandas as pd
import numpy as np
import os
import time
import datetime
import sys
from model_word2vec import create_model
from vis_wordcloud import generate_wordcloud
from tfidf import similarity_to_trump
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#main_path = os.path.join(os.path.dirname(__file__), '../')
main_path = os.path.join(os.path.dirname('pastTrump.py'), '../')
filepath = 'data/clean_tweets.csv'
outputPath = 'data/segmented_tweets/'
announcementDate = datetime.datetime(2015,6,15)
electionDate = datetime.datetime(2016,11,8)

#Partitions tweet data based on time separators
#segments: number of time partitions based on the start and end index
#dates: list of specified date separators
def compareSelf(segments=0, dates=[announcementDate]):
    #Reads in Trump's cleaned tweet data
    filename = main_path + filepath
    df = pd.read_csv(filename, header=0)
    #converts/sorts data into a useable format
    data = zip([__convertDate(date) for date in df['created_at']], df['clean_text'], df['clean_text'])
    
    data.sort()
    dateTime = [d[0] for d in data]
    #Creates the segment indexes for the data
    separators = []
    minDate = min(dateTime)
    separators.append(__findSplitIndex(dateTime, minDate)) 
    maxDate = max(dateTime)
    separators.append(__findSplitIndex(dateTime, maxDate))
    #loads in the specified dates
    for date in dates:
        separators.append(__findSplitIndex(dateTime, date))
    #loads in the time segment dates
    if segments > 0:
        span = (maxDate - minDate).days
        segmentWidth = span/segments
        for i in range(1, segments):
            timeEndSlice = minDate + datetime.timedelta(i * segmentWidth)
            separators.append(__findSplitIndex(dateTime, timeEndSlice))
    separators.sort()
    #print separators
    #Use separator indices to segment data
    segmentedData = []
    for index in range(len(separators)-1):
        startDate = separators[index]
        endDate = separators[index+1]
        segment = (startDate, endDate, data[startDate:endDate])
        segmentedData.append(segment)
    #Write segmented Data to different files
    for i in range(len(segmentedData)):
        dataPath = main_path + outputPath + str(i) + "_timeSlice.csv"
        with open(dataPath, 'w') as f:
            f.write("date,clean_text,text,\n")
            for line in segmentedData[i][2]:
                f.write(str(line[0]) + "," + str(line[1]) + ',' + line[2] + ',\n')
            f.close()
            #Run sentiment analysis on each timeSlice
            sid = SentimentIntensityAnalyzer()
            df = pd.read_csv(dataPath)
            df['compound_polarity'] = df['clean_text'].apply(lambda x: sid.polarity_scores(str(x))['compound'])
            df.to_csv(dataPath, index=False,line_terminator="\n")
    return segmentedData

#Converts the date from text to a datetime object
#date: date in the csv's format
def __convertDate(date):
    monthText = ['Jan','Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    dateComponents = date.split(' ')
    day = int(dateComponents[2])
    month = monthText.index(dateComponents[1]) + 1
    year = int(dateComponents[5])
    return datetime.datetime(year, month, day)
    
    
#finds the most recent tweet's index given a date
#data: list of tweet datetimes
#date: date to split on
def __findSplitIndex(data, date):
    dayCount = 0
    findIndex = -1
    #Search backwards 1 day at a time from the given start date
    while findIndex == -1 and dayCount < 356:
        end = date - datetime.timedelta(dayCount)
        if end in data:
            findIndex = data.index(end)
        dayCount += 1
    return findIndex

if __name__ == "__main__":
    compareSelf()
    #compareSelf(10, [])
    for i in range(2):
        dataPath = main_path + outputPath + str(i) + '_timeSlice.csv'
        #Creates word clouds of each timeSlice
        generate_wordcloud(dataPath, str(i) + '_sliceWordCloud.png')
        #Creates word2vec models of each timeSlice
        create_model(dataPath, main_path + 'models/word2vec/' + str(i) + '_sliceWord2Vec.bin', min_word_count=5, logging=False)
        #TF-IDF analysis will be run through main
        
        
    