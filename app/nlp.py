from copy import deepcopy
from collections import Counter
from itertools import chain, product
from janome.tokenizer import Tokenizer
import pandas as pd
import random
import re
import time
import unicodedata


data = [
    "頭悪そうな日菜ちん描いてるけどとりあえず引越し準備終わらせねば…",
    "お気づきの通りもうひとつのサブ垢は日常メイン垢です",
    "スターレイル光円錐とか遺物ばっか育成して肝心の天賦を上げるのを忘れていた…\n光円錐はともかく遺物より天賦が先だったわ…\n符玄ですら上げきってなかった…！",
    "はあもうダメだ何も終わらせられない私には",
    "こっちはそこまで暑くないけど最近夜寝苦しいんよね。悪夢にうなされて起きる🥺",
    "試合当日まで隠しきれるかどうかはめっちゃ興味ある。無理なんじゃないかという予感はある。",
    "ボーはおそれている、見てきたけど全ての不条理の意味がさっぱり分からなくて、Xで「あれはユダヤ教の受難のオマージュ」っていう解説記事を読んだところ。読んでも全然スッキリするわけじゃないけど。",
    "今の狐面を修理するか....同じものを作ってもらうか...うーん...",
    "フォロワーの7割が手当たり次第フォローしまくってフォロワー増やすような垢なんだが()",
    "ヨースケ真犯人案がそのまま通ってたら\n今まであんなに優しくしてくれてたヨースケから突然切られることになるわけで\n番長の足立告発しないルートのヨースケも同じだよな\nトラウマゲーとして永久封印になるとこだわ",
    "お昼なんかあるものなんでもいいんだよランチ\n\n@gohanclub.bsky.social",
    "おトイレバトル、全体的なカラーは黒と青緑なので青緑を使うと思うけど、赤と青の宿命色も好きだからそっちで統一するかも",
    "こはくさん～！ありがとうございます\U0001faf6キャラデザ好き人間としてHAPPYです！！",
    "画像貼るテスト\n(写真アプリから共有候補には出て来なかったから…)\n\n最近の画像編集貼り合わせを作業BGMは乃木坂ちゃん\n\n乃木坂づいてる日々…このプチマイブームは当面続くんだろうね😌",
    "沖田さんと斎藤さん。 \n斎藤さんって、洋服のイメージが強いのは「るろ剣」を読んでたからかな？？",
    "安いラーメン屋があったのだが久々に行くと当面休業中だった\nがーんだな…",
    "もうすぐ満開だった河津桜、昨日の大雨と強風でいっきに終わりに近くなってきた状態。すでに花びらが散り始めてる！",
    "ほどよい味噌味でおいしかった！\n#時は豚なり",
    "どんなゲームも本体とソフトが揃えば遊べると思ってるからそんな事あるの！？という衝撃",
    "100ちゃん今日はめっちゃ素直にお昼食べてくれた",
    "昨日は急な予定が入り（プレゼント絵を描く）配信ができなかったけど裏で少しだけホコやれました😆\n水曜早起き予定があるので念のため今日も配信休みなのよねごめん～🙏",
    "みすきーあいおーもそうだったから…>RT",
    "ラムステーキ。前回はハーフだったので今回は1ブロック。やはり食べ過ぎ。",
    "明日は娘の幼稚園で去年から練習していたダンスや演奏を披露する予定だったけど、インフル罹患で参加でないことになりました。かわいそう😢",
    '"私たち"…？',
    "金沢で買ったゴールドのお気に入りピアス…\n無くしてなくてよかった\U0001f979",
    "素敵な猫猫と壬氏様描く方がおられるー😭と思ってプロフィール見たら商業BL描いてる方で拝んだ。貴重な存在。ありがとう……",
    "頭脳警察のアルバム「誕生」を聴いていた。",
    "なぎりーはそれがでかい",
    "ネコメイド妹ちゃん🐈",
    "こんなに暖かくてつくしんぼあたりはにょきにょき生えてきそうだね",
    "よし、モナのSP節約の為に祐介入れてみよう！って思ったら、出てくる敵がみんな物理氷耐性で、セーフルーム逃げ込んだよ",
    "最近、幻冬社版のコジコジを揃えたのだけど、めちゃくちゃ装丁が凝っててとってもかわいいんですよー\n\nあんなに豪華な装丁、1200円でできたのは2000年に発行だったからなんだろうなあ",
    "オモコロで梨さんの新作見た！難しくてよくわからない……解説がほしい",
    "ほ、北斎プレマ買えなかった…",
    "日常に戻る",
    "自分が楽しければいいとだけ考えられるならいいと思うけど\n楽しくてかつ少しでも推しの力になりたいって思ってて\n今の自分が何か力になれてるかって考えたら全くだし\nリスナーとしての今の自分に価値があるかって考えたらないって思う",
    "デスティニーインパルス張ってたのに何故かデスティニーSpecIIの方が注文できてしまう",
    "両断される\u3000いぬ",
    "据え置きゲーでもストーリー長すぎると失踪するのでほどほどのボリュームじゃないとダメ だ",
    "カニに勝てるわけないだろ。",
    "食った後、賞味期限4度見しました",
    "最近の絵の講座系はこういう描き方はダメだとかやっちゃいけない描き方とか否定から入るものがよく流れるようになってなんだかなあの気持ち。絵って本来は自由に描いていいもののはずだったんだけどな。",
    "うーん13-2⭐︎3クリアできない",
    "はじめてみました😊よろしくお願いします🙏\n\n最近お気に入りのサクラソウです。",
    "寝",
    "渡会雲雀がユニゾンを歌う日も遠くないんだと私は確信してるんだ",
    "とはいえ2月なのでね…雰囲気がね… と見栄張って上着着て出かけたら暑さでジューシーに蒸しあがってしまった。そもそもすっぴんのくせに妙な見栄を張るんじゃない",
    "いや、見たいじゃん\nｾﾗとﾍﾞﾘの牽制現パロって",
    "新空港占拠は家に帰ってから見ようと思ってネタバレ避けてたんだけどライブでジェシー本人からネタバレ食らった話でもする？",
    "あああああーー！！！\nクリーニングのタグ丸見えで２時間闊歩してた！はずっっっ\nリバーシブルのやつ裏返して着てたから襟元全見えやん",
    "寝起きのほこりくん、ショタだからかわいくみえるかもだけど、実際はめちゃ機嫌悪くて怒ってて攻撃的で危ない\n怒ってる猫が可愛いのと同じかも",
    "X消したニンゲンなので、Xで見ていた以前の作品がまた青空で見られる喜び。これは踊るっきゃねぇ(“ᕕ( ᐛ )ᕗ,,“ᕕ( ᐛ )ᕗ,,ﾁﾋﾟﾁﾋﾟﾁｬﾊﾟﾁｬﾊﾟﾙﾋﾞﾙﾋﾞﾗﾊﾞﾗﾊﾞﾊﾟﾁｺﾐﾙﾋﾞﾙﾋﾞﾌﾞｰﾌﾞｰﾌﾞｰ(ง  ᐛ  )ว🎶 (ง  ᐛ  )ว 🎶(ง  ᐛ  )ว 🎶",
    "金持ちニート夢見て今日も生きる。\n(大嫌いな人事考課シート作成の時期)",
    "公式、舞台化の情報を焦らすな…焦らしていいのは(自主規制)",
    "ワーフリおつかれさまでした！",
    "ついた〜\n#ミドグラ",
    "",
    "ここはTwitterより気が楽でいいわ\n1部界隈から嫌われてるからなぁ",
    "赤子が汗ばんでる……",
    "ふたたび寝てた。今度はベッドでゆっくり寝た💤。そしたらちぇりちゃんが小さな赤ちゃん猫を拾って来る夢を見た。長毛の赤ちゃんをちぇりが取り上げられないように隠して見せてくれない。実際は外に出さないので、ちぇりが拾って来ることはないんだけど、夢の中でも「赤ちゃん猫に猫エイズがうつっちゃうなぁ。どうしよう😥」とヤキモキしてる夢だった。\nちぇりはまだ発症はしてないし、一生発症しないようになるべくストレスない生活が送れるように気をつけてる（つもり…）。",
    "コマ割り大きく見直して調整したら20ページ増えたんだけど……\nでも間の余韻とかできて、絶対良くなったと思う\n……がんばろ",
    "夜はちょっと寒いくらいが嬉しいかも(布団が気持ちいいため😁)",
    "3/17も上京するから関東のゲーセンに寄るか誰か捕まえて飲み行くか迷う～～～日帰りつらい！",
    "明日はひたすらトマトカットせんといかん…マシーンに頼るかなあ。あれ好きじゃないんだけど、さすがに全部手で切るのだるすぎる。",
    "@zznnyydq10.bsky.social \nうえい！じにーちゃん！！",
    "😔辛い時😔\n\n😢悲しい時😢\n\n人はどんな時でも心の隙間に\n\n⚫️⚫️闇⚫️⚫️\n\nができる！その心の\n\n⚫️⚫️闇⚫️⚫️\n\nに\n\n😈👹🧛魔物たち👻👿🧟\n\nは容赦なく入り込んでくるのだ！\n\nだから\u3000苦しくても\n\n挫けるな🦶💥！\n\n落ち込むな✊💥！！\n\nクヨクヨするな\U0001faf5💥！！！\n\n何事にも屈しない強靭な\n\n❤️\u200d🔥心❤️\u200d🔥\n\nこそが最強の\n\n⚔️武器⚔️\n\nなのだから！！！！！！",
    "ブルスコしまくることで得られる正義もあるんだから仕方がない",
    "今dアニメ会員しか見れないようになってないですか？？？？",
    "金カムめっちゃ良かったよ！！！？？？！？！",
    "もう200postはちょっときもいとおもう",
    "新規イラストめちゃくちゃ可愛いし、MVも可愛い！…ってか3Dじゃん！",
    "多分私の声聴いたことある人ほとんどいないと思う",
    "肉の万世秋葉原本店閉店寂しすぎる。いろんな人と秋葉原行くたびにここで食べたなぁ。思い出の場所が…閉店までに一度は行きたい。思い出納めしたい。",
    "ｳﾜｰｰｰｰｰｰｰｰｰｰｯｯｯ‼︎‼︎‼︎‼︎‼︎(不調)",
    "なんかやばそうなのでフォローされてフォロバしてたっぽいけど一旦ブロ解しとくか",
    "近所のカレー屋さんがロケット団のアジトになってて笑っちゃった\nランチに来たのかな\n#pokemonGO",
    "これで明日は最高気温10℃とかなるんじゃろ？\n体壊れてまうで(:3_ヽ)_",
    "公開マンツーみたいな感じになるのかなぁ。ここに人が増えるようにはあまりおもえない。",
    "DLCかッ…………！！！！（ググった）",
    "今日店を1時間早く閉めてその後に社長が来てお話をされるみたいなんだけど、そこまでしてする話って良い話か悪い話かって言ったらもう、そう",
    "ちょっと忙しくなるとすぐ色々後回しにしちゃうんだから〜…",
    "とるものぬいちゃんが届いていたのに出かける直前に気づいてしまって…荷物も多いし大分帰らないから玄関の内側に放ってそのまま出てきてしまったんですがなんとかして荷物にねじ込めばよかったなと",
    "フォローしたと思ったらできてなかったみたいなのちょいちょいやっちゃう",
    "今週は金曜お仕事なので三連休なんてなかった()",
    "今日も元気に！！バクシーン！！！（書きたいコメントがなかったです）",
    "いりあむVへの目線変わる話だなコレ",
    "タイッツーもいいな",
    "なんとなく「薫風梢」で検索したら候補にアークナイツって出てきて、なんで？ と思ったらアークナイツにそういうスキン？があるらしい\u3000そえなんだ",
    "ハローワーク行って仕事探して\n窓口行ったのに👨\u200d⚕️の意見書が絶対に\nいるみたいで仕事紹介してくれんかった\nその意見書にもお金かかるのに毎回毎回\n出しよったらアホくさいよな\n病状も変わってくるのに\nやっぱり病気になっていい事なさすぎる\n普通に働きたいのに働けんし\n介護の仕事したいのに作業所から行けっち\n言われたり。ダルすぎるやろ、、、",
    "センシティブ設定しないのはセンシティブ設定=サーチBANのイメージがXでついてしまったからなのか\nそれともルールが日本語化されてないからなのか\n\n早く公式日本語ルールできるといいね",
    "どうせ神曲なんて余り散らかすし黄金までのんびり全身クレデンダムRE化計画をしていけばいいのよね",
    "不信任決議\n投票総数452\n賛成122\n反対330",
    "最近はクレカ限度額までガチャ回すぜﾋｬｯﾊｰ!はしなくなったんだけど普通に買い物してしまう\n人の物欲は終わらねぇ",
    "〜たまに訪れる本当に料理するのがイヤイヤ期〜\u3000しばらく放置するとなおります\u3000たぶん",
    "お日様ポカポカ暖かいね🔅\nみるたは午前中にミスしてしまって凹んでます(ˆ꜆ . \xa0̫ . )\n午後もゆるやかに頑張ろうねっ✊",
    "モチベが家出🦀してたけどお米という生き物は単純なもので…一気にモチベ上がった！生きる！",
    "今日花粉飛んでそうだなあ〜",
    "なんだこの異常な眠さは。\n春か…？",
    "わろた",
]

