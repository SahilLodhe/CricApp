"""handcricketReset URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from operator import index
from player import views
from django.contrib import admin
from django.urls import path
# from numpy import r_
from django.conf.urls import include
from django.urls import include,path
from player import urls
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
router = routers.DefaultRouter()
router.register('players',views.PlayerView, basename='players')
router.register('iplteams',views.IPLTeamView, basename='iplteams')
router.register('intlteams',views.INTLTeamView, basename='intlteams')
# router.register('users',views.User, basename='users')
# router.register('profileextends',views.ProfileExtendView, basename='profileextends')
# routeriplteams = routers.DefaultRouter()
# routeriplteams.register('iplteams',views.IPLTeamView, basename='iplteams')
# routerintlteams = routers.DefaultRouter()
# routerintlteams.register('intlteams',views.INTLTeamView, basename='intlteams')
# routerusers = routers.DefaultRouter()
# routerusers.register('users',views.UserView, basename='users')
# routerprofileextend = routers.DefaultRouter()
# routerprofileextend.register('profileextends',views.UserView, basename='profileextends')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('player.urls',namespace='player')),
    path('login/',auth_views.LoginView.as_view(template_name="registration/login.html"),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('test/',views.TestPage.as_view(),name='test'),
    path('thanks/',views.ThanksPage.as_view(),name='thanks'),
    path('api/',include(router.urls)),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)