from django.urls import path
from .views import login_view, ObtainAuthTokenView,logout_view

urlpatterns = [
    path('login', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api-token-auth/', ObtainAuthTokenView.as_view(), name='api_token_auth'),
]
