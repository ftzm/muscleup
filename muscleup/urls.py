"""muscleup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from core import views

api_v1_patterns = [
    url(r'^progressions/$', views.ProgressionList.as_view()),
    url(r'^progressions/(?P<pk>[0-9]+)/$',
        views.ProgressionDetail.as_view(),
        name='progressions-detail'),
    url(r'^progressions/(?P<progression_pk>[0-9]+)/progressionslots/$',
        views.ProgressionSlotList.as_view(),
        name='progressions-progressionslots-list'),
    url(r'^progressions/(?P<progression_pk>[0-9]+)/progressionslots/' \
         '(?P<pk>[0-9]+)/',
        views.ProgressionSlotDetail.as_view(),
        name='progressions-progressionslots-detail'),
]

urlpatterns = [
    url(r'^api-v1/', include(api_v1_patterns)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
