import threading
import checker



def monitor_site(site):
    c = checker.Checker(site["name"], site["paths"])
    # c.start()
    c.start_schedule()

if __name__ == "__main__":


    sites = [
      {
        # 'name': 'nataloo.com', 'paths': [('/', "Tell us how we can help")]
        'name': 'nataloo.com', 'paths': [('/', "Tell me how we can help")]
      },
      {
        'name': 'recipeboxkitchen.com', 'paths': [("/", "<title>Recipe Box Kitchen</title>")]
      },
      {
        'name': 'hotpeasnbutter.com', 'paths': [("/", "Music for every nation &amp; generation!")]
      },
      {
        'name': 'eatingfromthegroundup.com', 'paths': [("/", "<title>Eating From the Ground Up")]
      },
      {
        'name': 'theevillemon.com', 'paths': [("/", "Nothing here to see")]
      }
    ]

    for site in sites:        
        t = threading.Thread(group=None, target=monitor_site, args=(site,), daemon=False, name=site["name"])
        t.start()
