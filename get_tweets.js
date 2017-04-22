const http = require('http');
const fs = require('fs');

const years = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
const tweets = []

for (year of years) {
  const url = `http://www.trumptwitterarchive.com/data/hillaryclinton/${year}.json`
  http.get(url, function(res) {
    let body = '';
    res.on('data', function(chunk){
        body += chunk;
    });
    res.on('end', function(){
      const json_tweets = JSON.parse(body);
      tweets.concat(json_tweets);
    });
  }).on('error', function(e) {
    console.log('Got error: ' + e.message);
  });
}

fs.writeFile('hillary_tweets.json', JSON.stringify(tweets), (err) => {
  console.log('Error writing file')
})
