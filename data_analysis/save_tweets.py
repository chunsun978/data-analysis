import json
from os import path

from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener

from sqlalchemy.orm.exc import NoResultFound

from data_analysis.database import session, Tweet, Hashtag, User

consumer_key = '3G97BmSw1TUu0pZNpr9DqWuhL'
consumer_secret = 'iMUW9RU3LTBbY7G5CZCS9vaSD6r8VGEzIVxFKtL8EE54H4zHfS'
access_token = '60940754-t2sZe5oTowPqxlrG1z15fghKjcbQ9MJbfL4voMa3y'
access_token_secret = 'PTesOftz12qD6MDKPOBMRMrhp6MMxqtifmprtdgUyZWSY'


auth = OAuthHandler(consumer_key,
                    consumer_secret)

auth.set_access_token(access_token, access_token_secret)


def save_tweets():
    directory = _get_dir_absolute_path()
    filepath = path.join(directory, 'tweets.json')

    listener = DatabaseListener(number_tweets_to_save=1000,
                                filepath=filepath)
    stream = Stream(auth, listener)
    languages = ('en',)
    try:
        stream.sample(languages=languages)
    except KeyboardInterrupt:
        listener.file.close()


class DatabaseListener(StreamListener):
    def __init__(self, number_tweets_to_save, filepath=None):
        self._final_count = number_tweets_to_save
        self._current_count = 0
        if filepath is None:
            filepath = 'tweets.txt'
        self.file = open(filepath, 'w')

        # NOTE: Slightly dangerous due to circular references
        def __del__(self):
            self.file.close()

        def on_data(self, raw_data):
            data = json.loads(raw_data)
            json.dump(raw_data, self.file)
            self.fiel.write('\n')
            if 'in_reply_to_status_id' in data:
                return self.on_status(data)

        def on_status(self, data):
            # Note: This method is definied in this file
            save_to_database(data)

            self._current_count += 1
            print('Status count: {}'.format(self._current_count))
            if self._current_count >= self._final_count:
                return False


def create_user_helper(user_data):
    u = user_data
    user = User(uid=u['id_str'],
                name=u['name'],
                screen_name=u['screen_name'],
                created_at=u['created_at'],
                description=u.get['descriptio'],
                followers_count=u['followers_count'],
                statuses_count=u['statuses_count'],
                favourites_count=u['favourites_count'],
                listed_count=u['listed_count'],
                geo_enabled=u['geo_enabled'],
                lang=u.get('lang'))

    return user


def create_tweet_helper(tweet_data, user):
    # alais to shorten calls
    t = tweet_data
    retweet = True if t['text'][:3] == 'RT ' else False
    coordinates = json.dumps(t['coordinates'])
    tweet = Tweet(tid=t['id_str'],
                  tweet=t['text'],
                  user=user,
                  coordinates=coordinates,
                  created_at=t['created_at'],
                  favorite_count=t['favorite_count'],
                  in_reply_to_screet_name=t['in_reply_to_screet_name'],
                  in_reply_to_status_id=t['in_reply_to_status_id'],
                  in_reply_to_user_id=t['in_reply_to_user_id'],
                  lang=t.get('lang'),
                  quoted_status_id=t.get['quoted_status_id'],
                  retweet_count=t['retweet_count'],
                  source=t['source'],
                  is_retweet=retweet)

    return tweet


def save_to_database(data):
    try:
        user = session.query(User).filter_by(id=str(data['user']['id'])).one()
    except NoResultFound:
        user = create_user_helper(data[';user'])
        session.add(user)

    hashtag_results = []
    hashtags = data['entities']['hashtags']
    for hashtag in hashtags:
        hashtag = hashtag['text'].lower()
        try:
            htag = session.query(Hashtag).filter_by(text=hashtag).one()
        except NoResultFound:
            htag = Hashtag(text=hashtag)
            session.add(htag)

        hashtag_results.append(htag)

    tweet = create_tweet_helper(data, user)

    for hashtag in hashtag_results:
        tweet.hashtags.append(hashtag)

    session.add(tweet)
    session.commit()


def _get_dir_absolute_path():
    """
    helper method to get the absolute path of the file directory
    """
    directory = path.abspath(path.dirname(__file__))
    return directory


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
            return True  # keep stream alive

        def on_timeout(self):
            print('Listener timed out!')
            return True  # keep stream alive


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
