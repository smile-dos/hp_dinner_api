from user import views


urlpatterns = [
    # eg: (resource, url)
    # User login
    (views.Login, "/api_v1/user/login/"),
    # Get User information
    (views.GetUserInfo, "/api_v1/user/info/"),
    # Get user list by page
    (views.GetUserList, "/api_v1/user/list/"),
    # Test
    (views.Test, "/api_v1/user/test/"),
]