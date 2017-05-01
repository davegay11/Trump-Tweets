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
# for username in "${usernames[@]}"; do
  # echo ""
  # echo " Collecting Tweets for $username ..."
  # echo ""
  # mkdir -p "./data/raw_json/$username"
  # for year in "${years[@]}"; do
    # echo "=============================$year============================="
    # url="http://www.trumptwitterarchive.com/data/$username/$year.json"
    # curl -s $url > "./data/raw_json/$username/tweets_$year.json"
  # done
  # # Having some issues with getting booted from the site so we sleep for a little
  # # while in between each request. You can remove and see if you have the same
  # # issue
  # sleep $((1 + RANDOM % 5))
# done

# Other users that were not from the Trump Twitter Archive. All you have to do
# is place the json file in the ./data directory and add the name of the file
# (which should be the twitter handle if there is one) in the to array below:
other_usernames=("berniesanders" "baseline_tweets")

# Iterate over each user we want to add and copy the file into raw_json
for username in "${other_usernames[@]}"; do
  file="./data/$username.json"
  if test -f $file; then
    echo "Copying $username.json into the raw_json folder"
    mkdir -p "./data/raw_json/$username"
    cp $file "./data/raw_json/$username/"
  fi
done

echo ""
echo "All done!!!"
