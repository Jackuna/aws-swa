import json
from userapi.create_user import *
from userapi.list_user import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def lambda_handler(event, context):

    if (event['httpMethod']) == "POST":
        print(event)
        
        body = json.loads(event['body'])
        construct_paylod = {    
            "profile": {'firstName': body['firstName'],
            "lastName": body['lastName'],
            "email": body['email'],
            "login": body['email']},
            "credentials": {'password': {"value": body['userPassword']}}
            }
        
        s=load_okta_create_user_modules(construct_paylod)
        val = s.create_user_without_cred()
        
    else:
        if (event['httpMethod']) == "GET":
            print(event)
            d = load_okta_list_user_modules()
            
            val = d.get_user((event['pathParameters']['uid']))
            print(val)
        else:
            pass

    return {
        'statusCode': 200,
        'body':  json.dumps(val)
        }