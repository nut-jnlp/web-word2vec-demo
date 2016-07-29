#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python web_word2vec_demo.py

オープンキャンパス用デモ
word2vecから、ある入力した単語の類義語を獲得し、それらの関係を主成分分析により可視化する。

Requirement：
-- Python 3
---- bottle
---- matplotlib
---- scikit-learn
---- gensim
-- 日本語フォント(IPAフォントが入手しやすい)
-- あらかじめword2vec作成したモデル
"""

__author__ = "takahashi <takahashi@jnlp.org>"
__version__ = "1"
__date__ = "29 7 2016"


from bottle import route, run, template, get, post, request, static_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from sklearn.decomposition import PCA
from gensim.models import word2vec


## 適宜環境に合わせて書き換える
# word2vecのモデル
WORD2VEC_MODEL_PATH = './org_wakati.bin'
# matplotlibで日本語を表示するためのIPAゴシックフォント
font = FontProperties(fname='./ipagp.ttf')
TEXT_KW = dict(fontsize=16, fontweight='bold', fontproperties=font)

print("Now loading word2vec model....")
data = word2vec.Word2Vec.load_word2vec_format(WORD2VEC_MODEL_PATH, binary=True)

@route('/word2vec')
def introduction():
    filename='{}.png'.format("学校")
    return template('show_plot.tpl', filename=filename)

@post('/word2vec')
def demonstration():
    word = request.forms.decode().get('word')
    filename='{}.png'.format(word)
    return template('show_plot.tpl', filename=filename)

@route('/images/<filename:re:.*\.png>')
def make_image(filename):
    """
    動的に画像ファイルを生成する
    テンプレートから/images/.*.pngにアクセスがあったときに、ファイル名を元にグラフを生成。
    """
    target_word = filename.split(".")[0]
    # 例外となる入力の処理。見つからない場合は、not_found.pngを表示
    if len(target_word) > 2 or filename == "not_found.png":
        return static_file('./not_found.png', root='./images', mimetype='image/png')

    # word2vecに入力された単語が存在するかどうか確認
    try:
        data[target_word]
    except:
        return static_file('./not_found.png', root='./images', mimetype='image/png')

    save_graph(target_word, filename)

    return static_file(filename, root='./images', mimetype='image/png')

def save_graph(target_word, filename):
    """
    ある単語に対して、類義語を取得しグラフに描画
    グラフを保存
    """
    # word2vecから類義語を獲得
    vec_japan = data[target_word]
    sim_japan = data.most_similar(positive=target_word)

    # 類似した単語のベクトル成分を取得
    vec = dict()
    for w, s in sim_japan:
        vec[w] = data[w]

    # ラベルを作成
    word_indexes = [target_word] + [w for w, s in sim_japan]

    # 主成分分析するデータを抽出
    X = data[word_indexes]

    # 主成分分析により2次元に圧縮
    pca = PCA(n_components=2)
    pca.fit(X)

    X = pca.transform(X)
    xs = X[:, 0]
    ys = X[:, 1]

    # plotする
    fig = Figure()  # Plotting
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(xs, ys, marker='o')
    ax.set_title('{}の類義語'.format(target_word), fontproperties=font)

    for i, w in enumerate(word_indexes):
        ax.annotate(
            w,
            xy = (xs[i], ys[i]),
            xytext = (3, 3),
            textcoords = 'offset points',
            ha = 'left',
            va = 'top',
            **TEXT_KW
        )

    # imagesディレクトリ以下に保存
    canvas.print_figure('./images/' + filename)


# webサーバーを走らせる。8080番のtcpアクセスを許可しておくこと。
run(host='0.0.0.0', port=8080, debug=True, reloader=True)
