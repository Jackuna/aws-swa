import json
import requests
from user.create import *
def lambda_handler(event, context):
    
    a = printme()
    c = a.sum(1)
            
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(c)
    }
