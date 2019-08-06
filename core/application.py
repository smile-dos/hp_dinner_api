import logging
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import importlib
from core import settings


logger = logging.getLogger(__name__)


def load_urls(api):
    if isinstance(api, Api):
        for app in settings.INSTALL_APPS:
            try:
                url_module = importlib.import_module("{}.urls".format(app))
                if hasattr(url_module, "urlpatterns"):
                    urlpatterns = getattr(url_module, "urlpatterns")
                    for urlpattern in urlpatterns:
                        api.add_resource(urlpattern[0], urlpattern[1])
                else:
                    logger.warning("{} urls not found urlpatterns".format(app))
            except ImportError as e:
                logger.warning("{} not found module urls, for reason: {}".format(app, str(e)))
    else:
        logging.error("api is not instance of Api, will exit.")
        exit(-1)


def create_app(name):
    """
    Create a flask application
    :param name: [str] The name of application
    :return:
    """
    app = Flask(name)
    # load settings
    app.config.from_object("core.settings")
    # Init cors
    CORS(app=app, supports_credentials=True)
    # Init api
    api = Api(app=app)
    # load urls
    load_urls(api=api)
    return app
