import tweepy
from textblob import TextBlob
import sys
import csv

consumer_key = '<your key>'
consumer_secret = '<your key>'

access_token = '<your token>'
access_token_secret = '<your token>'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Retrieve tweets
#public_tweets = api.search('modi')

# to get tweets having 2 labels and between a timeline
name_of_debate = 'UP'
candidate = 'modi'
since_date = "2017-01-01"
until_date = "2017-04-20"
this_candidate_tweets = api.search(q=[name_of_debate, candidate], count=100, since = since_date, until=until_date)

with open('%s_tweets.csv' % candidate, 'w', newline='\n', encoding='utf-8') as  f:

	writer = csv.DictWriter(f, fieldnames=['Tweet', 'Sentiment'])
	writer.writeheader()
	for tweet in this_candidate_tweets:
		text = tweet.text
		
		#Cleaning tweet
		cleanedtext = ' '.join([word for word in text.split(' ') if len(word) > 0 and word[0] != '@' and word[0] != '.' and word[0] != '#' and 'http' not in word and word != 'RT'])
		
		analysis = TextBlob(cleanedtext)

		sentiment = analysis.sentiment.polarity
		if sentiment >= 0:
			polarity = 'Positive'
		else:
			polarity = 'Negative'

		#print(cleanedtext, polarity)

		writer.writerow({'Tweet':text, 'Sentiment':polarity})
