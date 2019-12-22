# !/usr/bin/python

import sys
import subprocess
import smtplib


class ParameterError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SendMail:

    def __init__(self, **kwargs):
        try:
            if len(kwargs) == 7:
                for key, value in kwargs.items():
                    if key == 'from_email':
                        self.__from_email = value
                    if key == 'to_email':
                        self.__to_email = value
                    if key == 'password':
                        self.__password = value
                    if key == 'server':
                        self.__server = value
                    if key == 'port':
                        self.__port = value
                    if key == 'msg':
                        self.__msg = value
                    if key == 'subject':
                        self.__subject = value

                self._add__subject()
                self._smtp__server = smtplib.SMTP(self.__server, self.__port)
                self._smtp__server.starttls()
                self._smtp__server.login(self.__from_email, self.__password)
            else:
                raise ParameterError(
                    'Not enough parameters: from_email, to_email, password, server, port, msg, subject')
        except ParameterError as e:
            print (e.value)
            sys.exit()

    def _add__subject(self):
        self.__msg = "Subject: " + self.__subject + "\n\n" + self.__msg

    def send(self):
        self._smtp__server.sendmail(self.__from_email, self.__to_email, self.__msg)
        self._smtp__server.quit()
