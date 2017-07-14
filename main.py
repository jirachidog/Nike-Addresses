import os.path, json, requests, emoji

from classes.logger import logger
log = logger().log

log("[@eggins] PyBase initalised. (github.com/eggins/pybase)", "info", showtime = False)
log("-----------@_zruss_-----------", "yellow", showtime = False)
log("         Lets build!", "lightpurple", showtime = False)
print emoji.emojize(':sign_of_the_horns: :cowboy_hat_face: :sign_of_the_horns: :cowboy_hat_face: :sign_of_the_horns: :cowboy_hat_face: :sign_of_the_horns: :cowboy_hat_face: :sign_of_the_horns: :cowboy_hat_face: :sign_of_the_horns: :cowboy_hat_face: :sign_of_the_horns: :cowboy_hat_face: :sign_of_the_horns: :cowboy_hat_face:')

from classes.Nike import Nike

if not os.path.exists("config.json"):
    log("Config.json not found brother!!!", "error")
    log("Exiting...", "error")
    exit()

with open('config.json') as json_data_file:
    config = json.load(json_data_file)
    log("Config loaded", "success")

with open('accounts.txt') as accounts_file:
    accounts = accounts_file.read().splitlines()

def addInfo():

    l = Nike(x, config)
    Login = l.login()

for x in accounts:
    
    addInfo()



