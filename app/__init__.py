from flask import Flask


def create_app():
    app = Flask(__name__)
    from app.routes.api import api
    app.register_blueprint(api)

    @app.route("/")
    def home():
        return "<h1>Student Academic Platform</h1><p>See /api/health</p>"

    return app
