# CiteUptime

A site monitoring tool written in python to check to see if a site is up and the selected page(s) are responding properly. You can bypass pinging the site initially if the site ignores pings (e.g. some serverless services ignore them). Just set 

    ping: False 

Otherwise, set to 

    ping: True.

### Usage
IMPORTANT UPDATE: only tested with 3.8.0. Singleton pattern used for db won't work
pre 3.7.
You only need to configure it once, then run it. It spawns one thread per site you give it.
You need: 
    1. Access to an smtp server or smpt server account
    2. A site or list of sites you want to monitor
    3. python3

#### Configuration
In config/

Update credentials.yaml with your own credentials:

    from_email: you@example.com
    to_email: someone@example.com
    password: super-secret-password
    server: smtp.example.com
    port: 587

Update sites.yaml with your sites like so:

    ---
    name: example1.com
    ping: True
    paths: 
      - ["/","What we do"], 
      - ["/contact","Contact us"]
    ---
    name: example2.org
    ping: False
    paths: 
      - ["/about","Our mission..."]

Run it with 
```
    python3 run_checker.py &
```

to let it continue after logging off.

### TODO
- Create web interface to manage sites, so more than terminal monkeys can use it
