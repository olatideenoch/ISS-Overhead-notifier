import requests
from datetime import datetime
import smtplib
import time
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
ISS_URL = os.getenv("ISS_URL")
URL = os.getenv("URL") 

MY_LAT = float(9.081999) # Your latitude
MY_LONG = float(8.675277) # Your longitude


def is_iss_overhead():
    response = requests.get(url=ISS_URL)
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])


    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT+5  <= iss_latitude <= MY_LAT-5 and MY_LONG+5 <= iss_longitude <= MY_LONG-5:
        return True
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get(URL, params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
        )


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# run the code every 60 seconds.



