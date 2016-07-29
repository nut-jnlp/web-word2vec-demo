<html>
  <head>
    <title>Word2Vecで獲得した類義語の関係を知ろう</title>
  </head>
  <body>
    <h1>Word2Vecで獲得した類義語の関係を知ろう</h1>

    <p>入力フォームに単語を入力して、類義語の関係を知ろう</p>
    <p>例：学校, 運動, 音楽, 触る</p>

    <form method="post" action="/word2vec">
      <p> 単語：<input type="text" name="word"> <input type="submit" value="解析する"></p>
    </form>

    <img src="/images/{{filename}}" alt="Image Placeholder">

    <h2>詳しい説明</h2>
    <p>
      「王様-男+女」は何になると思いますか？ <br>
      「女王」になりますよね。 <br>
      このように単語の意味をコンピュータで計算できるようにしたものがWord2Vecです。 <br>
      もう一歩踏み込むと、単語をニューラルネットワークを用いて、ベクトルで表現したものです。 <br>
    </p>

  </body>
</html>
