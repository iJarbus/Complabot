from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
from aylienapiclient import textapi

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="VaW0e25LAxzB2hHcshSpMs8LM"
consumer_secret="MFAZnn0vEqCFKHfZXIlBjm7ll1HN7fcRZVuCXLvenOTMBrMbFs"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="938088146-JI9rSWcR6WiA6TPdmAgonv3tOTfEmJnUKveZA2J2"
access_token_secret="J84n9wfsfWwLvATnldiYpi1oRaIh53Xg9gQmNIOehxiOQ"

ayClient = textapi.Client("bd9f639e", "b94d0f98405802ec37c080ac84b03267")

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, maxTweets = 100):
        self.counter = 0
        self.maxTweets = maxTweets


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

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    with open('words.txt') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    stream = Stream(auth, l)
    stream.filter(languages=['en'], track=content)

    #api = tweepy.API(auth)
    #api.update_with_media("kitten.jpg", status="test")

