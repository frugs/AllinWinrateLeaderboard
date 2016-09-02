import urllib.request
import json
import pytz


def determine_local_timezone(ip):
    geo_response = urllib.request.urlopen("http://freegeoip.net/json/" + ip)
    geo_info = json.loads(geo_response.read().decode('utf-8'))

    if 'time_zone' in geo_info:
        tz_str = geo_info['time_zone']
    else:
        tz_str = 'UTC'

    if tz_str in pytz.all_timezones:
        return pytz.timezone(tz_str)
    else:
        return pytz.timezone('UTC')