import os.path, json, requests

from classes.logger import logger
log = logger().log

log("[@eggins] PyBase initalised. (github.com/eggins/pybase)", "info")
log("-----------@_zruss_-----------", "yellow")
log("\t\t\t Lets build!", "lightpurple")
from classes.shipping import shipping

if not os.path.exists("config.json"):
    log("Config.json not found brother!!!", "error")
    log("Exiting...", "error")
    exit()

with open('config.json') as json_data_file:
    config = json.load(json_data_file)
    log("Config loaded", "success")

with open('accounts.txt') as accounts_file:
    accounts = accounts_file.read().splitlines()

def addShippingAddress():

    l = shipping(email, password)
    Login = l.login(email, password, config)

for x in accounts:
    email, password = x.split(':')
    addShippingAddress()



