#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Twitter_Crawlerで取得したデータの読み込みサンプル"""

import sys
import configparser
import codecs
import os
import json
import glob

"""設定ファイルの読み込み"""
inifile = configparser.ConfigParser(allow_no_value=True,interpolation=configparser.ExtendedInterpolation())
inifile.readfp(codecs.open('./config.ini',"r","utf8"))

save_dir_path=inifile.get('other_settings', 'save_dir_path')
save_dir_name=inifile.get('other_settings', 'save_dir_name')
save_dir=os.path.join(save_dir_path,save_dir_name)
tweets_paths=glob.glob(save_dir+"/tweets*")

#一つ目のtweet.jsonを読み込み
with codecs.open(tweets_paths[0],"r","utf8") as fi:
	tweet_datas=json.load(fi)

#ツイート者とその内容を表示
for tweet_data in tweet_datas:
	print("user:",tweet_data["user"]["name"],"tweet:",tweet_data["text"])