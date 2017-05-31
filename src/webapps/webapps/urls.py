"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from grumblr import views
import django.contrib.auth.views

from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^LogIn/', django.contrib.auth.views.login, {'template_name':'grumblr/LogIn.html'}, name='login'),
    url(r'^add-post/', views.add_post),
    url(r'^get-post/', views.get_post),
    url(r'^get-comment/', views.get_comment),
    url(r'^LogOut/', django.contrib.auth.views.logout_then_login, name='SignUp'),
    url(r'^Profile/(?P<id>\w+)/$', views.profile),
    url(r'^Profile/(?P<id>\w+)/ProfileEdit', views.profileEdit),
    url(r'^SignUp/', views.register),
    url(r'^Follower/(?P<id>\w+)/$', views.follow),
    url(r'^addFollower/(?P<id1>\w+)/(?P<id2>\w+)/$', views.addfollow),
    url(r'^deleteFollower/(?P<id1>\w+)/(?P<id2>\w+)/$', views.deletefollow),
    url(r'^confirm/(?P<id>\w+)/$', views.confirm),
    url(r'^changePassword/(?P<id>\w+)/$', views.changePassword),
    url(r'^ForgetPassword/', views.forgetPassword),
    url(r'^add-comment/', views.add_comment),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
