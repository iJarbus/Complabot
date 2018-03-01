from aylienapiclient import textapi
from tweepy import OAuthHandler

class Authenticator():
    """
    This is a class that handles all the authentication for logging into the Aylien api as well as the twitter API
    """
    def __init__(self, fileLocation):
        """
        The initilisation function
        :param fileLocation: This is the location of the text file that houses the API keys, it should be in the format:
        Consumer Key (API Key)(Twitter)
        Consumer Secret (API Secret)(Twitter)
        Access Token(Twitter)
        Access Token Secret(Twitter)
        App ID(Aylien)
        Key(Aylien)
        """
        fileLocation
        try:
            f = open(fileLocation)
        except FileNotFoundError:
            print("the file does not exsist")
        self.apiKeys = []
        for line in f:
            self.apiKeys.append(line)
        if len(self.apiKeys) != 6:
            print("Keys not stored in file correctly, please make sure they are in the form\n"
                  "Consumer Key (API Key)(Twitter)\n"
                  "Consumer Secret (API Secret)(Twitter)\n"
                  "Access Token(Twitter)\n"
                  "Access Token Secret(Twitter)\n"
                  "App ID(Aylien\n"
                  "Key(Aylien)\n")

    def AyAuthenticaor(self):
        """
        This is a function that creates an ayClient instance and authenticates it
        :return: returns an authenticated ayClient object
        """
        try:
            ayClient = textapi.Client(self.apiKeys[4], self.apiKeys[5])
        except Exception:
            print("Something went wrong trying to authenticate with Aylien")
        return ayClient

    def TwitAuthenticator(self):
        """
        This is a function that creates and authentication object for the Twitter API
        :return: and authentication obect for the Twitter API
        """
        try:
            auth = OAuthHandler(self.apiKeys[0], self.apiKeys[1])
            auth.set_access_token(self.apiKeys[2], self.apiKeys[3])
        except Exception:
            print("Something went wrong trying to authenticate with Twitter")

        return auth