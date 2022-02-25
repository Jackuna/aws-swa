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
    
class load_okta_list_user_modules():
    def __init__(self):
        pass
    
    def invoke_req(self):
        global value
    
        response = requests.get(apiurl+operation, headers=headers, verify=False)
        #print (response.json())
        #print((event['pathParameters']['proxy']))
        value = response.json()
        return value
            
    def get_current_user(self):
        global operation
            
        operation = 'api/v1/users/me'
        return self.invoke_req()
    
    def list_users(self, limit):
        global operation
    
        operation = 'api/v1/users?limit='+str(limit)
        return self.invoke_req()
    
    def get_user(self, userId):
        global operation
    
        operation = 'api/v1/users/'+userId
        return self.invoke_req()
        
