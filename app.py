from crypt import methods
from io import BytesIO
from typing import TypedDict
from flask import Flask, request, abort, send_from_directory, send_file
import werkzeug

app = Flask(__name__)


@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"


Request = TypedDict(
    'Request', {'w': int, 'h': int, 'seed': int, 'scale': int, 'num': int})


@app.route("/body", methods=["GET", "POST"])
def call_post():
    req: Request = request.json
    app.logger.info('request body: %s', req)
    if (req['num'] > 4):
        abort(400)
    return request.method


@app.route('/images/<path:path>', methods=["GET"])
def get_image(path):
    app.logger.info('path: %s', path)
    return send_from_directory('static', path)


@app.route('/bin/<path:path>', methods=["GET"])
def get_image_bin(path):
    app.logger.info('path: %s', path)
    f = open('static/castle.png', 'rb')
    return send_file(
        BytesIO(f.read()),
        mimetype='image/png',
        as_attachment=True,
        download_name='%s.png' % 'download'
    )


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400
