from django.urls import path
from accounts.api.views.registration_view import registration_view
from accounts.api.views.login_view import login_view

urlpatterns = [
    path('register', registration_view, name='register'),
    path('login', login_view, name="login"),
    # path('list', retailer_by_commodities, name="ret"),
]
