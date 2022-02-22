import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

apiurl='https://dev-50183936-admin.okta.com/'
apikey='009GlRDnyVq7AYmiWlaqgNWZhSFg4QLHVq0r6Y_w2u'

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'SSWS'+apikey
    }

class load_okta_create_user_modules:
    
    def __init__(self,construct_paylod):
        self.construct_paylod = construct_paylod
        
    
    def invoke_req(self):
        global value
        response = requests.post(apiurl+operation, headers=headers, data=json.dumps(self.construct_paylod), verify=False)
        value = response.json()
        return value
        
    def create_user_without_cred(self):
        global operation
            
        operation = 'api/v1/users?activate=true'
        return self.invoke_req()
