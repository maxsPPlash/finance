import tweepy
from tweepy import OAuthHandler, Stream, StreamListener

access_token='1378102406693675009-akhaJ9gdAa0VdVZXUtuhMCNRPOtVFU'
access_secret='JvpykChNr7jr6IVeIog5hPlSSfHKgUtG7AQGACbFYN9IM'
consumer_key = 'qiXSMzir0JE0zXOQIdQoasumX'
consumer_secret = 'K9721VTgDZJWWn6rqQwAmGYSfUVv60ZJwmlYgA6HPwcL1tPnq0'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

class MyListener(StreamListener):
    def on_status(self, status):
        try:
            if status.user.followers_count > 5000:
                print('%s (%s at %s, followers: %d)' % (status.text, status.user.screen_name, status.created_at, status.user.followers_count))
                return True
        except BaseException as e:
            print("Error on_status: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['The'])