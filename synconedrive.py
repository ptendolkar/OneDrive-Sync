#!/usr/bin/python

import sys
import json
import os.path
import time

import requests
import datetime

from PIL import Image
from StringIO import StringIO

def searchLocalforCloud(cloudCurrFile, localFiles):
	flag = False
	for currFile in localFiles:
		if currFile.encode('UTF-8') == cloudCurrFile:
			flag = True
	return flag

def downloadFile(fileToDownload, access_token):
	root = "https://api.onedrive.com/v1.0" 
	command = "/drive/root:/vimwiki/" + fileToDownload  + ":/content" 
	payload = {
			"access_token" : access_token
		}
	r = requests.get( root + command, params=payload)
	i = Image.open(StringIO(r.content))
	return i

def modification_date(filename):
	t = os.path.getmtime(filename)
	return datetime.datetime.utcfromtimestamp(t)

tokenReturnUrl = "https://login.live.com/oauth20_desktop.srf"
fp = os.path.realpath(__file__)
folderpath = fp[:fp.rfind('/')+1]

print "Loading configurations..."

if os.path.isfile(folderpath + "config"):
	config = json.loads(open(folderpath + "config").read())
	print "Config file loaded."
else:
	raise Exception("No config file. Make a file title config with a JSON of needed variables, see GitHub page")


filepath = config.get("local_filepath")       # local directory to sync files with
client_secret = config.get("client_secret")   # client secret of your one drive application
client_id = config.get("client_id")           # client id of you one drive application
cloud_filepath = config.get("cloud_filepath") # one drive directory containing files to sync (relative to root)

print "Reading refresh token..."

if os.path.isfile(folderpath + "refresh_token"):
	refresh_token = open(folderpath + "refresh_token").read()
else:
	raise ("No refresh_token available. First use the gui program to intialize tokens, see GitHub page")

headers = {'Content-Type': 'application/x-www-form-urlencoded'}

payload = {
	'client_id':client_id, 
	"redirect_uri":tokenReturnUrl, 
	"client_secret":client_secret, 
	"refresh_token":refresh_token,
	"grant_type":"refresh_token"
	}
r = requests.get("https://login.live.com/oauth20_token.srf", headers=headers, params=payload)

access_token = r.json().get("access_token")
refresh_token = r.json().get("refresh_token")

#automatically write refresh token to file
file_ = open(folderpath + 'refresh_token', 'w')
file_.write(refresh_token)
file_.close()

#get information on the children of the cloud directory
payload = {
		"access_token" : access_token
	}
root = "https://api.onedrive.com/v1.0" 
command = "/drive/root:/" + cloud_filepath + ":/children"
r2 = requests.get(root + command , params=payload)

cloudFiles = r2.json().get("value")
localFiles = os.listdir(filepath)

print "Syncing files..."
for currFile in cloudFiles:
	dt = currFile.get("lastModifiedDateTime")

	s = currFile.get("name")
	sfull = filepath + "/" + s
	if not searchLocalforCloud(s, localFiles):
	# check if cloud file exists in local drive
		print "Downloading new file...", s
		i = downloadFile(s.decode('UTF-8'), access_token)
		i.save(sfull)
	else:
	# compare files to see if there  
		cloudDate = time.strptime(dt,  "%Y-%m-%dT%H:%M:%S.%fZ")
		localDate = modification_date(sfull).timetuple()
		if cloudDate > localDate:
			print "Updating file...", s
			r = downloadFile(s.decode('UTF-8'), access_token)
			i = downloadFile(s.decode('UTF-8'), access_token)
			i.save(sfull)

#notify that files were synced
print "Completed"
