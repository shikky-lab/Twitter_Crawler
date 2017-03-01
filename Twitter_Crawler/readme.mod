Twitter収集スクリプト(試作)
試作なのでバグが多々あるかもです．．．

できること
・指定キーワードでのtwitter検索
・検索結果をメタデータ混みで保存(json形式)
・過去の収集結果より新しいツイートのみの収集

使用方法
1.Twitterのデベロッパーに登録して，アクセストークン他を取得
2.Twitter_Crawler.pyと同じディレクトリのconfig.iniにアクセストークンや検索設定をセット
3.Twitter_Crawler.pyを実行．

config.iniについて
[tokens]
アクセストークンなどをセット

[search_params]
検索設定をセット．前半はTwitterAPIに直接ポストする値．これらの値の意味は本家APIマニュアルを参照のこと．
後半はTwitter_Crawler独自の変数．
search_count:APIを呼び出す回数．基本は制限以下の値のセットを推奨．
try_interval_sec:APIを呼び出す間に待ち時間(秒)をセット．未設定の場合はインターバルなし．
resent_only:Trueの場合，過去の検索結果より新しいツイートのみを収集(※result_typeがresent以外の動作は保証しない)
	なおsearch_countなどの制約に触れた場合，前回の結果より新しいツイートを全て収集できる保証はない．
	また収集結果は別名で保存されるので，別途統合が必要．

[other_settings]
ファイルの保存場所などその他設定
save_dir_path:収集結果を保存するディレクトリの位置
save_dir_name:そのディレクトリの名前．デフォルト名は[検索ワード]_tweets
