#!/usr/bin/python3
# Fillename: TwitterStreamDownload.py
'''
Created on 2014-12-1

@author: thewingter
Access the twitter stream api, download and save the tweets.
'''
import traceback
import tweepy
from tweepy.streaming import StreamListener
import time
from tweepy.models import Status
import csv
import logging
from tweepy.utils import import_simplejson
from TwitterStream import NewStream
json = import_simplejson()

class Save2FileListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    
    This is a listener that save received tweets to a file.

    """
    def __init__(self, api=None):
        StreamListener.__init__(self, api=api)
        ts = time.strftime("./data/%Y%m%d%H%M")
        self.statusf = open(ts+'_status.csv','w',newline='')
        self.statusw = csv.writer(self.statusf)
        self.statusw.writerow(['id', 'created_at', 'coordinates',\
                               'hashtags', 'user_mentions', 'symbols', 'urls', \
                               'media', \
                               'in_reply_to_screen_name', \
                               'in_reply_to_user_id_str', \
                               'in_reply_to_status_id_str', \
                               'place', 'retweeted_status_id', 'source', \
                               'text', 'user id' \
                               # some other attributes exsits, they are list below
                               #, status.withheld_copyright, \#optional
                               #status.withheld_in_countries, \#optional
                               #status.withheld_scope, \#optional
                               #status.truncated, \#default False
                               #status.retweeted, status.retweet_count, \#for no rt
                               #status.scopes, possibly_sensitive, \
                               #status.lang, status.fiter_level, \lang=en
                               #status.favorited, status.favorite_count, \
                               #status.current_user_retweet, \
                               #status.contributors, status.annotations \
                               ])
        self.userf = open(ts+'_user.csv','w',newline='')
        self.userw = csv.writer(self.userf)
        self.userw.writerow(['created_at', 'default_profile', \
                             #user.default_profile_image, \
                             'description', \
                             #user.entities, \
                             'favourites_count', \
                             #user.follow_request_sent, user.following,\#relate to given user
                             'followers_count', 'friends_count', \
                             'geo_enabled', 'id_str', 'is_translator', \
                             'lang', 'listed_count', 'location', \
                             #user.notifications, \
                             'name', \
                             #user.profile_background_color, user.profile_background_image_url, \
                             #user.profile_background_image_url_https, user.profile_background_tile, \
                             #user.profile_banner_url, user.profile_image_url, \
                             #user.profile_image_url_https, user.profile_link_color, \
                             #user.profile_sidebar_border_color, user.profile_sidebar_fill_color, \
                             #user.profile_text_color, user.profile_use_background_image, \
                             'protected', 'screen_name', \
                             #user.show_all_inline_media, user.status, \
                             'statuses_count', 'time_zone', 'user.url', \
                             #user.utc_offset, \
                             #user.withheld_in_countries, user.withheld_scope, 
                             'verified'])
        self.deletef = open(ts+'_delete.csv','w',newline='')
        self.deletew = csv.writer(self.deletef)
        self.deletew.writerow(['status_id','user_id'])
        self.logf = open('stream.log','a')
        self.count = 0
        self.err_count = 0
        self.time = 0.0
    
    def on_connect(self):
        """Called once connected to streaming server.

        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.
        """
        self.time = time.time()
        self.logf.write("connection build at time"+time.ctime(self.time)+'\n')

    def on_data(self, raw_data):
        """Called when raw data is received from connection.

        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.
        """
        self.count += 1
        
        data = json.loads(raw_data)
        
        if self.count >50000:
            self.statusf.close()
            self.userf.close()
            self.deletef.close()
            self.count = 0
            ts = time.strftime("./data/%Y%m%d%H%M")
            self.statusf = open(ts+'_status.csv','w',newline='')
            self.statusw = csv.writer(self.statusf)
            self.statusw.writerow(['id', 'created_at', 'coordinates',\
                               'hashtags', 'user_mentions', 'symbols', 'urls', \
                               'media', \
                               'in_reply_to_screen_name', \
                               'in_reply_to_user_id_str', \
                               'in_reply_to_status_id_str', \
                               'place', 'retweeted_status_id', 'source', \
                               'text', 'user id' \
                               # some other attributes exsits, they are list below
                               #, status.withheld_copyright, \#optional
                               #status.withheld_in_countries, \#optional
                               #status.withheld_scope, \#optional
                               #status.truncated, \#default False
                               #status.retweeted, status.retweet_count, \#for no rt
                               #status.scopes, possibly_sensitive, \
                               #status.lang, status.fiter_level, \lang=en
                               #status.favorited, status.favorite_count, \
                               #status.current_user_retweet, \
                               #status.contributors, status.annotations \
                               ])
            self.userf = open(ts+'_user.csv','w',newline='')
            self.userw = csv.writer(self.userf)
            self.userw.writerow(['created_at', 'default_profile', \
                             #user.default_profile_image, \
                             'description', \
                             #user.entities, \
                             'favourites_count', \
                             #user.follow_request_sent, user.following,\#relate to given user
                             'followers_count', 'friends_count', \
                             'geo_enabled', 'id_str', 'is_translator', \
                             'lang', 'listed_count', 'location', \
                             #user.notifications, \
                             'name', \
                             #user.profile_background_color, user.profile_background_image_url, \
                             #user.profile_background_image_url_https, user.profile_background_tile, \
                             #user.profile_banner_url, user.profile_image_url, \
                             #user.profile_image_url_https, user.profile_link_color, \
                             #user.profile_sidebar_border_color, user.profile_sidebar_fill_color, \
                             #user.profile_text_color, user.profile_use_background_image, \
                             'protected', 'screen_name', \
                             #user.show_all_inline_media, user.status, \
                             'statuses_count', 'time_zone', 'user.url', \
                             #user.utc_offset, \
                             #user.withheld_in_countries, user.withheld_scope, 
                             'verified'])
            self.deletef = open(ts+'_delete.csv','w',newline='')
            self.deletew = csv.writer(self.deletef)
            self.deletew.writerow(['status_id','user_id'])

        if 'in_reply_to_status_id' in data:
            status = Status.parse(self.api, data)
            if self.on_status(status) is False:
                return False
        elif 'delete' in data:
            delete = data['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'event' in data:
            status = Status.parse(self.api, data)
            if self.on_event(status) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(data['limit']['track']) is False:
                return False
        elif 'disconnect' in data:
            if self.on_disconnect(data['disconnect']) is False:
                return False
        elif 'warning' in data:
            if self.on_warning(data['warning']) is False:
                return False
        else:
            logging.error("Unknown message type: " + str(raw_data))
            return False
        return True
        
    #def on_data(self, data):
    #    self.f.write(data)
    #    self.count = self.count + 1
    #    print "recieving data %d" % self.count
    #    if self.count%1000 == 0 and (time.time()-self.time) > 60:
    #        print "total number of messages: %d" % self.count
    #        return False
    #    elif self.count%1000 == 0:
    #        return True
    #    else:
    #        return True
    def on_status(self, status):
        """Called when a new status arrives"""
        b = self.save_status(status)
        return b

    def on_exception(self, exception):
        """Called when an unhandled exception occurs.
        
        Exit when unhandled exception occurs."""
        self.logf.write(time.ctime()+': Exit due to Exception:'+traceback.format_exc()+'\n')
        self.logf.flush()
        return False
    
    def on_delete(self, status_id, user_id):
        """Called when a delete notice arrives for a status"""
        self.deletew.writerow([status_id,user_id])
        return True
    
    def on_limit(self, track):
        """Called when a limitation notice arrives"""
        self.logf.write('Stream incoming rate exceeds a limit. Fall behind '+track+'\n')
        self.logf.flush()
        return False

    def on_timeout(self):
        """Called when stream connection times out"""
        self.logf.write('timeout @'+time.ctime()+'\n')
        return False

    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice

        Disconnect codes are listed here:
        https://dev.twitter.com/docs/streaming-apis/messages#Disconnect_messages_disconnect
        """
        self.logf.write('disconnect @'+time.ctime()+'\n')
        return False
    
    def on_warning(self, notice):
        """Called when a disconnection warning message arrives"""
        self.logf.write('disconnection warning @'+time.ctime()+'\n')
        return False
    def on_error(self, status):
        self.logf.write('error occur @'+time.ctime()+status.__str__()+'\n')
        self.logf.flush()
        return False
    def save_status(self, status):
        entities = status.entities
        symbols = ''
        hashtags = ''
        user_mentions = ''
        media = ''
        urls = ''
        retweeted_status_id = ''
        if 'symbols' in entities:
            symbols = entities['symbols']
        if 'hashtags' in entities:
            hashtags = entities['hashtags']
        if 'user_mentions' in entities:
            user_mentions = entities['user_mentions']
        if 'media' in entities:
            for m in entities['media']:
                media += m['id_str']
                media += ' '
                media += m['expanded_url']
                media += ' '
                media += m['type']
                media += ','
        if 'urls' in entities:
            for u in entities['urls']:
                urls += u['expanded_url']
                urls += ' '
        if hasattr(status, 'retweeted_status'):
            retweeted_status_id = status.retweeted_status.id_str
            self.save_status(status.retweeted_status)
        try:
            self.save_user(status.user)
            self.statusw.writerow([status.id_str, status.created_at, status.coordinates,\
                               hashtags, user_mentions, symbols, urls, \
                               media, \
                               status.in_reply_to_screen_name, \
                               status.in_reply_to_user_id_str, \
                               status.in_reply_to_status_id_str, \
                               status.place.__str__(), retweeted_status_id, status.source, \
                               status.text, status.user.id_str \
                               # some other attributes exsits, they are list below
                               #, status.withheld_copyright, \#optional
                               #status.withheld_in_countries, \#optional
                               #status.withheld_scope, \#optional
                               #status.truncated, \#default False
                               #status.retweeted, status.retweet_count, \#for no rt
                               #status.scopes, possibly_sensitive, \
                               #status.lang, status.fiter_level, \lang=en
                               #status.favorited, status.favorite_count, \
                               #status.current_user_retweet, \
                               #status.contributors, status.annotations \
                               ])
            return True
        except UnicodeEncodeError:
            self.logf.write('UnicodeEncodeError:'+status.id_str+'\n')
            self.logf.flush()
            return False
    
    def save_user(self, user):
        description = ''
        if user.description is not None:
            description = user.description
        self.userw.writerow([user.created_at, user.default_profile, \
                             #user.default_profile_image, \
                             description, \
                             #user.entities, \
                             user.favourites_count, \
                             #user.follow_request_sent, user.following,\#relate to given user
                             user.followers_count, user.friends_count, \
                             user.geo_enabled, user.id_str, user.is_translator, \
                             user.lang, user.listed_count, user.location, \
                             #user.notifications, \
                             user.name, \
                             #user.profile_background_color, user.profile_background_image_url, \
                             #user.profile_background_image_url_https, user.profile_background_tile, \
                             #user.profile_banner_url, user.profile_image_url, \
                             #user.profile_image_url_https, user.profile_link_color, \
                             #user.profile_sidebar_border_color, user.profile_sidebar_fill_color, \
                             #user.profile_text_color, user.profile_use_background_image, \
                             user.protected, user.screen_name, \
                             #user.show_all_inline_media, user.status, \
                             user.statuses_count, user.time_zone, user.url, \
                             #user.utc_offset, \
                             #user.withheld_in_countries, user.withheld_scope, 
                             user.verified])
if __name__ == '__main__':
    consumer_key = 'E25EdiCXmoqfBSN0vMUzQdgr2'
    consumer_secret = 'M2wpz5mq3ck5u2FiAnp1MCXlo4EqrhZ7RHd1TUDecTIJSVlIEk'
    access_token = '614605905-XvYzSEF1y1skQW5XZX2J8DDAFze64Gu7iqTtkN45'
    access_token_secret = 'H4mtnCj2j0nD4z1rWq5Lbq3ptOp0c9SuDuW530dqtp07C'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    l = Save2FileListener()
    #stream = tweepy.Stream(auth, l)
    looping = False
    count_stream = 0
    while not looping:
        #print('building connection')
        count_stream += 1
        if count_stream == 1:
            try:
                stream = NewStream(auth, l)
                stream.sample(languages=['en'])
            except Exception:
                stream.disconnect()
                l.logf.write(time.ctime()+': stream end because: '+traceback.format_exc()+'\n')
            finally:
                l.logf.flush()
            count_stream -= 1
            time.sleep(5)
        else:
            time.sleep(5)
            count_stream = 0
        #print('connection down')

