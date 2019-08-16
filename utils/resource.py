import flask_restful
from utils import auth_jwt


class Resource(flask_restful.Resource):
    pass


class JWTResource(flask_restful.Resource):

    method_decorators = [auth_jwt.jwt_required]
