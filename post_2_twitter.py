#!/usr/bin/env python
# -*- coding: utf-8 -*-
#original source by https://qiita.com/dmackey_2128/items/7a7e01ea47e745913fcb

import tweepy
import sys

# Twitter APIキーとアクセストークン
CONSUMER_KEY = 'aaaaaaaaaaaaaaaaaaaaaaaaa'
CONSUMER_SECRET = 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
ACCESS_TOKEN = 'cccccccccccccccccccccccccccccccccccccccccccccccccc'
ACCESS_TOKEN_SECRET = 'ddddddddddddddddddddddddddddddddddddddddddddd'

# 指定テキスト内容でツイートする
def text_tweet(text):

    #引数で投稿文字列を渡すのだが、改行コードが生で入ってるとNGだったのが置き換えの理由だったはず
    text = text.replace("(cr)","\n")

    client = tweepy.Client(consumer_key=CONSUMER_KEY,
                           consumer_secret=CONSUMER_SECRET,
                           access_token=ACCESS_TOKEN,
                           access_token_secret=ACCESS_TOKEN_SECRET)
    try:
        tweeted_data = client.create_tweet(text=text)
    except Exception as e:
        print(e)
        return False

    if ('id' in tweeted_data.data):
        #結果あり
        ret_val = tweeted_data.data['id']
    else:
        ret_val = 0

    return ret_val

# 指定テキスト内容とファイルをツイートする
def image_tweet(text, imagefiles):

    #引数で投稿文字列を渡すのだが、改行コードが生で入ってるとNGだったのが置き換えの理由だったはず
    text = text.replace("(cr)","\n")
    outlist = imagefiles.split(',')
    if (len(outlist) == 0):
        #添付ファイル無し
        return False
    if (len(outlist) > 4):
        #4個を超えたら送れない
        return False

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    client = tweepy.Client(consumer_key=CONSUMER_KEY,
                           consumer_secret=CONSUMER_SECRET,
                           access_token=ACCESS_TOKEN,
                           access_token_secret=ACCESS_TOKEN_SECRET)

    #tweetに画像を添付する
    media_ids = []
    for sendfile in outlist:
        media = api.media_upload(filename=sendfile)
        media_ids.append(media.media_id)

    try:
        tweeted_data = client.create_tweet(text=text, media_ids=media_ids)
    except Exception as e:
        print(e)
        return False

    if ('id' in tweeted_data.data):
        #結果あり
        ret_val = tweeted_data.data['id']
    else:
        ret_val = 0

    return ret_val

def main():

    #引数は分を単位とする
    args = sys.argv
    if (2 == len(args)):
        #添付ファイル無し
        ret_val = text_tweet(args[1])
    elif (3 == len(args)):
        ret_val = image_tweet(args[1], args[2])

    if isinstance(ret_val, bool):
        print(f"bool型で投稿結果が返ってきました。文字数超過で投稿失敗かも：{ret_val}")
        ret_val = str(ret_val)  # True → "True", False → "False"
    
    sys.stdout.write(ret_val)
    sys.exit()

if __name__ == "__main__":
    main()
