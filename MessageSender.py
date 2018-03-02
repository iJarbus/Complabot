import authenticator
import csv
import tweepy

class MessageSender():
    """
    This is the class that handles going through the .csv file and finding the saddest person and tweeting them
    """

    def __init__(self, CandidatesFile = "tweets.csv"):
        self.CandidatesFile = CandidatesFile
        self.twitterAPIObject = tweepy.API(authenticator.Authenticator("keys.txt").TwitAuthenticator())

    def SendTweet(self):
        """
        This is the function that calls the other function to send out the tweet to the saddest person
        :return:
        """
        theImage = "Kitten.jpg"
        theSadPerson = self.SaddestUserFinder()
        self.TweetSaddestPerson(theSadPerson, theImage)

    def SaddestUserFinder(self):
        """
        This function goes through the .csv file and finds the user with the highest score on the emotion
        :return: a string with the username of the saddest user or None if there is no users
        """
        #Try to open the file
        try:
            f = open(self.CandidatesFile, 'r')
            reader = csv.reader(f)
            People = list(reader)
        except FileNotFoundError:
            print("There is no file with users in it")
            return False

        try:
            #initilising varible to first entry
            SaddestPerson = People[0]
        except IndexError:
            print("No sad people")
            return False

        #loop through and find the person with the highest emotion score
        for person in People:
            if person[1] > SaddestPerson[1]:
                SaddestPerson = person

        return SaddestPerson[0]

    def TweetSaddestPerson(self, SadPerson, image):
        """
        This is the function that tweets a person a message along with an image
        :param SadPerson: This is the twitter user name of the person to be tweeted at
        :return: None
        """
        message = "Hi @" + SadPerson + " , I'm a twitter bot trying to help cheer people up. Remember there is always" \
                                       " happiness in the world, you need only seek it out"

        self.twitterAPIObject.update_with_media(image, status=message)