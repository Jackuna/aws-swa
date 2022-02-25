import json
import socket


def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.settimeout(1)
      return True
   except:
      time.sleep(1)
      return False
      
def lambda_handler(event, context):
    
    if isOpen('142.250.195.196',443):
        code = 200
    else:
        code = 500


    return {
        'statusCode': code,
        'body': json.dumps("Port status")
    }