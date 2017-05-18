"""fotogram URL Configuration

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
from django.conf import settings
from django.views.static import serve
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required
from fotogram_app.views import PostListView, NewPostCreate, like_post, create_comment, PostDelete

urlpatterns = [

    # User Related urls
    url(r'^users/login/$', login, {'authentication_form': AuthenticationForm}, name='login'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'},
        name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'),
        name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls',
        namespace='users')),
    url(r'^users/profile/$', login_required(TemplateView.as_view(
        template_name='registration/profile.html')), name='profile'),

    url(r'^$', PostListView.as_view(), name='home'),
    url(r'^newpost/$', NewPostCreate.as_view(), name='newpost'),
    url(r'^userposts/(?P<user_id>\d+)/$', PostListView.as_view(), name='user_posts'),
    url(r'^like/$', like_post, name='like'),
    url(r'^create_comment/(?P<post_id>\d+)/$', create_comment, name='create_comment'),
    url(r'^delete/(?P<pk>\d+)/$', PostDelete.as_view(), name='delete'),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
        urlpatterns += [url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
                        ]
