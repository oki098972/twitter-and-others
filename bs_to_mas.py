from atproto import Client
from mastodon import Mastodon
import requests
import os
import glob
import time
from datetime import datetime, timezone, timedelta

def has_video_mp4(embed):
    if hasattr(embed, 'media') and hasattr(embed.media, 'video'):
        return embed.media.video.mime_type == 'video/mp4'
    return False

#for debug
out1_time = []
out2_time = []
#for debug

# 設定
BLUESKY_USERNAME = "xxxxxxxx.bsky.social"
BLUESKY_PASSWORD = "aaaa-bbbb-cccc-dddd"
MASTODON_ACCESS_TOKEN = "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
MASTODON_BASE_URL = "https://mastodon.social"  # MastodonのインスタンスURL

# 取得する投稿の時間範囲（UTCで指定）
until_time = datetime.now(tz=timezone.utc)                         #現在時刻をUTCで取得
until_time = until_time.replace(minute=0, second=0, microsecond=0) #正時（hh:00:00）にする
since_time = until_time - timedelta(hours=3)                       #さらに3H遡ってた投稿を取得対象とする

# Blueskyにログイン
client = Client()
client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)

# 時間範囲をISOフォーマットに変換
since_time = since_time.isoformat().replace("+00:00", "Z")
until_time = until_time.isoformat().replace("+00:00", "Z")

# Blueskyの投稿を検索
search_params = {
    "q": "from:xxxxxxxx.bsky.social", #https://qiita.com/nekoniii3/items/bbaef6a19b4aa1d02c10の知見に従ってここで投稿主を絞る
    "sort": "latest",
    "limit": 30,
    "since": since_time,
    "until": until_time
}
search_results = client.app.bsky.feed.search_posts(search_params)["posts"]
print(f"ヒット件数: {len(search_results)}")

if not search_results:
    print("指定時間内の投稿が見つかりませんでした。")
    exit()


# Mastodonインスタンス作成
mastodon = Mastodon(access_token=MASTODON_ACCESS_TOKEN, api_base_url=MASTODON_BASE_URL)

# 保存フォルダ
os.chdir('/home/xxxxxxxx/')
MEDIA_DIR = "./media"
os.makedirs(MEDIA_DIR, exist_ok=True)
# ファイルを削除（あれば）
for filename in  glob.glob('./media/*'):
    os.remove(filename)

# ヒットした投稿をすべて処理
for post in reversed(search_results):
    post_text = post.record.text

    #連続でmastodonのAPIを叩くと制限にかかるようなので１秒waitをかける
    #制限は件数によるものらしいが残しとくか
    #2025/04/02:久々にブラウザでmastodon見たら「制限に達しました」ってメッセージが出てたんで3秒に変えて様子見
    time.sleep(3)

    # 動画が含まれる場合はスキップ
    if hasattr(post, "embed") and hasattr(post.embed, "videos"):
        print("動画付きの投稿: ", post_text)
        #continue
        post_text = f"※本投稿はblueskyの投稿の転送ですが、現状blueskyの投稿から動画が取得する方法が不明な為、動画はありません\n{post_text}"
    if hasattr(post, "record") and hasattr(post.record, "embed"):
        if has_video_mp4(post.record.embed):
            print("動画付きの投稿: ", post_text)
            #continue
            post_text = f"※本投稿はblueskyの投稿の転送ですが、現状blueskyの投稿から動画が取得する方法が不明な為、動画はありません\n{post_text}"
    # OHアラートの文字列が無ければスキップ
    if not("OHアラート" in post_text):
        print("「OHアラート」文字列が無いのでスキップ: ", post_text)
        continue

    # メディアを取得
    media_ids = []
    if hasattr(post, "embed") and hasattr(post.embed, "images"):
        for img in post.embed.images:
            img_url = img.fullsize
            img_filename = os.path.join(MEDIA_DIR, os.path.basename(img_url))

            # 画像をダウンロード
            response = requests.get(img_url)
            with open(img_filename, "wb") as f:
                f.write(response.content)
            
            # Mastodonにアップロード
            media_id = mastodon.media_post(img_filename)
            media_ids.append(media_id)

    # Mastodonに投稿
    mastodon.status_post(post_text, media_ids=media_ids)
    print("Mastodonに投稿しました！")
