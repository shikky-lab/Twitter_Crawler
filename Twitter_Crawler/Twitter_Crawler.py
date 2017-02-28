#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import configparser
import codecs
from requests_oauthlib import OAuth1Session
import twitter

"""入力がNoneかどうかを判別して，Noneの場合はdefaultを返す"""
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
	inifile = configparser.SafeConfigParser(allow_no_value=True)
	inifile.readfp(codecs.open('./config.ini',"r","utf8"))

	"""アクセストークンの読み込み"""
	ConsumerKey=inifile.get('tokens', 'ConsumerKey')
	ConsumerSecret=inifile.get('tokens', 'ConsumerSecret')
	AccessToken=inifile.get('tokens', 'AccessToken')
	AccessTokenSecret=inifile.get('tokens', 'AccessTokenSecret')

	"""検索パラメータの読み込み"""
	q = inifile.get('params', 'query')
	geocode=none_check(inifile.get,'params', 'geocode')
	lang = none_check(inifile.get,'params', 'lang')
	locale = none_check(inifile.get,'params', 'locale')
	result_type = none_check(inifile.get,'params', 'result_type')
	count = none_check(inifile.get,'params', 'count')
	until = none_check(inifile.get,'params', 'until')
	since_id=none_check(inifile.get,'params', 'since_id')
	max_id=none_check(inifile.get,'params', 'max_id')
	include_entities=none_check(inifile.get,'params', 'include_entities')

	"""検索実行"""
	t=twitter.Twitter(auth=twitter.OAuth(AccessToken, AccessTokenSecret, ConsumerKey, ConsumerSecret))
	datas=t.search.tweets(q=q,geocode=geocode,lang=lang,locale=locale,result_type=result_type,count=count,until=until,since_id=since_id,max_id=max_id,include_entities=include_entities)
	#datas=t.search.tweets(q=q)
	pass

if __name__=="__main__":
	main()