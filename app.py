import io
import winrate


def wsgi_app(environ, start_response):
    player_wins = winrate.download_current_player_wins()
    leaderboard = winrate.compute_win_rate_leaderboard(player_wins)

    str_buffer = io.StringIO()
    for name, winrate_percentile in leaderboard:
        print(name, winrate_percentile, file=str_buffer)

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    response_body = str_buffer.getvalue()
    yield response_body.encode()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('localhost', 5555, wsgi_app)
    httpd.serve_forever()
