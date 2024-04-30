from atproto import Client, client_utils, models
from datetime import datetime, timedelta
from flask import Blueprint
import os
from zoneinfo import ZoneInfo


shuukei = Blueprint("shuukei", __name__, url_prefix="/shuukei")

isoformat = "%Y-%m-%dT%H:%M:%S.%fZ"


def get_followers(client, profile):
    f = []
    get_followers_cursor = None
    while True:
        r = client.app.bsky.graph.get_followers(
            params={
                "actor": profile.did,
                "limit": 100,
                "cursor": get_followers_cursor,
            }
        )
        f += r.followers
        get_followers_cursor = r.cursor
        if get_followers_cursor is None:
            break
    return f


class Data(object):
    def __init__(self, v):
        self.type = (
            "repost"
            if v.reason is not None
            else "reply" if v.reply is not None else "post"
        )
        if self.type == "repost":
            self.date = (
                datetime.strptime(v.reason.indexed_at, isoformat)
                .astimezone(ZoneInfo("Japan"))
                .date()
            )
        else:
            self.date = (
                datetime.strptime(v.post.indexed_at, isoformat)
                .astimezone(ZoneInfo("Japan"))
                .date()
            )


def get_stats_on_date(client, actor, target_date):
    cursor = None
    posts = []

    while True:
        r = client.app.bsky.feed.get_author_feed(
            params={
                "actor": actor.did,
                "limit": 100,
                "cursor": cursor,
                "filter": "posts_with_replies",
            }
        )
        cursor = r.cursor
        if cursor is None:
            break

        data = map(lambda v: Data(v), r.feed)
        filtered = filter(lambda d: d.date >= target_date, data)

        old_len = len(posts)
        posts.extend(filtered)
        if old_len == len(posts):
            break

    posts = list(filter(lambda d: d.date == target_date, posts))
    stats = {
        "sum": len(posts),
        "posts": sum(map(lambda d: d.type == "post", posts)),
        "reposts": sum(map(lambda d: d.type == "repost", posts)),
        "replies": sum(map(lambda d: d.type == "reply", posts)),
    }
    return stats


def post_announcement(client, date):
    text_builder = client_utils.TextBuilder()
    text_builder.tag("しゅうけいくん", "しゅうけいくん")
    text_builder.text("がみんなの集計結果を発表しまーす！")
    r = client.post(text_builder)
    return models.create_strong_ref(r)


def post_stats(client, root, parent, actor, stats, date):
    text_builder = client_utils.TextBuilder()
    main_text = (
        "さんの集計結果です！\n"
        + f" {date}\n\n"
        + f"総計：{stats['sum']}\n"
        + f"ポスト：{stats['posts']}\n"
        + f"リポスト：{stats['reposts']}\n"
        + f"リプライ：{stats['replies']}"
    )

    remaining = 300 - len(main_text)
    name = (
        actor.display_name
        if remaining >= len(actor.display_name)
        else actor.display_name[: remaining - 1] + "…"
    )

    text_builder.mention(name, actor.did)
    text_builder.text(main_text)
    r = client.post(
        text_builder,
        reply_to=models.AppBskyFeedPost.ReplyRef(parent=parent, root=root),
    )
    return models.create_strong_ref(r)


@shuukei.route("/")
def show_stats():
    client = Client()
    profile = client.login(
        os.environ["shuukei_username"], os.environ["shuukei_password"]
    )
    print(f"logged in as {profile.display_name} ({profile.handle})")

    followers = get_followers(client, profile)
    print(f"Gathering statistics on {len(followers)} followers")

    current_date = datetime.now(ZoneInfo("Japan")).date()
    target_date = current_date - timedelta(days=1)

    root = post_announcement(client, target_date)
    parent = root

    for follower in followers:
        stats = get_stats_on_date(client, follower, target_date)
        if stats["sum"] == 0:
            continue

        parent = post_stats(client, root, parent, follower, stats, target_date)

    return "しゅうけい！"
