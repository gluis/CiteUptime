# CiteUptime

A site monitoring tool written in python to check to see if a site is up and the selected page(s) are responding properly

### Usage

1. Import checker
2. Init with domain name, then a List of tuples(path,text-to-seek)
This will load the page and look for the text, if the text isn't found, it's assumed there's something wrong and logs are written and the authorities are notified...as they should be when something goes wrong.

```
    import checker

    c = checker.Checker("example.com", [("/","Something on the homepage"),("/contact","Text on the contact page")])
    c.start_schedule()

```

