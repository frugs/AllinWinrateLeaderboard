import cgi
import datetime
import re

import pytz
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

import timezone
import winrate


def winrate_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)

    engine = Engine(loader=FileLoader(['']), extensions=[CoreExtension()])
    template = engine.get_template('winrate_template.html')

    player_wins = winrate.download_current_player_wins()
    leaderboard = winrate.compute_win_rate_leaderboard(player_wins)
    ranked_leaderboard = [(str(index + 1), name, "{:.2f}%".format(probability * 100))
                          for index, (name, probability)
                          in enumerate(leaderboard)]

    preview_leaderboard = ""
    for rank, name, percentile in ranked_leaderboard[:3]:
        preview_leaderboard += "{}. {} {} ".format(rank, name, percentile)

    response_body = template.render({
        "preview_leaderboard": preview_leaderboard,
        "leaderboard": ranked_leaderboard
    })

    yield response_body.encode()


def timezone_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)

    query_params = cgi.parse_qs(environ.get('QUERY_STRING', ''))

    naive_datetime = datetime.datetime.now()

    remote_tzs = []
    if 'remote_tz' in query_params:
        candidate_tz_str = query_params['remote_tz'][0]
        remote_tzs = timezone.parse_timezone_name(naive_datetime, candidate_tz_str)

    if not remote_tzs:
        remote_tzs = [pytz.timezone('UTC')]

    ip = environ['REMOTE_ADDR']
    local_tz = timezone.determine_local_timezone(ip)

    date_format = "%d %b %H:%M %Z%z"

    result = []
    for remote_tz in remote_tzs:
        remote_datetime = remote_tz.localize(naive_datetime)
        local_datetime = local_tz.normalize(remote_datetime.astimezone(local_tz))

        remote_time = remote_datetime.strftime(date_format)
        local_time = local_datetime.strftime(date_format)

        result.append(remote_time + " " + remote_tz.zone + " is " + local_time + " " + local_tz.zone)

    engine = Engine(loader=FileLoader(['']), extensions=[CoreExtension()])
    template = engine.get_template('timezone_template.html')

    response_body = template.render({
        "result_preview": result[0],
        "result": result
    })

    yield response_body.encode()


def not_found_app(environ, start_response):
    start_response('404 NOT_FOUND', [('Content-type', 'text/plain')])
    yield "Not found".encode()


ROUTES = [
    (r'^winrate/?$', winrate_app),
    (r'^timezone/?$', timezone_app),
    (r'^timezone/.+$', timezone_app)
]


def wsgi_app(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in ROUTES:
        match = re.search(regex, path)
        if match is not None:
            return callback(environ, start_response)
    return not_found_app(environ, start_response)
