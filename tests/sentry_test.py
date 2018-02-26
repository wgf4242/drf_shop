from raven import Client

dsn = "xxx"

client = Client(dsn)

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()
