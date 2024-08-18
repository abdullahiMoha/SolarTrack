"""
This project is build with Pure Python code to solve the solar tracking problem.
it will tell you when the sun rises or the sun falls at your location using API.
"""
import requests
from datetime import datetime

MY_LAT = 2.046934
MY_LONG = 45.318161


def is_iss_overhead():
    response = requests.get(url = "http://api.open-notify.org/iss-now.json")
    response.raise_for_status()  # raising exception if error happens
    data = response.json()  # getting the information from response as json dictionary
    iss_position = data['iss_position']  # getting the location related info

    iss_latitude = float(iss_position['latitude'])
    iss_longitude = float(iss_position['longitude'])
    iss_position = (iss_latitude, iss_longitude)  # getting long and lat of the iss into single tuple

    # To mach ISS location you should be at position of +5 or -5 degree
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    API_URL = " https://api.sunrise-sunset.org/json"
    PARAMETERS = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    response = requests.get(url = API_URL, params = PARAMETERS)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour  # the current hour we are

    if time_now >= sunset or time_now <= sunrise:
        return True


if is_iss_overhead() and is_night():
    print("Look Up.")
else:
    print("Not now.")
