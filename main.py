import requests
from datetime import datetime
import smtplib
import time

#import your own lat and long from latlong

MY_LAT = 45.512230
MY_LONG = -122.658722

#email address to send the notification
EMAIL = 'email@exmaple.com'
PASSWORD = 'longstrongpassword'


#location fo the ISS

def ISS_location():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()
    longitude = float(data['iss_position']['longitude'])
    latitude = float(data['iss_position']['latitude'])
    if longitude == MY_LONG or longitude >= MY_LONG - 5 or longitude <= MY_LONG + 5:
        return True
    if latitude == MY_LAT or latitude >= MY_LAT - 5 or latitude <= MY_LAT + 5:
        return True
    else:
        return False

#Checking to see if its dark where you're located
def is_dark():
    parameters = {
        'lat': MY_LAT,
        'long': MY_LONG,
        'formatted': 0,
    }

    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()

    data = response.json()

    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

    timenow = datetime.now().hour

    if sunset >= timenow or timenow <= sunrise:
        return True


while True:
    time.sleep(60)
    if ISS_location() and is_dark():
        print('look up :)')
        connection = smtplib.SMTP('smtp.example.com')
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg='Subject: Look up :) \n\n ISS is overhead.'
        )
    else:
        print('not overhead :(')
