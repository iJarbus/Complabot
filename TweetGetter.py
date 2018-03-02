from tweepy.streaming import StreamListener
from tweepy import Stream
import tweepy
import json
import authenticator
import csv

class TweetGetter(StreamListener):
    """
    This is a class that handles getting tweets from the twitter api via the stream method, it is saving them to a csv
    file.
    """

    def __init__(self, wordsFile, maxTweets = 100):
        """
        Initialision function
        :param maxTweets: This is the number of tweets to be analysed per job
        """
        self.counter = 0
        self.maxTweets = maxTweets
        self.Authenticator = authenticator.Authenticator("keys.txt")
        self.TwitAuthenticator = self.Authenticator.TwitAuthenticator()
        self.WatonsAuthenticator = self.Authenticator.WatsonToneAuth()
        self.tweetFile = open("tweets.csv", 'w')

        """
        Why the words file is needed:
        There seems to be a bug in the Twitter API where if you filter by a langauge you have to also filter by words
        since for this case we don't want to do this to try to get the most random assortment of tweets we'll be
        matching any tweet that has one or more of the top 500 most common English words, this should mean that we
        match almost any tweet in English.
        """
        with open(wordsFile) as f:
            self.words = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        self.words = [x.strip() for x in self.words]
        self.languageToTarget = "en" #This must be a ISO 639-1 language code, Wikipedia has a good list.

    def on_data(self, data):
        """
        This is the function that handles what is done when a tweet is streamed in
        :param data: This is the tweet, it is in the form of a JSON object, the structure of which is defined at:
        https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json
        :return: True or False, True if the streaming should continue, False to stop it
        """
        tweet = json.loads(data)
        try:
            #if the tweet is a retweet skip over it.
            if tweet['text'][0:2] == "RT":
                return True
            print(tweet['text'])
        except KeyError:
            #if we can't access all the data just skip over it and request again without incrementing counter
            return True
            pass
        try:
            TweetText = tweet['extended_text']['full_text']
        except KeyError:
            TweetText = tweet['text']

        #get the tone analysis from Watson
        Tone = self.WatonsAuthenticator.tone(TweetText, content_type='text/plain')

        #loop through the returned emotions and if sadness store the data in the .csv file
        try:
            for emotions in Tone['document_tone']['tones']:
                if emotions['tone_id'] == "sadness":
                    row = tweet['user']['screen_name'] + "," + str(emotions['score']) + "\n"
                    self.tweetFile.write(row)
        #If there is a key error just move on to the next tweet
        except KeyError:
            return True

        #This is the control logic for how many tweets to get
        if self.counter < self.maxTweets:
            self.counter += 1
            return True
        else:
            print("All tweets gathered")
            return False

    def on_error(self, status):
        print(status)

    def streamTweets(self):
        """
        This is a function that streams tweets using the twitter api, the logic of what is done with each tweet is
        defined in the on_data function.
        :return: None
        """
        stream = Stream(self.TwitAuthenticator, self)
        stream.filter(languages=[self.languageToTarget], track=self.words)


