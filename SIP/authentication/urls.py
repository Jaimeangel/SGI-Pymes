from django.urls import path
from .views import login_view, ObtainAuthTokenView

urlpatterns = [
    path('login', login_view, name='login'),
    path('api-token-auth/', ObtainAuthTokenView.as_view(), name='api_token_auth'),
]
