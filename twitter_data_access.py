from tweepy import OAuthHandler 
from tweepy import Stream
from tweepy.streaming import StreamListener 

consumer_key = '3G97BmSw1TUu0pZNpr9DqWuhL'
consumer_secret = 'iMUW9RU3LTBbY7G5CZCS9vaSD6r8VGEzIVxFKtL8EE54H4zHfS'
access_token = '60940754-t2sZe5oTowPqxlrG1z15fghKjcbQ9MJbfL4voMa3y'
access_token_secret = 'PTesOftz12qD6MDKPOBMRMrhp6MMxqtifmprtdgUyZWSY'


auth = OAuthHandler (consumer_key, 
                     consumer_secret)

auth.set_access_token(access_token, access_token_secret)

class PrintListener(StreamListener):
        def on_status(self, status):
            print(status.text)
            print(status.author.screen_name, 
                  status.created_at, 
                  status.source, 
                  '\n')

        def on_error(self, status_code):
            print("Error code: {}".format(status_code))
            return True #keep stream alive

        def on_timeout(self):
            print('Listener timed out!')
            return True #keep stream alive

def print_to_terminal():
            listener = PrintListener()
            stream = Stream(auth, listener)
            stream.sample()


if __name__ == '__main__':
    print_to_terminal()
