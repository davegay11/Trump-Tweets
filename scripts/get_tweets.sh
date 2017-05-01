#!/usr/bin/env bash

# Bash script to pull all the tweets down that were stored in the trump
# twitter archive. Make sure to run this file from the ROOT of the project
# like: 
# 
#   ./scripts/get_tweets.sh
# 
# You can additionally pass in the user as a parameter to only retrieve tweets
# for a specified handle. For example:
#
#   ./scripts/get_tweets.sh realscottpruitt
# 
# Author: Zachary Marion


if [ -z "$1" ]; then
  echo "No user specified, getting all users from the Trump Twitter Archive"
  # Get all of the accounts in the trump twitter archive
  usernames_str=$(curl -s "http://www.trumptwitterarchive.com/data/accounts.json" | \
    grep '"account"' | \
    sed 's/"account": //g' | \
    sed 's/    "//g' | \
    sed 's/"//g' | \
    tr "\n" " ")
  # Parse the usernames into a bash list to iterate over
  usernames=(${usernames_str//,/ })
else
  usernames=("$1")
fi

# All the years that were available
years=(2009 2010 2011 2012 2013 2014 2015 2016 2017)

# make sure the raw_json folder is created
mkdir -p "./data/raw_json"

# make sure the clean_data folder is created
mkdir -p "./data/clean_data"

# make sure the tf_idf folder is created
mkdir -p "./data/tf_idf"

# make sure the img folder exists
mkdir -p "./img"

# For each username we collect all of the tweets and save them to a file
for username in "${usernames[@]}"; do
  echo ""
  echo " Collecting Tweets for $username ..."
  echo ""
  mkdir -p "./data/raw_json/$username"
  for year in "${years[@]}"; do
    echo "=============================$year============================="
    url="http://www.trumptwitterarchive.com/data/$username/$year.json"
    curl -s $url > "./data/raw_json/$username/tweets_$year.json"
  done
  # Having some issues with getting booted from the site so we sleep for a little
  # while in between each request. You can remove and see if you have the same
  # issue
  sleep $((1 + RANDOM % 5))
done

# Move the baseline tweets to the same place as the others, in the same format
# to make the cleaning process easier
baseline_tweets="./data/baseline_tweets.json"
if test -f $baseline_tweets; then
  echo "Moving baseline tweets"
  mkdir -p ./data/raw_json/baseline_tweets
  mv ./data/baseline_tweets.json ./data/raw_json/baseline_tweets/
fi

berniefolder="./data/raw_json/berniesanders"
berniefile="./data/raw_json/berniesanders/berniesanders.json"
mkdir -p $berniefolder
if [ ! -f $berniefile ]; then
  echo "Moving bernie sanders to raw_json"
  cp "./andrews_stuff/berniesanders.json" $berniefile 
fi

echo ""
echo "All done!!!"
