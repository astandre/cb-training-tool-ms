import os
from flakon import create_app as _create_app
from .views import blueprints
from flask_cors import CORS

_HERE = os.path.dirname(__file__)
_SETTINGS = os.path.join(_HERE, 'settings.ini')


def create_app(settings=None):
    if settings is None:
        settings = _SETTINGS

    app = _create_app(blueprints=blueprints, settings=settings)
    CORS(app)
    return app
