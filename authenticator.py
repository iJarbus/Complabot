import watson_developer_cloud
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
        try:
            f = open(fileLocation)
        except FileNotFoundError:
            print("the file does not exsist")
        self.apiKeys = []
        for line in f:
            self.apiKeys.append(line)
        #Strip the new line charecters from end
        self.apiKeys = [x.strip() for x in self.apiKeys]
        if len(self.apiKeys) != 6:
            print("Keys not stored in file correctly, please make sure they are in the form\n"
                  "Consumer Key (API Key)(Twitter)\n"
                  "Consumer Secret (API Secret)(Twitter)\n"
                  "Access Token(Twitter)\n"
                  "Access Token Secret(Twitter)\n"
                  "App ID(Aylien\n"
                  "Key(Aylien)\n")

    def WatsonToneAuth(self):
        """
        creates an authenticated ToneAnalyzer for the IBM Watson cloud API
        :return: Autherised Tone Analyser
        """
        tone_analyzer = watson_developer_cloud.ToneAnalyzerV3(
            version='2017-09-21',
            username=self.apiKeys[4],
            password=self.apiKeys[5]
        )
        return tone_analyzer

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