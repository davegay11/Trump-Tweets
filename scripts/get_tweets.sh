#!/usr/bin/env bash

# Bash script to pull all the tweets down that were stored in the trump
# twitter archive. Make sure to run this file from the ROOT of the project
# like: 
# > ./scripts/get_data.sh

# Get all of the accounts in the trump twitter archive
echo "Getting the accounts"
usernames_str=$(curl -s "http://www.trumptwitterarchive.com/data/accounts.json" | grep '"account"' | sed 's/"account": //g' | sed 's/    "//g' | sed 's/"//g' | tr "\n" " ")
# Parse the usernames into a bash list to iterate over
usernames=(${usernames_str//,/ })

# All the years that were available
years=(2009 2010 2011 2012 2013 2014 2015 2016 2017)

# make sure the raw_json folder is created
mkdir -p "./data/raw_json"

# make sure the clean_data folder is created
mkdir -p "./data/clean_data"

# make sure the tf_idf folder is created
mkdir -p "./data/tf_idf"

# For each username we collect all of the tweets and save them to a file
for username in "${usernames[@]}"; do
  echo ""
  echo " Collecting Tweets for $username ..."
  echo ""
  mkdir -p "./data/raw_json/$username"
  for year in "${years[@]}"; do
    echo "=============================$year============================="
    url="http://www.trumptwitterarchive.com/data/$username/$year.json"
    # echo $url
    curl -s $url > "./data/raw_json/$username/tweets_$year.json"
  done
done

echo ""
echo "All done!!!"
