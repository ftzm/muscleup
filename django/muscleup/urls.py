"""muscleup URL Configuration

The `urlpatterns` list routes URLs to api_views. For more info please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function api_views
    1. Add an import:  from my_app import api_views
    2. Add a URL to urlpatterns:  url(r'^$', api_views.home, name='home')
Class-based api_views
    1. Add an import:  from other_app.api_views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from core.views import api_views, web_views

api_v1_patterns = [
    url(r'^exercises/$', api_views.ExerciseList.as_view()),
    url(r'^exercises/(?P<pk>[0-9]+)/$',
        api_views.ExerciseDetail.as_view(),
        name='exercises-detail'),
    url(r'^upgrades/$', api_views.UpgradeList.as_view()),
    url(r'^upgrades/(?P<pk>[0-9]+)/$',
        api_views.UpgradeDetail.as_view(),
        name='upgrades-detail'),
    url(r'^exercises/(?P<pk>[0-9]+)/sets/$',
        api_views.ExerciseSetList.as_view()),
    url(r'^exercises/(?P<exercise_pk>[0-9]+)/sets/(?P<pk>[0-9]+)/$',
        api_views.ExerciseSetDetail.as_view(),
        name='exercises-sets-detail'),
    url(r'^workouts/$', api_views.WorkoutList.as_view()),
    url(r'^workouts/(?P<pk>[0-9]+)/$',
        api_views.WorkoutDetail.as_view(),
        name='workouts-detail'),
    url(r'^workouts/(?P<pk>[0-9]+)/sets/$', api_views.WorkoutSetList.as_view()),
    url(r'^workouts/(?P<workout_pk>[0-9]+)/sets/(?P<pk>[0-9]+)/$',
        api_views.WorkoutSetDetail.as_view(),
        name='workouts-sets-detail'),
    url(r'^progressions/$', api_views.ProgressionList.as_view()),
    url(r'^progressions/(?P<pk>[0-9]+)/$',
        api_views.ProgressionDetail.as_view(),
        name='progressions-detail'),
    url(r'^progressions/(?P<progression_pk>[0-9]+)/progressionslots/$',
        api_views.ProgressionSlotList.as_view(),
        name='progressions-progressionslots-list'),
    url(r'^progressions/(?P<progression_pk>[0-9]+)/progressionslots/' \
         '(?P<pk>[0-9]+)/',
        api_views.ProgressionSlotDetail.as_view(),
        name='progressions-progressionslots-detail'),
    url(r'^routines/$', api_views.RoutineList.as_view()),
    url(r'^routinesexpanded/$', api_views.RoutineListExpanded.as_view()),
    url(r'^routines/(?P<pk>[0-9]+)/$',
        api_views.RoutineDetail.as_view(),
        name='routines-detail'),
    url(r'^routines/(?P<routine_pk>[0-9]+)/routinedays/$',
        api_views.RoutineDayList.as_view(),
        name='routines-routineslots-list'),
    url(r'^routines/(?P<routine_pk>[0-9]+)/routinedays/' \
         '(?P<pk>[0-9]+)/$',
        api_views.RoutineDayDetail.as_view(),
        name='routines-routinedays-detail'),
    url(r'^routines/(?P<routine_pk>[0-9]+)/routinedays/' \
         '(?P<pk>[0-9]+)/slots/$',
        api_views.RoutineDaySlotList.as_view(),
        name='routines-routinedays-slot-list'),
    url(r'^routines/(?P<routine_pk>[0-9]+)/routinedays/' \
         '(?P<routineday_pk>[0-9]+)/slots/(?P<pk>[0-9]+)/$',
        api_views.RoutineDaySlotDetail.as_view(),
        name='routines-routinedays-slot-detail'),
]

urlpatterns = [
    url(r'^api-v1/', include(api_v1_patterns)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^progress/$', web_views.Progress.as_view(), name='progress'),
    url(r'^exercises/$', web_views.Exercises.as_view(), name='exercises'),
    url(r'^add_exercise/$', web_views.AddExercise.as_view(),
        name='add_exercise'),
    url(r'^routines/$', web_views.Routines.as_view(), name='routines'),
    url(r'^delete_exercise/(?P<pk>[0-9]+)/$',
        web_views.DeleteExercise.as_view(),
        name='delete_exercise'),
    url(r'^delete_routine/(?P<pk>[0-9]+)/$',
        web_views.DeleteRoutine.as_view(),
        name='delete_routine'),
    url(r'^add_routinedayslot/$',
        web_views.AddRoutinedayslot.as_view(),
        name='add_routinedayslot'),
    url(r'^delete_routinedayslot/(?P<pk>[0-9]+)/$',
        web_views.DeleteRoutinedayslot.as_view(),
        name='delete_routinedayslot'),
    url(r'^login/$', web_views.Login.as_view(), name='login'),
    url(r'^logout/$', web_views.Logout.as_view(), name='logout'),
    url(r'^$', web_views.Home.as_view(), name='home'),
    #java authentication token
    url(r'^api-token-auth/', obtain_jwt_token),
    ]
