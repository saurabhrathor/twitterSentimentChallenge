import tweepy
from textblob import TextBlob
import sys
import csv
import numpy as np
import operator

consumer_key = 'FgBzwRqpu6gKsPIdSS9iqnhHK'
consumer_secret = 'rEwItQOBkcVoJg7xhY9Vpi6NP8lQhvFFiZZD84GsiyIOhunSAP'

access_token = '755811601362456576-osQAubuToh1mkhMgudi2uXDUcNTDHv3'
access_token_secret = 'FNAPZnWImDO7xJvtMVPU23vCjKxCETIRoRe9nQedvJ4dm'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Retrieve tweets
#public_tweets = api.search('modi')

name_of_debate = 'election'
candidates_names = ['Modi', 'Sonia', 'Rahul', 'Kejriwal', 'Mulayam']
since_date = "2017-01-01"
until_date = "2017-04-20"

all_polarities = dict()
for candidate in candidates_names:
	this_candidate_polarities = []
	# to get tweets having 2 labels and between a timeline	
	this_candidate_tweets = api.search(q=[name_of_debate, candidate], count=100, since = since_date, until=until_date)
	
	with open('%s_tweets.csv' % candidate, 'w', newline='\n', encoding='utf-8') as  f:
		f.write('tweet,sentiment_label\n')
		#writer = csv.DictWriter(f, fieldnames=['Tweet', 'Sentiment'])
		#writer.writeheader()
		for tweet in this_candidate_tweets:
			text = tweet.text
			#Cleaning tweet
			cleanedtext = ' '.join([word for word in text.split(' ') if len(word) > 0 and word[0] != '@' and word[0] != '.' and word[0] != '#' and 'http' not in word and word != 'RT'])
			
			analysis = TextBlob(cleanedtext)
			
			sentiment = analysis.sentiment.polarity
			this_candidate_polarities.append(analysis.sentiment[0])
			if sentiment >= 0:
				polarity = 'Positive'
			else:
				polarity = 'Negative'

			#print(cleanedtext, polarity)
			f.write('%s,%s\n' % (tweet.text.encode('utf8'), polarity))
			
	all_polarities[candidate] = np.mean(this_candidate_polarities)

#Step bonus - Print a Result
sorted_analysis = sorted(all_polarities.items(), key=operator.itemgetter(1), reverse=True)
print("Mean Sentiment Polarity in descending order :")
for candidate, polarity in sorted_analysis:
	print('%s : %0.3f' % (candidate, polarity))
