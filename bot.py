# Framework Copyright (c) 2015-2016 Molly White
# Additional code Copyright (c) 2016 Stuart Grieve
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import os.path as path
import tweepy
import random
from secrets import *
from time import gmtime, strftime


# ====== Individual bot configuration ==========================
bot_username = 'COUNTRYCAPSBOT'
logfile_name = bot_username + ".log"

# ==============================================================


def create_tweet():
    '''
    Load a random lyric from the file, check its length and if it has been
    recently tweeted and return it in uppercase.
    '''
    lyricpath = path.realpath(path.join(os.getcwd(), path.dirname(__file__)))
    with open(path.join(lyricpath, 'LYRICS.txt'), 'r') as f:
        lyrics = f.readlines()

    Recent = GetRecentTweets()

    # cycle through random lyrics until one meets the criteria.
    while True:
        text = random.choice(lyrics)

        if (text not in Recent) and CheckLength(text):
            break

    return text.upper()


def WriteRecent(tweet):
    '''
    Write the most recent tweet to a file, keeping the 5 most recent tweets.
    Adds tweet to front of file and pops the oldest recent tweet off the file.
    '''
    recentpath = path.realpath(path.join(os.getcwd(), path.dirname(__file__)))
    with open(path.join(recentpath, 'RECENT.txt'), 'r') as f:
        recent = f.readlines()

    # if the list is longer than 4, remove the last entry and add the tweet
    # otherwise just add the tweet to the list
    if len(recent) >= 5:
        recent = [''] + recent[:-1]
        recent[0] = tweet
    else:
        recent = [''] + recent[:]
        recent[0] = tweet

    with open(path.join(recentpath, 'RECENT.txt'), 'w') as f:
        for r in recent:
            f.write(r)


def GetRecentTweets():
    '''
    Load the most recent tweets from a file.
    '''
    recentpath = path.realpath(path.join(os.getcwd(), path.dirname(__file__)))
    with open(path.join(recentpath, 'RECENT.txt'), 'r') as f:
        return f.readlines()


def CheckLength(text):
    '''
    Check the prospective tweet is not too long.
    '''
    if len(text) > 139:
        return False
    else:
        return True


def tweet(text):
    """Send out the text as a tweet."""
    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Send the tweet and log success or failure
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted: " + text)

    WriteRecent(text)


def log(message):
    """Log message to logfile."""
    logpath = path.realpath(path.join(os.getcwd(), path.dirname(__file__)))
    with open(path.join(logpath, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


if __name__ == "__main__":
    tweet_text = create_tweet()
    tweet(tweet_text)
