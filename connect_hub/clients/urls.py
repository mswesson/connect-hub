from django.urls import path

from .views import (
    ClientProfileApiView,
    ClientCreateApiView,
    ClientLoginApiView,
)

app_name = "clients"

urlpatterns = [
    path(
        "register/", ClientCreateApiView.as_view(), name="client_register"
    ),
    path(
        "login/", ClientLoginApiView.as_view(), name="client_login"
    ),
    path(
        "profile/", ClientProfileApiView.as_view(), name="client_profile"
    ),
]
