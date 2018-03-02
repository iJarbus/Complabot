import TweetGetter
import MessageSender
import time
from http.client import IncompleteRead

Tweeter = TweetGetter.TweetGetter("words.txt", 30)
try:
    Tweeter.streamTweets()
except IncompleteRead:
    print("incom")
    pass

while not Tweeter.DoneStreaming:
    time.sleep(30)

MessageSenderController = MessageSender.MessageSender()
MessageSenderController.SendTweet()


