from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from game import Game
from dotenv import load_dotenv
from os import environ
load_dotenv()

STOCKFISH_PATH = environ.get("stockfish-path")
VERSION = "1.0"

app = Flask(__name__)
app.config["DEBUG"] = True
limiter = Limiter(app, key_func=get_remote_address)
CORS(app)


@app.route('/status')
@limiter.limit("1/second")
def status():
    return f'whitecape {VERSION}'


@app.route('/best-move', methods=['POST'])
@limiter.limit("1/second")
def best_move():
    try:
        steps = request.get_json(force=True)
        game = Game(STOCKFISH_PATH, Game.sanToUciSteps(steps))
        return ok_response(game.best_move())
    except Exception:
        return generic_error(3, "Invalid input steps")


@app.errorhandler(404)
def page_not_found(e):
    return generic_error(1, "Invalid endpoint")


@app.errorhandler(400)
def bad_request(e):
    return generic_error(1, "Bad request")


@app.errorhandler(405)
def not_allowed(e):
    return generic_error(2, "Invalid method")


def generic_error(error_code, error_message):
    return {
        "status": "error",
        "errorCode": error_code,
        "errorMessage": error_message
    }


def ok_response(data):
    return {
        "status": "ok",
        "data": data
    }


def main():
    app.run(threaded=True, use_reloader=True)


if __name__ == "__main__":
    main()
