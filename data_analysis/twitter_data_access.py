import json

from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener

consumer_key = '3G97BmSw1TUu0pZNpr9DqWuhL'
consumer_secret = 'iMUW9RU3LTBbY7G5CZCS9vaSD6r8VGEzIVxFKtL8EE54H4zHfS'
access_token = '60940754-t2sZe5oTowPqxlrG1z15fghKjcbQ9MJbfL4voMa3y'
access_token_secret = 'PTesOftz12qD6MDKPOBMRMrhp6MMxqtifmprtdgUyZWSY'


auth = OAuthHandler(consumer_key,
                    consumer_secret)

auth.set_access_token(access_token, access_token_secret)


class PrintListener(StreamListener):
        def on_status(self, status):
            if not status.text[:3] == 'RT ':
                print(status.text)
                print(status.author.screen_name,
                      status.created_at,
                      status.source,
                      '\n')

        def on_error(self, status_code):
            print("Error code: {}".format(status_code))
            return True     # keep stream alive

        def on_timeout(self):
            print('Listener timed out!')
            return True     # keep stream alive


def print_to_terminal():
            listener = PrintListener()
            stream = Stream(auth, listener)
            languages = ('en',)
            stream.sample(languages=languages)


def pull_down_tweets(screen_name):
    api = API(auth)
    tweets = api.user_timeline(screen_name=screen_name, count=200)
    for tweet in tweets:
        print(json.dumps(tweet._json, indent=4))


if __name__ == '__main__':
    # print_to_terminal()
    pull_down_tweets(auth.username)
