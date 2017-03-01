#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import configparser
import codecs
import os
import json
from requests_oauthlib import OAuth1Session
import twitter
import glob
import re
import time
import urllib.parse

def none_check(func,*args,default=''):
	"""
	関数がエラー終了した際のラッピング．失敗した際にデフォルト値を返す．
	@arg
		func:実際に実行する関数
		*args:その関数に渡す引数
		default:その関数がエラー終了した際に返す値
	@ret
		関数が実行可能だった場合はその結果．エラー終了した場合はデフォルト値
	"""
	value=default
	try:
		value=func(*args)
	except configparser.NoOptionError:
		pass
	except:
		pass
	return value

def sort_nicely( l ): 
	""" Sort the given list in the way that humans expect. """ 
	convert = lambda text: int(text) if text.isdigit() else text 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	l.sort( key=alphanum_key )

def main():
	"""設定ファイルの読み込み"""
	inifile = configparser.ConfigParser(allow_no_value=True,interpolation=configparser.ExtendedInterpolation())
	inifile.readfp(codecs.open('./config.ini',"r","utf8"))

	"""アクセストークンの読み込み"""
	ConsumerKey=inifile.get('tokens', 'ConsumerKey')
	ConsumerSecret=inifile.get('tokens', 'ConsumerSecret')
	AccessToken=inifile.get('tokens', 'AccessToken')
	AccessTokenSecret=inifile.get('tokens', 'AccessTokenSecret')

	"""検索パラメータの読み込み"""
	q = inifile.get('search_params', 'query')
	geocode=none_check(inifile.get,'search_params', 'geocode')
	lang = none_check(inifile.get,'search_params', 'lang')
	locale = none_check(inifile.get,'search_params', 'locale')
	result_type = none_check(inifile.get,'search_params', 'result_type')
	count = none_check(inifile.get,'search_params', 'count')
	until = none_check(inifile.get,'search_params', 'until')
	since_id=none_check(inifile.get,'search_params', 'since_id')
	max_id=none_check(inifile.get,'search_params', 'max_id')
	include_entities=none_check(inifile.get,'search_params', 'include_entities')
	"""検索パラメータ(非ポスト)の読み込み"""
	search_count=none_check(inifile.getint,'search_params', 'search_count',default=1)
	try_interval_sec=none_check(inifile.getint,'search_params', 'try_interval_sec',default=0)
	resent_only=none_check(inifile.getboolean,'search_params', 'resent_only',default=True)

	"""過去データの確認(保存tweetsのjsonのうち，最も末尾番号の新しいものを取得)"""
	save_dir_path=inifile.get('other_settings', 'save_dir_path')
	save_dir_name=inifile.get('other_settings', 'save_dir_name')
	save_dir=os.path.join(save_dir_path,save_dir_name)
	tweets_no=1#今回収集する結果の通し番号．過去データを参照する場合，それらの中の最大の数字+1に書き換えられる.
	if resent_only is True:
		if os.path.exists(save_dir):
			tweets_paths=glob.glob(save_dir+"/tweets*")
			sort_nicely(tweets_paths)
			with codecs.open(tweets_paths[-1],"r","utf8") as fi:
				last_tweets=json.load(fi)
			since_id=last_tweets[0]["id"]
			tweets_no= int(re.findall('([0-9]+)', tweets_paths[-1])[-1])
		else:
			print("past data is not exit.exect normal collection")

	"""検索実行"""
	t=twitter.Twitter(auth=twitter.OAuth(AccessToken, AccessTokenSecret, ConsumerKey, ConsumerSecret),retry=10)
	all_datas=[]
	for i in range(search_count):
		try:
			datas=t.search.tweets(q=q,geocode=geocode,lang=lang,locale=locale,result_type=result_type,count=count,until=until,since_id=since_id,max_id=max_id,include_entities=include_entities)
		except Exception as e:
			print(e)
			break
		if datas["statuses"] == []:
			break
		next_param=datas["search_metadata"]["next_results"][1:]#次の検索パラメータの取得．[1:]は先頭の「?」記号を除去するため
		max_id=urllib.parse.parse_qs(next_param)["max_id"][0]
		max_id=str(int(max_id)+1)#検索はmax_id未満に対して行うため，+1する
		#max_id=datas["statuses"][-1]["id"]#収集したデータからmax_idを直接取得する場合．
		all_datas.extend(datas["statuses"])
		print("collected %d tweets"%len(all_datas))
		time.sleep(try_interval_sec)

	"""結果の保存"""
	if not os.path.exists(save_dir):
		os.mkdir(save_dir)
	with codecs.open(os.path.join(save_dir,"tweets"+str(tweets_no)+".json"),"w","utf8") as fo:
		json.dump(all_datas,fo,indent=4,ensure_ascii=False)

if __name__=="__main__":
	main()