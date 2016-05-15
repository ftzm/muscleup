
"""
Website and API views for muscleup
"""

from rest_framework import viewsets
from django.shortcuts import render
from core.models import Exercise, Routine, RoutineDay
from core.serializers import ExerciseSerializer, RoutineSerializer, RoutineDaySerializer

class OwnedModelViewSet(viewsets.ModelViewSet):
    """
    Adjustment to ModelViewSet so that the queryset is filter by current user
    and the owner of a model is automatically set to the current user.
    """

    query_model = None

    def get_queryset(self):
        user = self.request.user
        return self.query_model.objects.filter(owner=user)


    def perform_create(self, serializer):
        # The request user is set as owner automatically.
        serializer.save(owner=self.request.user)

class ExerciseViewSet(OwnedModelViewSet):
    """
    API endpoint that allows exercises to be viewed or edited
    """
    query_model = Exercise
    serializer_class = ExerciseSerializer

class RoutineViewSet(OwnedModelViewSet):
    """
    API endpoint that allows routines to be viewed or edited
    """
    query_model = Routine
    serializer_class = RoutineSerializer

class RoutineDayViewSet(OwnedModelViewSet):
    """
    API endpoint that allows routinedays to be viewed or edited
    """
    query_model = RoutineDay
    serializer_class = RoutineDaySerializer
