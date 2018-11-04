import os
import json

from flask import Flask, abort
from flask_cors import CORS
from core import CompositeCalendarFetcher


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_json('config.json')
    else:
        # load the test config if passed in
        app.config.from_json(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    fetcher = CompositeCalendarFetcher.from_json(os.path.join(app.instance_path, "calendars.json"))

    @app.route('/events.json')
    def events():

        try:
            return fetcher.fetch()
        except:
            print("hello")
            abort(402)

    return app


#if __name__ == "__main__":
    # Only for debugging while developing
#    app.run(host='0.0.0.0', debug=True, port=80)