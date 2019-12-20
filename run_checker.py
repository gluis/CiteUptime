import threading
import checker

if __name__ == "__main__":
    c = checker.Checker('nataloo.com', [('/', "Tell us how we can help")])
    c.start()
    # c.start_schedule()
