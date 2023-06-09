import requests, smtplib, time
from requests import get
from requests.exceptions import HTTPError
from pushbullet import Pushbullet



print("Checking your public IP")

try:
    response = requests.get('https://api64.ipify.org?format=json')
    jsonResponse = response.json()
    ipresponse = jsonResponse["ip"]


except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')


def checkSites():
        while True:
            siteIPs = []

            try:
                response = requests.get('https://api64.ipify.org?format=json')
                jsonResponse = response.json()
                ipresponse = jsonResponse["ip"]


            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                
            siteIPs.append(ipresponse)
            current_ips = siteIPs
            print("Current IP:", str(current_ips))

            # While the latest check of IPs is equal to the first check (i.e there has been no IP change). This loop will run every 30 seconds
            while siteIPs == current_ips:
                print("No changes found.Checking your public IP again in 30 seconds")
                time.sleep(30)
                print("Checking your public IP again......")
                siteIPs = []
                try:
                    response = requests.get('https://api64.ipify.org?format=json')
                    jsonResponse = response.json()
                    ipresponse = jsonResponse["ip"]
                
                except HTTPError as http_err:
                    print(f'HTTP error occurred: {http_err}')

                siteIPs.append(ipresponse)

            # Once the loop is broken, and a change is detected, find what site's IP was changed.
            print("An IP change was detected! Locating the exact change now.....")
            pushNotification(ipresponse)

            
# Send notification to PushBullet
def pushNotification(content):
    API_KEY = "o.3SdXPspcryST1EKgXxC94JZ4bujrr4tp"
    pb = Pushbullet(API_KEY)
    push = pb.push_note('IP Address has been changed', content)

# Start
if __name__ == '__main__':
    checkSites()
