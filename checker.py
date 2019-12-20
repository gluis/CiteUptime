import requests
import datetime
from urllib.parse import urlparse
import subprocess


class Checker:

	def __init__(self, url):
		self.__url = url
		self.__netloc = urlparse(url).netloc

	def __ping_host(self):
		c = subprocess.call(["ping", "-c", "3", self.__netloc], stdout=subprocess.DEVNULL)
		print(c)

	def __check_page(self, path):
		try:
			response = requests.get(self.__url)
			if response.status_code == 200:
				print(response.content)	
			else:
				print(response.status_code)
		except requests.exceptions.ConnectionError as e:
			date = datetime.datetime.now().strftime("%Y-%m-%d-")
			logfilename = self.__netloc + '-error'
			print(date)
			print(logfilename)
			print(str(e))
			# with open(logfilename, "wb") as logfile:
			# 	logfile.writelines(date + ' ' + e)

	def start(self):
		self.__ping_host()


c = Checker('https://theevillemon.com')
c.start()
