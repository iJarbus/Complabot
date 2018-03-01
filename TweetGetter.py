from tweepy.streaming import StreamListener
from tweepy import Stream
import tweepy
import json
import authenticator

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
        self.TwitAuthenticator = authenticator.Authenticator.TwitAuthenticator()
        self.AyAuthenticator = authenticator.Authenticator.AyAuthenticaor()

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
        tweet = json.loads(data)
        try:
            print(tweet['text'])
            print(tweet['user']['name'])
        except KeyError:
            print("Some data is missing, skip it")
        if self.counter < self.maxTweets:
            print(self.counter)
            print("-------------------------------------------------------")
            self.counter += 1
            return True
        else:
            print("All tweets gathered")
            return False

    def on_error(self, status):
        print(status)

    def streamTweets(self):

        stream = Stream(self.TwitAuthenticator, self)
        stream.filter(languages=[self.languageToTarget], track=self.words)


