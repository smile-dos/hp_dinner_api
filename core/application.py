import logging
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from werkzeug import security
import importlib
from core import settings
from utils import auth_jwt
from utils import rpc_client
from utils import constant
from utils import user as utils_user

logger = logging.getLogger(__name__)

rpc_client = rpc_client.RpcProxy(settings.RPC_BROKER_URL)


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


def authenticate(username, password):
    try:
        rpc_msg = rpc_client.select_user_by_username(username=username)
        if rpc_msg["code"] == constant.ErrCode.ERR_OK:
            user_info = rpc_msg["user"]
            user = utils_user.AuthUser()
            for k, v in user_info.items():
                if hasattr(user, k):
                    setattr(user, k, v)
            if security.check_password_hash(pwhash=user.password, password=password) is True:
                return user
            else:
                return
    except Exception:
        return


def identity(payload):
    user_id = payload['identity']
    try:
        rpc_msg = rpc_client.select_user_by_id(user_id=user_id)
        if rpc_msg["code"] == constant.ErrCode.ERR_OK:
            user_info = rpc_msg["user"]
            user = utils_user.AuthUser()
            for k, v in user_info.items():
                if hasattr(user, k):
                    setattr(user, k, v)
            return user
        else:
            return
    except Exception:
        return


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
    # Init jwt
    auth_jwt.JWT(app=app, authentication_handler=authenticate, identity_handler=identity)
    return app
