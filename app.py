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


def not_found_app(environ, start_response):
    start_response('404 NOT_FOUND', [('Content-type', 'text/plain')])
    yield "Not found".encode()


ROUTES = [
    (r'^$', winrate_app),
    (r'^winrate/?$', winrate_app)
]


def wsgi_app(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in ROUTES:
        match = re.search(regex, path)
        if match is not None:
            return callback(environ, start_response)
    return not_found_app(environ, start_response)
