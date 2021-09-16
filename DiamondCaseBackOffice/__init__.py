from flask import Flask, render_template

def create_app():
    app = Flask(__name__, static_folder='src', static_url_path="/src")

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return render_template('index.html')

    return app