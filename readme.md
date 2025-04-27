twitter及び近似サービス用自動投稿用コード

***

- post_2_bluesky.py:  
    bluesky投稿用pythonスクリプト  
    使い方：python3 post_2_bluesky.py "投稿文字列"  
    　　　　　　又は  
    　　　　python3 post_2_bluesky.py "投稿文字列" "投稿画像"
  
    投稿画像の部分にはカンマ区切りでファイル名を指定する（ex.: "aaa.png,bbb.png"）、最大４ファイルまで対応
    twitterと異なり、動画添付は不可だったはず

***

- post_2_twitter.py:  
    twitter投稿用pythonスクリプト  
    使い方：python3 post_2_twitter.py "投稿文字列"  
    　　　　　　又は  
    　　　　python3 post_2_twitter.py "投稿文字列" "投稿画像"
  
    投稿画像の部分にはカンマ区切りでファイル名を指定する（ex.: "aaa.png,bbb.png"）、最大４ファイルまで対応  
    twtterが自動で判定してくれるようで、投稿画像の部分には動画ファイルでも可（pngとmp4しか確認してないがおそらくtwitterが対応してる形式ならup可能と思われる

***
