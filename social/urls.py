"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views import generic
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from social import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name="users")
router.register(r'posts', views.PostViewSet, base_name="posts")

urlpatterns = [
    # Model views
    url(r'^api/', include(router.urls, namespace='api')),
    # Rest auth
    url(r'^', include('rest_auth.urls')),
    # Custom Signup/login functionality
    url(r'^sign-up/', views.signup, name="signup_user"),
    # url(r'^login/', views.login, name="login_user"),
    # Admin
    url(r'^admin/', admin.site.urls),
    # Rest auth
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # JWT endpoints
    url(r'^auth-jwt/', obtain_jwt_token, name="token_auth"),
    url(r'^auth-jwt-refresh/', refresh_jwt_token),
    url(r'^auth-jwt-verify/', verify_jwt_token),
]