tokenizer = Tokenizer(
    "special_words.csv", udic_type="simpledic", udic_enc="utf8"
)


class Model(object):
    def __init__(self, depth):
        self.model = {}
        self.depth = depth

    def add_ngrams(self, ngrams, key_transform=None):
        for ngram in ngrams:
            k = (
                ngram[:-1]
                if key_transform is None
                else key_transform(ngram[:-1])
            )
            if k not in self.model:
                self.model[k] = [ngram[-1]]
            else:
                self.model[k].append(ngram[-1])

    def normalise(self):
        for key in self.model.keys():
            counter = Counter(self.model[key])
            total = sum(counter.values())
            probability = {
                item: max(count / total, 0.1) for item, count in counter.items()
            }
            if total < 1:
                scaling_factor = 1 / total
                probability = {
                    key: value * scaling_factor
                    for key, value in probability.items()
                }
            elif total > 1:
                scaling_factor = 1 / total
                probability = {
                    key: value * scaling_factor
                    for key, value in probability.items()
                }
            self.model[key] = probability

    def next_word_choice(self, context):
        if context in self.model:
            return self.model[context]
        else:
            return None


def data_preprocessing(data):
    rgx = re.compile(
        r"@([a-zA-Z0-9_\-]+\.)+([a-zA-Z0-9_\-]+)|[（）()「」『』【】]|[a-zA-Z_-]*RT[a-zA-Z_-]*"
    )

    def rules(s):
        s1 = re.sub(rgx, "", s)
        s2 = unicodedata.normalize("NFKC", s1)
        return s2

    split_it = map(lambda s: s.split("\n"), data)
    data = [rules(x) for xs in split_it for x in xs]

    tokens = list(
        map(lambda t: list(tokenizer.tokenize("<start>" + t + "<end>")), data)
    )
    df = pd.DataFrame(
        {"tokens": tokens, "len": list(map(lambda t: len(t), tokens))}
    )
    q = df["len"].quantile(0.90)
    df = df[df["len"] < q]
    pos_depth = int(df["len"].quantile(0.6))
    text_depth = int(pos_depth // 3)
    return df["tokens"], text_depth, pos_depth


# https://stackoverflow.com/a/48316236
def shiftToken(i, seq):
    return (el for j, el in enumerate(seq) if j >= i)


def n_grams(seq, n=1):
    """Returns an itirator over the n-grams given a listTokens"""
    shiftedTokens = (shiftToken(i, seq) for i in range(n))
    tupleNGrams = zip(*shiftedTokens)
    return tupleNGrams


def range_ngrams(listTokens, ngramRange=(1, 2)):
    """Returns an itirator over all n-grams for n in range(ngramRange) given a listTokens."""
    return chain(*(n_grams(listTokens, i) for i in range(*ngramRange)))


def build_models(tokens, text_depth, pos_depth):
    text_model = Model(text_depth)
    pos_model = Model(pos_depth)

    for tokens in tokens:
        words = list(map(lambda t: t.surface, tokens))
        postags = list(map(lambda t: t.part_of_speech, tokens))

        text_ngrams = range_ngrams(
            list(zip(words, postags)), ngramRange=(2, text_depth + 1)
        )
        text_model.add_ngrams(
            text_ngrams, key_transform=lambda y: tuple(map(lambda x: x[0], y))
        )

        pos_ngrams = range_ngrams(postags, ngramRange=(2, pos_depth + 1))
        pos_model.add_ngrams(pos_ngrams)

    text_model.normalise()
    pos_model.normalise()

    return text_model, pos_model


def choose(choices):
    keys = list(choices.keys())
    weights = list(choices.values())
    return random.choices(keys, weights, k=1)[0]


def generate_text(text_model, pos_model):
    tokens = ["<start>"]
    postags = ["<start>,*,*,*"]
    while tokens[-1] != "<end>":
        for try_pos_depth, try_text_depth in reversed(
            list(
                product(
                    range(pos_model.depth - 1, 0, -1),
                    range(text_model.depth - 1, 0, -1),
                )
            )
        ):
            next_token_choices = text_model.next_word_choice(
                tuple(tokens[-try_text_depth:])
            )
            next_pos_choices = deepcopy(
                pos_model.next_word_choice(tuple(postags[-try_pos_depth:]))
            )
            if next_token_choices is None or next_pos_choices is None:
                continue

            while len(next_pos_choices) > 0:
                chosen_pos = choose(next_pos_choices)
                available_token = [
                    s for s, p in next_token_choices if p == chosen_pos
                ]
                if len(available_token) == 0:
                    del next_pos_choices[chosen_pos]
                    continue
                break
            else:
                continue

            tokens.append(random.choice(available_token))
            postags.append(chosen_pos)
            break
        else:
            tokens.append("<end>")
            break

    return re.sub("<start>|<end>", "", "".join(tokens))


def measure_time(task, f, *args, **kwargs):
    start = time.time()
    r = f(*args, **kwargs)
    end = time.time()
    print("[" + task + "]", "time elapsed", end - start)
    return r


# def main():
#     tokens = tokenizer.tokenize("草生えるまんこバズーカRT")
#     for token in tokens:
#         print(token.surface, token.part_of_speech)
#
#     exit(0)
#     tokens, text_depth, pos_depth = measure_time(
#         "data processing", data_preprocessing, data
#     )
#     print(text_depth, pos_depth)
#     text_model, pos_model = measure_time(
#         "build models", build_models, tokens, text_depth, pos_depth
#     )
#     text = ""
#     while text.strip() == "":
#         text = measure_time(
#             "generate text",
#             generate_text,
#             text_model,
#             pos_model,
#         )
#     print(text)
#
#
# main()
