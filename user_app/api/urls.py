from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from. views import registration_view, logout_view

app_name = 'user_app'
urlpatterns = [
    # token authentication
    path('login/', obtain_auth_token, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # jwt authentication
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]