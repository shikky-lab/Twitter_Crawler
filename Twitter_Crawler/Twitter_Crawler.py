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

def get_or_setDefault(func,*args,default=''):
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
	geocode=get_or_setDefault(inifile.get,'search_params', 'geocode')
	lang = get_or_setDefault(inifile.get,'search_params', 'lang')
	locale = get_or_setDefault(inifile.get,'search_params', 'locale')
	result_type = get_or_setDefault(inifile.get,'search_params', 'result_type')
	count = get_or_setDefault(inifile.get,'search_params', 'count')
	until = get_or_setDefault(inifile.get,'search_params', 'until')
	since_id=get_or_setDefault(inifile.get,'search_params', 'since_id')
	max_id=get_or_setDefault(inifile.get,'search_params', 'max_id')
	include_entities=get_or_setDefault(inifile.get,'search_params', 'include_entities')
	"""検索パラメータ(非ポスト)の読み込み"""
	search_count=get_or_setDefault(inifile.getint,'search_params', 'search_count',default=1)
	if search_count == 0:
		search_count=True

	"""保存先の設定"""
	save_dir_path=inifile.get('other_settings', 'save_dir_path')
	save_dir_name=inifile.get('other_settings', 'save_dir_name')
	save_dir=os.path.join(save_dir_path,save_dir_name)
	if os.path.exists(save_dir):
		print("target directory exists.please delete or change target name")
		exit()
	tweets_no=1#保存時の通し番号

	"""検索実行"""
	if not os.path.exists(save_dir):
		os.mkdir(save_dir)
	t=twitter.Twitter(auth=twitter.OAuth(AccessToken, AccessTokenSecret, ConsumerKey, ConsumerSecret),retry=True)
	collected_data_count=0
	while search_count:
		try:
			datas=t.search.tweets(q=q,geocode=geocode,lang=lang,locale=locale,result_type=result_type,count=count,until=until,since_id=since_id,max_id=max_id,include_entities=include_entities)
		except Exception as e:
			print(e)
			break
		if datas["statuses"] == []:
			print("there are not tweets")
			break
		with codecs.open(os.path.join(save_dir,"tweets"+str(tweets_no)+".json"),"w","utf8") as fo:
			json.dump(datas["statuses"],fo,indent=4,ensure_ascii=False)
		tweets_no+=1
		collected_data_count+=len(datas["statuses"])
		print("collected %d tweets"%collected_data_count)

		"""次の検索時の最大max_idの設定"""
		max_id=datas["statuses"][-1]["id"]#収集したデータからmax_idを直接取得する．next_paramsはたまに取得できないときがある？
		max_id=str(int(max_id)-1)#検索はmax_id未満に対して行うはずなのだが，なぜか重複するため-1する．
		"""以下，search_metadataを使ったmax_id設定．たまに取得できない事があったため上記方法に切り替えた．"""
		#if "next_results" not in datas["search_metadata"]:
		#	print("there are not next tweet")
		#	break
		#next_param=datas["search_metadata"]["next_results"][1:]#次の検索パラメータの取得．[1:]は先頭の「?」記号を除去するため
		#max_id=urllib.parse.parse_qs(next_param)["max_id"][0]
		#max_id=str(int(max_id)+1)#検索はmax_id未満に対して行うため+1する

		if type(search_count) is int:
			search_count-=1

	if collected_data_count == 0:
		print("target tweets are nothing")

if __name__=="__main__":
	main()
