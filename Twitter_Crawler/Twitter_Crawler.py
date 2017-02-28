#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import configparser
import codecs
import os
import json
from requests_oauthlib import OAuth1Session
import twitter

"""変数が存在するかどうか確認し，なければデフォルト値を返す"""
def none_check(func,*args):
	value=''
	try:
		value=func(*args)
	except configparser.NoOptionError:
		pass
	except:
		pass
	return value

def main():
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

	search_count=inifile.getint('search_params', 'search_count')

	"""検索実行"""
	t=twitter.Twitter(auth=twitter.OAuth(AccessToken, AccessTokenSecret, ConsumerKey, ConsumerSecret),retry=10)
	all_datas=[]
	for i in range(search_count):
		try:
			datas=t.search.tweets(q=q,geocode=geocode,lang=lang,locale=locale,result_type=result_type,count=count,until=until,since_id=since_id,max_id=max_id,include_entities=include_entities)
		except:
			print("except occered")
			break
		if datas["statuses"] == []:
			break
		max_id=datas["statuses"][-1]["id"]
		all_datas.extend(datas["statuses"])

	"""保存"""
	save_dir_path=inifile.get('other_settings', 'save_dir_path')
	save_dir_name=inifile.get('other_settings', 'save_dir_name')
	#print (save_dir_name)
	save_dir=os.path.join(save_dir_path,save_dir_name)
	if not os.path.exists(save_dir):
		os.mkdir(save_dir)

	with codecs.open(os.path.join(save_dir,"tweets.json"),"w","utf8") as fo:
		json.dump(all_datas,fo,indent=4,ensure_ascii=False)

if __name__=="__main__":
	main()