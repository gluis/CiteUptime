"""Checker checks for site details"""

import datetime
from urllib.parse import urljoin
import subprocess
import time
import requests
import schedule
from libs.notifier import notifier
from libs.site_db import site_db


class Checker:
    """
    Checks for site presence and checks content on select
    pages. Logs and notifies of failures as they happen.
    Notifies of no issues every 24 hours.
    """

    def __init__(self, site):
        self.__domainname = site["name"]
        self.__paths = site["paths"]
        self.__ping = site["ping"]
        self.__has_errors = False
        self.__database = site_db.SiteDB()

    def __ping_host(self):
        """
        Use OS to ping domain for up check. If ping == False,
        return success (0)
        """
        if self.__ping:
            return subprocess.run(
                ["ping", "-c", "3", self.__domainname],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            ).returncode
        return 0

    def __check_page(self,):
        """
        Retrieve page to check content match.
        Success == check content; Failure == log and notify
        """
        for path, text in self.__paths:
            try:
                schema_fqdn = "https://" + self.__domainname
                url = urljoin(schema_fqdn, path)
                response = requests.get(url, timeout=(3, 27))
                if response.status_code == 200:
                    self.__check_page_content(str(response.content), text)
                else:
                    message = (
                        "[-] Status code: "
                        + str(response.status_code)
                        + " : "
                        + self.__domainname
                    )
                    self.__write_to_log(message=message)
            except requests.exceptions.ConnectionError as err:
                message = "[-] ConnectionError: " + str(err)
                self.__write_to_log(message=message)

    def __check_page_content(self, content, text):
        """
        Content check; write to log if fails
        """
        has_text = content.find(text)
        if has_text == -1:
            message = (
                "[-] Text >>" + text +
                "<< not found on page for " + self.__domainname
            )
            self.__write_to_log(message=message)

    def __write_to_log(self, message="", logtype="error"):
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S-")
        logdate = datetime.datetime.now().strftime("%Y-%m-%d")
        message = "\n" + date + str(message)
        self.__notify_recipient(message, logtype)
        if logtype != "error":
            logfilename = "logs/" + self.__domainname + "-success-" + logdate
            with open(logfilename, "a+") as logfile:
                logfile.write(message)
        else:
            self.__has_errors = True
            self.__database.remove_site(self.__domainname)
            logfilename = "logs/" + self.__domainname + "-error-" + logdate
            with open(logfilename, "a+") as logfile:
                logfile.write(message)

    def __write_success(self):
        if not self.__has_errors:
            self.__write_to_log(
                message="\n[+] All is well in the intertubes : " +
                self.__domainname,
                logtype="success",
            )
        if self.__has_errors:
            self.__database.add_site(self.__domainname)
            self.__has_errors = False

    def __notify_recipient(self, message, logtype):
        if logtype == "error":
            nfr = notifier.Notifier(
                "Errors: CiteUptime for " + self.__domainname, message
            )
        # else:
        #     nfr = notifier.Notifier(
        #         "All good: CiteUptime for " + self.__domainname, message
        #     )
        nfr.send()

    def start(self):
        """Function to run once. Pings, then checks, else writes error."""
        ping_result = self.__ping_host()
        if ping_result == 0:
            self.__check_page()
        else:
            self.__has_errors = True
            self.__write_to_log(message="[-] Ping unsuccessful")

    def start_schedule(self):
        """Function to run on a schedule"""
        schedule.every(15).minutes.do(self.start)
        # schedule.every(60).seconds.do(self.start)
        # schedule.every().day.at("05:00").do(self.__write_success)
        while True:
            schedule.run_pending()
            time.sleep(1)
