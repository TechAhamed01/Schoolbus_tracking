"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from users.views import CustomTokenObtainPairView, UserRegistrationView, UserProfileView, LogoutView, ChangePasswordView

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/auth/register/', UserRegistrationView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # User profile
    path('api/users/me/', UserProfileView.as_view(), name='user_profile'),
    
    # API v1
    path('api/v1/', include([
        # Core app
        path('', include('core.urls')),
    ])),
]
