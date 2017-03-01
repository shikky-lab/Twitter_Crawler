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


"""設定ファイルの読み込み"""
inifile = configparser.ConfigParser(allow_no_value=True,interpolation=configparser.ExtendedInterpolation())
inifile.readfp(codecs.open('./config.ini',"r","utf8"))

save_dir_path=inifile.get('other_settings', 'save_dir_path')
save_dir_name=inifile.get('other_settings', 'save_dir_name')
save_dir=os.path.join(save_dir_path,save_dir_name)
tweets_paths=glob.glob(save_dir+"/tweets*")
with codecs.open(tweets_paths[-1],"r","utf8") as fi:
	last_tweets=json.load(fi)
pass
