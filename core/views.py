
"""
Website and API views for muscleup
"""

from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from core.models import Exercise, Routine, RoutineDay
from core.serializers import ExerciseSerializer, RoutineSerializer, RoutineDaySerializer

class OwnedModelViewSet(viewsets.ModelViewSet):
    """
    Adjustment to ModelViewSet so that the queryset is filter by current user
    and the owner of a model is automatically set to the current user.

    Inheriting classes function like ModelViewSet but must also specify
    query_model which is used in the get_queryset method
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


    def list(self, request, routines_pk=None):
        queryset = RoutineDay.objects.filter(routine=routines_pk)
        serializer = RoutineDaySerializer(queryset, many=True,
            context={'request':request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, routines_pk=None):
        queryset = RoutineDay.objects.filter(pk=pk, routine=routines_pk)
        routineday = get_object_or_404(queryset, pk=pk)
        serializer = RoutineDaySerializer(routineday,
            context={'request':request})
        return Response(serializer.data)
