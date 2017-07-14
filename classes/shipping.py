import json, requests, uuid

from classes.logger import logger
log = logger().log


class shipping:
    def __init__(self, x, config):
        self.x          = x
        self.email      = x.split(":")[0]
        self.password   = x.split(":")[1]
        self.config     = config

    def login(self):
        log("Account %s:%s" % (self.email,self.password), "info")

        nikeLoginHeader = {
            'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
        }
        s               = requests.Session()
        s.headers.update(nikeLoginHeader)


        loginData = {
            'client_id' : 'HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH',
            'grant_type': 'password',
            'password'  : self.password,
            'username'  : self.email,
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
        addingAddressData = {
            "address"     : {"shipping": {"preferred":True,
            "type"        : "shipping",
            "name"        : {"primary":{"given": self.config['shipping']['FirstName'], 
            "family"      : self.config['shipping']['LastName']}}, 
            "line1"       : self.config['shipping']['AddressLine1'],
            "line2"       : self.config['shipping']['AddressLine2'],
            "locality"    : self.config['shipping']['City'],
            "province"    : self.config['shipping']['State'],
            "code"        : self.config['shipping']['Zipcode'],
            "country"     : self.config['shipping']['Country'],
            "phone"       : {"primary": self.config['shipping']['PhoneNumber']},
            "label"       : "shipping_1",
            "guid"        : str(uuid.uuid4())}}}

        addingAddressHeaders = {
            "Authorization": ("Bearer "+ access_token)
        }
        addingAddress = s.put("https://api.nike.com/user/commerce", json = addingAddressData,headers = addingAddressHeaders)

        if addingAddress.status_code == 200 or addingAddress.status_code == 201 or addingAddress.status_code == 202:
            log("Address added to %s" % (self.email), "success")

        else:
            log("Brother we had an issue", "error")





