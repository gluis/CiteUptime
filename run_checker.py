"""
RunChecker starts the site monitoring
"""

import os
import threading
import yaml
from libs.checker import checker


def monitor_site(target_site):
    """
    Function to control monitoring
    """
    ckr = checker.Checker(target_site["name"], target_site["paths"])
    # c.start()
    ckr.start_schedule()


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

    for site in SITES:
        t = threading.Thread(group=None, target=monitor_site, args=(
            site,), daemon=False, name=site["name"])
        t.start()
