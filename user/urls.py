from user import views


urlpatterns = [
    # eg: (resource, url)
    (views.Test, "/api_v1/user/test/"),
    # User login
    (views.Login, "/api_v1/user/login/")
]