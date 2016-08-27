import os
import app


STATIC_FILE_DIR = "static/"
MIME_TABLE = {
    '.txt': 'text/plain',
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
}


def content_type(path):
    _, ext = os.path.splitext(path)
    if ext in MIME_TABLE:
        return MIME_TABLE[ext]
    else:
        return "application/octet-stream"


def static_content_app(environ, start_response):
    path = os.path.normpath("." + environ['PATH_INFO'])
    if path.startswith(STATIC_FILE_DIR) and os.path.exists(path):
        file = open(path, 'rb')
        response_body = file.read()
        file.close()

        status = '200 OK'
        response_headers = [('Content-type', content_type(path))]
        start_response(status, response_headers)
        return [response_body]


def switcheroo_app(environ, start_response):
    if environ['PATH_INFO'].startswith('/' + STATIC_FILE_DIR):
        return static_content_app(environ, start_response)
    else:
        return app.wsgi_app(environ, start_response)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('localhost', 5555, switcheroo_app)
    httpd.serve_forever()
