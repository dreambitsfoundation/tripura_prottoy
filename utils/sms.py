import urllib.request
import urllib.parse
import json

def sendSMS(numbers, message):
    apikey = "OhobzvB4fhU-5uViskTsRIn438b4TNBY3KEV41kVtY"
    if len(numbers) < 12:
        numbers = "91" + numbers
    data =  urllib.parse.urlencode({
        'user': 'QuickFixAgartala',
        'password': 'Chevichef@123',
        'sender': 'QIKFIX',
        'GSM': numbers,
        'output': 'json',
        'type': 'longSMS',
        'SMSText' : message
        })
    data = data.encode('utf-8')
    request = urllib.request.Request("http://api.smsbazar.in/api/v3/sendsms/plain?")
    try:
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        return (fr)
    except:
        response = json.dumps({"errors":[{"code":500,"message":"Internal server error. No Reply."}],"status":'failure'}).encode('UTF-8')
        return response