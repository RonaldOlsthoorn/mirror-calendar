from flaskr import create_app

if __name__ == "__main__":
    # Only for debugging while developing
    create_app().run(host='0.0.0.0', debug=True, port=80)

