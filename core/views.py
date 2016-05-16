
"""
Website and API views for muscleup
"""
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import render, get_object_or_404
from rest_framework_extensions.mixins import NestedViewSetMixin
from core.models import (
    Exercise,
    Routine,
    RoutineDay,
    Workout,
    Progression,
    ProgressionSlot
    )
from core.serializers import (
    ExerciseSerializer,
    RoutineSerializer,
    RoutineDaySerializer,
    WorkoutSerializer,
    ProgressionSerializer,
    ProgressionSlotSerializer
    )

class OwndedDetailView(generics.RetrieveUpdateDestroyAPIView):
    query_model = None

    def get_queryset(self):
        user = self.request.user
        return self.query_model.objects.filter(owner=user)

class ExerciseDetail(OwndedDetailView):
    """
    API endpoint that allows exercises to be viewed or edited
    """
    query_model = Exercise
    serializer_class = ExerciseSerializer

class WorkoutViewSet(OwnedModelViewSet):
    """
    API endpoint that allows workouts to be viewed or edited
    """
    query_model = Workout
    serializer_class = WorkoutSerializer

class ProgressionList(generics.ListCreateAPIView):
    serializer_class = ProgressionSerializer

    def get_queryset(self):
        user = self.request.user
        return Progression.objects.filter(owner=user)

class ProgressionDetail(OwndedDetailView):
    """
    Retrieve, update or delete a progression instance.
    """
    serializer_class = ProgressionSerializer
    query_model = Progression

class ProgressionSlotList(generics.ListCreateAPIView):
    # queryset = ProgressionSlot.objects.all()
    serializer_class = ProgressionSlotSerializer

    def get_queryset(self):
        progression = Progression.objects.get(pk=self.kwargs['progression_pk'],
                                              owner=self.request.user)
        return progression.progressionslots.all()

    def perform_create(self, serializer):
        progression = Progression.objects.get(pk=self.kwargs['progression_pk'],
                                              owner=self.request.user)
        serializer.save(progression=progression, owner=self.request.user)

class ProgressionSlotDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProgressionSlotSerializer

    def get_queryset(self):
        user = self.request.user
        progression = Progression.objects.get(pk=self.kwargs['progression_pk'],
                                              owner=user)
        return progression.progressionslots.all()
