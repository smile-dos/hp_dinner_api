from user import views


urlpatterns = [
    # eg: (resource, url)
    # User login
    (views.Login, "/api_v1/user/login/")
]