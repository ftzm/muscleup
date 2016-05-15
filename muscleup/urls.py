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
from rest_framework_nested import routers
from core import views

#rest_framework_rested router
router = routers.SimpleRouter()
router.register(r'routines', views.RoutineViewSet, 'routines')
router.register(r'routinedays', views.RoutineDayViewSet, 'routinedays')
routines_router = routers.NestedSimpleRouter(router, r'routines', lookup='routines')
routines_router.register(r'routinedays', views.RoutineDayViewSet, 'routinedays')
router.register(r'exercises', views.ExerciseViewSet, 'exercises')

urlpatterns = [
    url(r'^api-v1/', include(router.urls)),
    url(r'^api-v1/', include(routines_router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
