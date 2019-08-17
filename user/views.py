from werkzeug import security
from flask import request
from utils import resource
from user import validator
from core.application import rpc_client
from utils import constant
from utils import auth_jwt
from data_service.database import execption as dbi_exc
from utils import user


class Test(resource.JWTResource):

    def get(self):
        return {
            "mesaage": "Hello flask"
        }


class Login(resource.Resource):

    def post(self):
        parser = validator.user_login_parser()
        args = parser.parse_args()
        username = args.get("username")
        password = args.get("password")
        try:
            rpc_msg = rpc_client.select_user_by_username(username=username)
            user_info = rpc_msg["user"]
            pwhash = user_info["password"]
            if security.check_password_hash(pwhash=pwhash, password=password) is True:
                _user_identify = user.create_user_object(user_info=user_info)
                token = auth_jwt._default_jwt_encode_handler(identity=_user_identify)
                msg = {
                    "code": constant.RestErrCode.ERR_OK,
                    "message": "Login success",
                    "token": token.decode()
                }
                return msg
            else:
                msg = {
                    "code": constant.RestErrCode.ERR_PASSWORD_ERROR,
                    "message": "Password wrong"
                }
                return msg
        except dbi_exc.UsernameNotFound:
            msg = {
                "code": constant.RestErrCode.ERR_USERNAME_NOT_FOUND,
                "message": "Username not found."
            }
            return msg
        except Exception as e:
            msg = {
                "code": constant.RestErrCode.ERR_UNKNOWN,
                "message": str(e)
            }
            return msg


class GetUserInfo(resource.JWTResource):

    def get(self):
        auth_user = auth_jwt.current_identity
        try:
            rpc_ret = rpc_client.select_user_by_id(user_id=auth_user.id)
            user_info = rpc_ret["user"]
            roles = []
            if auth_user.is_superuser is True:
                roles.append("admin")
            msg = {
                "code": constant.RestErrCode.ERR_OK,
                "message": "Get user information success",
                "user": {
                    "username": user_info["username"],
                    "roles": roles,
                    "phone": user_info["phone"],
                    "avatar": user_info["avatar"]
                }
            }
            return msg
        except dbi_exc.UsernameNotFound:
            msg = {
                "code": constant.RestErrCode.ERR_USERNAME_NOT_FOUND,
                "message": "Username not found."
            }
            return msg
        except Exception as e:
            msg = {
                "code": constant.RestErrCode.ERR_UNKNOWN,
                "message": str(e)
            }
            return msg


class GetUserList(resource.JWTResource):

    def get(self):
        try:
            page = int(request.args.get("page", 1))
            page_size = int(request.args.get("page_size", 20))
        except (IndexError, ValueError):
            page = 1
            page_size = 20
        sort_name = request.args.get("sort_name", None)
        sort_order = request.args.get("sort_order")
        keyword = request.args.get("keyword", None)
        try:
            rpc_ret = rpc_client.select_user_list_by_page(page=page, page_size=page_size, keyword=keyword,
                                                          sort_name=sort_name, sort_order=sort_order)
            msg = {
                "code": constant.RestErrCode.ERR_OK,
                "message": "Get user list success.",
                "users": rpc_ret
            }
            return msg
        except Exception as e:
            msg = {
                "code": constant.RestErrCode.ERR_UNKNOWN,
                "message": str(e)
            }
            return msg
