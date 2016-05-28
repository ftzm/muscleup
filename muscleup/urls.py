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
    url(r'^exercises/$', views.ExerciseList.as_view()),
    url(r'^exercises/(?P<pk>[0-9]+)/$',
        views.ExerciseDetail.as_view(),
        name='exercises-detail'),
    url(r'^exercise/(?P<pk>[0-9]+)/sets/$', views.ExerciseSetList.as_view()),
    url(r'^exercise/(?P<exercise_pk>[0-9]+)/sets/(?P<pk>[0-9]+)/$',
        views.ExerciseSetDetail.as_view(),
        name='exercises-sets-detail'),
    url(r'^workouts/$', views.WorkoutList.as_view()),
    url(r'^workouts/(?P<pk>[0-9]+)/$',
        views.WorkoutDetail.as_view(),
        name='workouts-detail'),
    url(r'^workouts/(?P<pk>[0-9]+)/sets/$', views.WorkoutSetList.as_view()),
    url(r'^workouts/(?P<workout_pk>[0-9]+)/sets/(?P<pk>[0-9]+)/$',
        views.WorkoutSetDetail.as_view(),
        name='workouts-sets-detail'),
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
    url(r'^routines/$', views.RoutineList.as_view()),
    url(r'^routines/(?P<pk>[0-9]+)/$',
        views.RoutineDetail.as_view(),
        name='routines-detail'),
    url(r'^routines/(?P<routine_pk>[0-9]+)/routinedays/$',
        views.RoutineDayList.as_view(),
        name='routines-routineslots-list'),
    url(r'^routines/(?P<routine_pk>[0-9]+)/routinedays/' \
         '(?P<pk>[0-9]+)/$',
        views.RoutineDayDetail.as_view(),
        name='routines-routinedays-detail'),
    url(r'^routines/(?P<routine_pk>[0-9]+)/routinedays/' \
         '(?P<pk>[0-9]+)/slots/$',
        views.RoutineDaySlotList.as_view(),
        name='routines-routinedays-slot-list'),
    url(r'^routines/(?P<routine_pk>[0-9]+)/routinedays/' \
         '(?P<routineday_pk>[0-9]+)/slots/(?P<pk>[0-9]+)/$',
        views.RoutineDaySlotDetail.as_view(),
        name='routines-routinedays-slot-detail'),
]

urlpatterns = [
    url(r'^api-v1/', include(api_v1_patterns)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
