"""
Notifier contacts remote smtp server
"""

import threading
import yaml
import libs.notifier.send_mail as send_mail


class Notifier:
    """
    Notifier sends message
    """

    def __init__(self, subject, message):
        with open('config/.credentials.yaml', 'r') as file:
            self.__server_params = yaml.load(file, Loader=yaml.FullLoader)

        self.__subject = subject
        self.__message = message

    def __notify_send(self):
        to_email = self.__server_params['to_email']
        from_email = self.__server_params['from_email']
        password = self.__server_params['password']
        server = self.__server_params['server']
        port = self.__server_params['port']
        subject = self.__subject
        message = self.__message
        sm_server = send_mail.SendMail(from_email=from_email, to_email=to_email,
                                       password=password, server=server,
                                       port=port, msg=message, subject=subject)
        sm_server.send()

    def __notify(self):
        __mail_sender = threading.Thread(target=self.__notify_send)
        __mail_sender.isDaemon = True
        __mail_sender.start()

    def send(self):
        """Public method to send"""
        self.__notify()
