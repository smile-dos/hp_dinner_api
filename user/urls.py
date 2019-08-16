from user import views


urlpatterns = [
    # eg: (resource, url)
    # User login
    (views.Login, "/api_v1/user/login/"),
    # Get User information
    (views.GetUserInfo, "/api_v1/user/info/"),
    # Test
    (views.Test, "/api_v1/user/test/"),
]