import pytz


def parse_timezone_name(naive_datetime, timezone_name):
    tz_name_dict = {}
    for tz_str in pytz.common_timezones:
        tz = pytz.timezone(tz_str)
        localised_datetime = tz.localize(naive_datetime)
        if localised_datetime.tzname() == timezone_name:
            tz_name_dict[localised_datetime.strftime("%z")] = tz

    return list(tz_name_dict.values())
