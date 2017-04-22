#!/usr/bin/env bash

usernames=("realdonaldtrump" "hillaryclinton" "govpencein" "speakerryan" "senjohnmccain" "kellyannepolls" 
"marcorubio" "sarahpalinusa" "seanspicer" "seanspicer" "seanspicer")
years=(2009 2010 2011 2012 2013 2014 2015 2016 2017)

# For each username we collect all of the tweets and save them to a file
for username in "${usernames[@]}"; do
  echo "";
  echo " Collecting Tweets for $username ...";
  echo "";
  mkdir -p "./data/raw_json/$username";
  for year in "${years[@]}"; do
    echo "=============================$year=============================";
    url="http://www.trumptwitterarchive.com/data/$username/$year.json";
    # echo $url
    curl -s $url > "./data/raw_json/$username/tweets_$year.json";
  done
done

echo ""
echo "All done!!!"
