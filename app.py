from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader
import winrate


def wsgi_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)

    engine = Engine(loader=FileLoader(['']), extensions=[CoreExtension()])
    template = engine.get_template('main_template.html')

    player_wins = winrate.download_current_player_wins()
    leaderboard = winrate.compute_win_rate_leaderboard(player_wins)
    ranked_leaderboard = [(str(index + 1), name, "{:.2f}%".format(probability * 100))
                          for index, (name, probability)
                          in enumerate(leaderboard)]

    response_body = template.render({"leaderboard": ranked_leaderboard})

    yield response_body.encode()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('localhost', 5555, wsgi_app)
    httpd.serve_forever()
