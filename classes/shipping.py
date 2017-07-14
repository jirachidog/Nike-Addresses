import json, requests, uuid

from classes.logger import logger
log = logger().log


class shipping:
    def __init__(self, email, password):
        self.email    = email
        self.password = password

    def login(self, email, password, config):
        log("Account %s:%s" % (email,password), "info")

        nikeLoginHeaders = {
            'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
        }
        s                = requests.Session()
        s.headers.update(nikeLoginHeaders)


        loginData = {
            'client_id' : 'HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH',
            'grant_type': 'password',
            'password'  : password,
            'username'  : email,
            'ux_id'     : 'com.nike.commerce.nikedotcom.web'
        }

        log("Attempting login", "info")
        login = s.post("https://unite.nike.com/loginWithSetCookie?appVersion=239&experienceVersion=206&uxid=com.nike.commerce.nikedotcom.web&locale=en_US&backendEnvironment=default&browser=Google%20Inc.&os=undefined&mobile=false&native=false", json=loginData)

        if login.status_code == 200:
            log("Brother we logged in", "success")
        else:
            log("Brother login is fucked", "error")

        access_token  = login.json()['access_token']
        log('Adding address to account', "info")
        addingAddress = s.put("https://api.nike.com/user/commerce", json = {"address": {"shipping": {"preferred":True,"type":"shipping","name":{"primary":{"given":config['shipping']['FirstName'], "family": config['shipping']['LastName']}}, "line1": config['shipping']['AddressLine1'],"line2":config['shipping']['AddressLine2'],"locality":config['shipping']['City'],"province":config['shipping']['State'],"code":config['shipping']['Zipcode'],"country":config['shipping']['Country'],"phone":{"primary":config['shipping']['PhoneNumber']},"label":"shipping_1","guid":str(uuid.uuid4())}}},headers={"Authorization":("Bearer "+access_token)})

        if addingAddress.status_code == 200 or addingAddress.status_code == 201 or addingAddress.status_code == 202:
            log("Address added to %s" % (email), "success")

        else:
            log("Brother we had an issue", "error")





