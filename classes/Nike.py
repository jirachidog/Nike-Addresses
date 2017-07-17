import requests, uuid, time

from classes.logger import logger
log = logger().log


class Nike:
    def __init__(self, x, config):
        self.x          = x
        self.email      = x.split(":")[0]
        self.password   = x.split(":")[1]
        self.config     = config

    def login(self):
        log("Account %s:%s" % (self.email,self.password), "info")

        nikeLoginHeader = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
        }
        s               = requests.Session()
        s.headers.update(nikeLoginHeader)


        loginData = {
            'client_id'     : 'PbCREuPr3iaFANEDjtiEzXooFl7mXGQ7',
            'grant_type'    : 'password',
            'keepMeLoggedIn': 'true',
            'password'      : self.password,
            'username'      : self.email,
            'ux_id'         : 'com.nike.commerce.nikedotcom.web'
        }

        log("Attempting login", "info")



        while True:
            login = s.post("https://unite.nike.com/loginWithSetCookie?appVersion=287&experienceVersion=249&uxid=com.nike.commerce.snkrs.web&locale=en_US&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false",json=loginData)
            if login.status_code == 200:
                log("Brother we logged in", "success")
                break
            else:
                log(login.text)
                time.sleep(5)

        access_token  = login.json()['access_token']
        user_id       = login.json()['user_id']
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
        addingAddress = s.put("https://api.nike.com/user/commerce", json = addingAddressData, headers = addingAddressHeaders)

        if addingAddress.status_code == 200 or addingAddress.status_code == 201 or addingAddress.status_code == 202:
            log("Address added to %s" % (self.email), "success")

        else:
            log("Brother we had an issue", "error")

        creditCardInfoID = str(uuid.uuid4())

        cardData = {
            "accountNumber"   : self.config['billing']['CardNumber'],
            "cardType"        : self.config['billing']['CardType'],
            "expirationMonth" : self.config['billing']['ExpirationMonth'],
            "expirationYear"  : self.config['billing']['ExpirationYear'],
            "creditCardInfoId": creditCardInfoID,
            "cvNumber"        : ""
        }

        billingData = {
            "currency" : "USD",
            "isDefault": "true",
            "billingAddress": {"address1"   : self.config['billing']['AddressLine1'],
                               "city"       : self.config['billing']['City'],
                               "country"    : "US",
                               "firstName"  : self.config['billing']['FirstName'],
                               "guid"       : str(uuid.uuid4()),
                               "lastName"   : self.config['billing']['LastName'],
                               "phoneNumber": self.config['billing']['PhoneNumber'],
                               "postalCode" : self.config['billing']['PostalCode'],
                               "state"      : self.config['billing']['State']},
            "creditCardInfoId": creditCardInfoID,
            "type"            : "CreditCard"
        }

        CCUrl = "https://paymentcc.nike.com/creditcardsubmit/%s/store" % (creditCardInfoID)

        addingBilling  = s.post(url = CCUrl, json = cardData, headers = addingAddressHeaders)

        savingBilling = s.post("https://api.nike.com/commerce/storedpayments/consumer/savepayment", json = billingData, headers = addingAddressHeaders)

        if savingBilling.status_code == 200 or savingBilling.status_code == 201 or savingBilling.status_code == 202:
            log("Credit Card added to %s" % (self.email), "success")

        else:
            log("Brother we had an issue", "error")
