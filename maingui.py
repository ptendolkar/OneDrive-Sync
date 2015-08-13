#!/usr/bin/python

import sys
import json
import os.path
import time
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

import onedrivegui

from urlparse import parse_qs

import requests
import os
import datetime

from PIL import Image
from StringIO import StringIO

class MainDialog(QDialog, onedrivegui.Ui_Dialog):
	
	print "Loading configurations..."

	if os.path.isfile("config"):
		config = json.loads(open("config").read())
		print "Config file loaded."
	else:
		print "No config file. Make a file title config with a JSON of needed variables, see GitHub page"
		raise

	filepath = config.get("local_filepath")       # local directory to sync files with
	client_secret = config.get("client_secret")   # client secret of your one drive application
	client_id = config.get("client_id")           # client id of you one drive application
	cloud_filepath = config.get("cloud_filepath") # one drive directory containing files to sync (relative to root)
	
	def __init__(self, parent=None):
		super(MainDialog, self).__init__(parent)
		self.setupUi(self)

		self.connect(self.quitButton, SIGNAL("clicked()"), QCoreApplication.instance().quit)
		self.connect(self.tokenButton, SIGNAL("clicked()"), self.getToken)

		self.web = QWebView()
		self.web.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

		self.web2 = QWebView()
		self.web2.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

		self.trayiconmenu = QMenu(self)
		self.notif = QSystemTrayIcon()
		self.notif.show()
		self.notif.setContextMenu(self.trayiconmenu)

		self.connect(self.web, SIGNAL("urlChanged(const QUrl&)"), self.urlChange)
		
		self.tokenurl = QUrl("https://login.live.com/oauth20_authorize.srf")
		self.tokenurl.addQueryItem("client_id", "000000004C155544")
		self.tokenurl.addQueryItem("scope", "wl.signin wl.offline_access onedrive.readonly")
		self.tokenurl.addQueryItem("response_type", "code")
		self.tokenurl.addQueryItem("redirect_uri", "https://login.live.com/oauth20_desktop.srf")

		self.tokenReturnUrl = "https://login.live.com/oauth20_desktop.srf"

		#print self.tokenurl

	def getToken(self):
		self.web.setUrl(self.tokenurl)
		self.web.show()
	
	def searchLocalforCloud(self, cloudCurrFile, localFiles):
		flag = False
		for currFile in localFiles:
			if currFile.encode('UTF-8') == cloudCurrFile:
				flag = True
		return flag

	def downloadFile(self,fileToDownload):
		root = "https://api.onedrive.com/v1.0" 
		command = "/drive/root:/vimwiki/" + fileToDownload  + ":/content" 
		payload = {
				"access_token" : self.access_token
			}
		r = requests.get( root + command, params=payload)
		i = Image.open(StringIO(r.content))
		return i
	
	def modification_date(self,filename):
		t = os.path.getmtime(filename)
		return datetime.datetime.utcfromtimestamp(t)

	def urlChange(self, url):
		urlText = url.toString()
		baseurl = urlText[0:urlText.index("?")]
		
		if baseurl == self.tokenReturnUrl:
			print "Received authentication"
			self.web.hide()
			code_params = urlText[urlText.index("?")+1:]
			b = parse_qs(code_params)

			headers = {'Content-Type': 'application/x-www-form-urlencoded'}

			payload = {
				'client_id': self.client_id, 
				"redirect_uri":self.tokenReturnUrl, 
				"client_secret":self.client_secret, 
				"code":b.get("code")[0],
				"grant_type":"authorization_code"
				}
			self.r = requests.get("https://login.live.com/oauth20_token.srf", headers=headers, params=payload)

			self.access_token = self.r.json().get("access_token")
			self.refresh_token = self.r.json().get("refresh_token")
			
			#automatically write refresh token to file
			file_ = open('refresh_token', 'w')
			file_.write(self.refresh_token)
			file_.close()
			
			#get information on the children of the cloud directory
			payload = {
					"access_token" : self.access_token
				}
			root = "https://api.onedrive.com/v1.0" 
			command = "/drive/root:/" + self.cloud_filepath + ":/children"
			r2 = requests.get(root + command , params=payload)
			
			cloudFiles = r2.json().get("value")
			localFiles = os.listdir(self.filepath)
			
			print "Syncing files..."
			for currFile in cloudFiles:
				dt = currFile.get("lastModifiedDateTime")

				s = currFile.get("name")
				sfull = self.filepath + "/" + s
				if not self.searchLocalforCloud(s, localFiles):
				# check if cloud file exists in local drive
					print "Downloading new file...", s
					i = self.downloadFile(s.decode('UTF-8'))
					i.save(sfull)
				else:
				# compare files to see if there  
					cloudDate = time.strptime(dt,  "%Y-%m-%dT%H:%M:%S.%fZ")
					localDate = self.modification_date(sfull).timetuple()
					if cloudDate > localDate:
						print "Updating file...", s
						r = self.downloadFile(s.decode('UTF-8'))
						i = self.downloadFile(s.decode('UTF-8'))
						i.save(sfull)

			#notify that files were synced
			print "Completed"

app = QApplication(sys.argv)
form = MainDialog()
form.show()
app.exec_()
