from atproto import Client
from flask import Blueprint
import app.nlp as nlp
import os
import sys


chahan = Blueprint("chahan", __name__, url_prefix="/chahan")
client = Client()
# https://bsky.app/profile/did:plc:kwibnjihi6sfdphwfzlogfwi/feed/jp-cluster
feed_uri = (
    "at://did:plc:kwibnjihi6sfdphwfzlogfwi/app.bsky.feed.generator/jp-cluster"
)


def text_url_removed(post) -> str:
    facets = post.record.facets
    if facets is not None:
        encoded = post.record.text.encode("utf-8")
        indices = map(lambda x: (x.index.byte_start, x.index.byte_end), facets)
        slices = list(
            map(lambda x: encoded[x[0]:x[1]].decode("utf-8"), indices)
        )
        for slice in slices:
            post.record.text = post.record.text.replace(slice, "")
    return post.record.text


def fetch_post(count: int) -> [str]:
    posts = []
    cursor = None
    page_size = 100
    while len(posts) < count:
        remaining = count - len(posts)
        res = client.app.bsky.feed.get_feed(
            params={
                "feed": feed_uri,
                "limit": page_size if remaining > page_size else remaining,
                "cursor": cursor,
            }
        )
        posts += list(map(lambda f: text_url_removed(f.post), res.feed))
        cursor = res.cursor

    return posts


def post_text(text: str):
    client.send_post(text=text, langs=["ja"])


@chahan.route("/")
def main():
    profile = client.login(
        os.environ["chahan_username"], os.environ["chahan_password"]
    )
    print(f"logged in as {profile.display_name} ({profile.handle})")

    r = client.app.bsky.feed.get_feed_generator(params={"feed": feed_uri})
    if not (r.is_online and r.is_valid):
        print("Feed not available")
        sys.exit(1)

    while True:
        try:
            posts = fetch_post(100)
            data, text_depth, pos_depth = nlp.data_preprocessing(posts)
            text_model, pos_model = nlp.build_models(
                data, text_depth, pos_depth
            )
            text = ""
            while text.strip() == "":
                text = nlp.generate_text(text_model, pos_model)
            print(text, file=sys.stderr)
            post_text(text)

            del posts, text_depth, pos_depth, text_model, pos_model, text
            return "ちゃあはん！"

        except Exception as e:
            print(e, file=sys.stderr)
