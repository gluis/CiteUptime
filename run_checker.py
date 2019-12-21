import threading
import checker
import yaml


def monitor_site(site):
    c = checker.Checker(site["name"], site["paths"])
    # c.start()
    c.start_schedule()

if __name__ == "__main__":

    with open('config/sites.yaml', 'r') as file:
        sites = []
        for data in yaml.load_all(file, Loader=yaml.FullLoader):
            sites.append(data)

    for site in sites:        
        t = threading.Thread(group=None, target=monitor_site, args=(site,), daemon=False, name=site["name"])
        t.start()
