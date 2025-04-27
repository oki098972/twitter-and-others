#!/usr/bin/env python
# -*- coding: utf-8 -*-
#original source by https://github.com/MarshalX/atproto/blob/main/examples/send_images.py
#usage this function: python3 twpost2_temp_blue.py sendtext imgfile1,imgfile2

import sys
import io
from atproto import Client, models

# アカウントID
account = "xxxxxxxx.bsky.social"
# パスワード
apppassword = "aaaa-bbbb-cccc-dddd"

def image_tweet(p_text, p_imagefiles):

    p_text = p_text.replace("(cr)","\n")

    client = Client()
    client.login(account, apppassword)

    imgfile_paths = p_imagefiles.split(',')

    images = []
    for path in imgfile_paths:
        with open(path, 'rb') as f:
            images.append(f.read())

    tweeted_data = client.send_images(text=p_text,images=images)
    return tweeted_data

def text_tweet(p_text):
    p_text = p_text.replace("(cr)","\n")
    client = Client()
    client.login(account, apppassword)
    tweeted_data = client.send_post(text=p_text)

    return tweeted_data

def main():

#ins-s by toshi-shimoji
    #引数は分を単位とする
    args = sys.argv
    if (2 == len(args)):
        #添付ファイル無し
        ret_val = text_tweet(args[1])
    elif (3 == len(args)):
        ret_val = image_tweet(args[1], args[2])

    #本来ret_valの中身を要素ごとに変数に格納すればいいのが面倒なので
    #print文を使いたい、ので標準出力を変数に切り替えるというアホなことをしている
    with io.StringIO() as f:
        #標準出力を f に切り替える
        sys.stdout = f
        #ここでprintすると出力先はfになっている
        print(ret_val)
        #オブジェクト？を文字化したのでテキスト化されているはず
        ret_val = f.getvalue()
        #標準出力をデフォルトに戻す
        sys.stdout = sys.__stdout__
    
    sys.stdout.write(ret_val)
    sys.exit()

if __name__ == '__main__':
    main()
