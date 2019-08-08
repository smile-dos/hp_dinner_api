from werkzeug import security
from utils import resource
from user import validator
from core.application import rpc_client
from utils import constant
from utils import auth_jwt
from data_service.database import execption as dbi_exc


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
            print(rpc_msg)
            user_info = rpc_msg["user"]
            pwhash = user_info["password"]
            if security.check_password_hash(pwhash=pwhash, password=password) is True:
                token = auth_jwt._default_jwt_encode_handler(identity=user_info)
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
            import traceback
            traceback.print_exc()
            msg = {
                "code": constant.RestErrCode.ERR_UNKNOWN,
                "message": str(e)
            }
            return msg
