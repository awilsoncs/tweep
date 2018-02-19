#!/usr/bin/env python3
import argparse
import os
import sys

import twitter


KEY = "TWITTER_KEY"
SECRET = "TWITTER_SECRET"
APP_KEY = "TWEEP_KEY"
APP_SECRET = "TWEEP_SECRET"


def parse_args():
    parser = argparse.ArgumentParser("Simplified command line tweeting.")
    parser.add_argument("msg", type=str, nargs="*", help="Tweet the given message")
    parser.add_argument("-f", "--feed", action="store_true", help="Show all recent tweets from feed")
    args = parser.parse_args()
    return args

def get_api(key, secret, token, token_secret):
    try:
        return twitter.Api(consumer_key=key,
                consumer_secret=secret,
                access_token_key=token,
                access_token_secret=token_secret)
    except Exception as ex:
        print("Failed to connect to twitter: ", ex)
        sys.exit(-1)


def get_keys():
    key = os.environ.get(KEY)
    secret = os.environ.get(SECRET)
    app_token = os.environ.get(APP_KEY)
    app_secret = os.environ.get(APP_SECRET)

    abort = False
    if key is None:
        print("Missing in env: " + KEY)
        abort = True
    if secret is None:
        print("Missing in env: " + SECRET)
        abort = True
    if app_token is None:
        print("Missing in env: " + APP_KEY)
        abort = True
    if app_secret is None:
        print("Missing in env: " + APP_SECRET)
        abort = True

    if abort:
        print("Aborting.")
        sys.exit(-1)

    keys = {}
    keys[KEY] = key
    keys[SECRET] = secret
    keys[APP_KEY] = app_token
    keys[APP_SECRET] = app_secret

    return keys


def tweet(api, message):
    try:
        status = api.PostUpdate(message)
    except Exception as ex:
        print("Encountered an error while posting update: ", ex)
        sys.exit(-1)


def main(args):
    keys = get_keys()
    key = keys[KEY]
    secret = keys[SECRET]
    app_key = keys[APP_KEY]
    app_secret = keys[APP_SECRET]

    api = get_api(key, secret, app_key, app_secret)
    
    if len(args.msg) is not 0:
        tweet(api, " ".join(args.msg))
    return 0

if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(args))
