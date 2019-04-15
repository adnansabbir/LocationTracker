import requests

def get_lat_long():
    r = requests.get(url='http://ipinfo.io/json')
    data = r.json()
    return data['loc']

import os
import platform

print(platform.system())

