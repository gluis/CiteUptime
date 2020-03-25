"""
RunChecker starts the site monitoring
"""

import os
import threading
import time
import yaml
import schedule
from libs.site_db import site_db
from libs.checker import checker
from libs.notifier import notifier


# init in-memory DB
DB = site_db.SiteDB()


def monitor_site(target_site):
    """
    Function to control monitoring
    """
    ckr = checker.Checker(target_site)
    ckr.start()
    # ckr.start_schedule()


def notify():
    """
    Function to handle sending 24 hour success message
    """
    schedule.every().day.at("05:00").do(send_ok_message)
    while True:
        schedule.run_pending()
        time.sleep(1)


def send_ok_message():
    """
    Send success message after formatting message
    """
    sites = DB.get_sites()
    subject = "All is good in the intertubes"
    message = "The following sites have had no errors for 24 hours:\n"
    for name in sites:
        message += name + "\n"
    ntf = notifier.Notifier(subject, message)
    ntf.send()


if __name__ == "__main__":

    # check for logs directory
    DIRS = os.listdir()
    if 'logs' not in DIRS:
        os.mkdir('logs')

    # read config for sites
    with open('config/sites.yaml', 'r') as file:
        SITES = []
        for data in yaml.load_all(file, Loader=yaml.FullLoader):
            SITES.append(data)
            DB.add_site(data['name'])

    for site in SITES:
        t = threading.Thread(group=None, target=monitor_site, args=(
            site,), daemon=False, name=site["name"])
        t.start()

    NOTIFY_THREAD = threading.Thread(group=None, target=notify,
                                     args=(), daemon=False, name="success_notifier")
    NOTIFY_THREAD.start()
