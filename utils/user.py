class BaseUser:

    is_auth = False
    is_anonymous = False


class AnonymousUser(BaseUser):
    is_auth = False
    is_anonymous = True


class AuthUser(BaseUser):
    id = None
    username = None
    password = None
    is_superuser = False
    is_active = False
    email = None
    phone = None
    contactor = None
    realname = None
    avatar = None
    service_serial = None
    is_modify_username = False
    is_vip = False
    vip_id = None
    is_auth = True
    is_anonymous = False
