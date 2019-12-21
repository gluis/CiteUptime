import requests
import datetime
from urllib.parse import urljoin
import subprocess
import schedule
import time
import notifier


class Checker:

	def __init__(self, domainname, paths):
		self.__domainname = domainname
		self.__paths = paths
		self.__has_errors = False

	def __ping_host(self):
		return subprocess.run(["ping", "-c", "3", self.__domainname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
		
	def __check_page(self,):
		for path, text in self.__paths:
			try:
				schema_fqdn = "https://" + self.__domainname
				url = urljoin(schema_fqdn, path)
				response = requests.get(url, timeout=(3, 27))
				if response.status_code == 200:
					self.__check_page_content(str(response.content), text)
				else:
					message = '[-] Status code: ' + str(response.status_code) + " : " + self.__domainname
					self.__write_to_log(message=message)
			except requests.exceptions.ConnectionError as e:
				message = "[-] ConnectionError: " + str(e)
				self.__write_to_log(message=message)
	
	def __check_page_content(self, content, text):
		has_text = content.find(text)
		if has_text == -1:
			message = "[-] Text >>"+ text +"<< not found on page for " + self.__domainname
			self.__write_to_log(message=message)

	def __write_to_log(self, message='', logtype='error'):
		date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S-")
		logdate = datetime.datetime.now().strftime("%Y-%m-%d")
		message = '\n' + date + str(message)
		self.__notify_recipient(message)
		if logtype != 'error':
			logfilename = "logs/" + self.__domainname + '-success-' + logdate
			with open(logfilename, "a+") as logfile:
				logfile.write(message)
		else:
			self.__has_errors = True
			logfilename = "logs/" + self.__domainname + '-error-' + logdate
			with open(logfilename, "a+") as logfile:
				logfile.write(message)

	def __write_success(self):
		self.__write_to_log(message='[+] All is well in the intertubes : ' + self.__domainname, logtype='success')

	def __notify_recipient(self, message):
		n = notifier.Notifier('Message from CiteUptime for ' + self.__domainname, message)
		n.send()

	def start(self):
		ping_result = self.__ping_host()
		if ping_result == 0:
			self.__check_page()
		else:
			self.__has_errors = True
			self.__write_to_log(message='[-] Ping unsuccessful')

	def start_schedule(self):
		schedule.every(15).minutes.do(self.start)
		# schedule.every(30).seconds.do(self.start)
		schedule.every().day.at("00:00").do(self.__write_success)
		while True:
			schedule.run_pending()
			time.sleep(1)

