def create_app():
    from flask import Flask
    app = Flask(__name__)

    from .routes import bp

    app.register_blueprint(bp)
    return app
