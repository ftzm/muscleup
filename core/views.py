
"""
Website and API views for muscleup
"""
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import render, get_object_or_404
from core.models import (
    Exercise,
    Routine,
    RoutineDay,
    Workout,
    Progression,
    ProgressionSlot,
    Set,
    )
from core.serializers import (
    ExerciseSerializer,
    RoutineSerializer,
    RoutineDaySerializer,
    RoutineDaySlotSerializer,
    WorkoutSerializer,
    ProgressionSerializer,
    ProgressionSlotSerializer,
    SetSerializer,
    WorkoutSetSerializer,
    )

class OwndedDetailView(generics.RetrieveUpdateDestroyAPIView):
    query_model = None

    def get_queryset(self):
        user = self.request.user
        return self.query_model.objects.filter(owner=user)

class OwndedListView(generics.ListCreateAPIView):
    query_model = None

    def get_queryset(self):
        user = self.request.user
        return self.query_model.objects.filter(owner=user)

class ExerciseList(OwndedListView):
    """
    API endpoint that allows exercises to be viewed or edited
    """
    query_model = Exercise
    serializer_class = ExerciseSerializer

class ExerciseDetail(OwndedDetailView):
    """
    API endpoint that allows exercises to be viewed or edited
    """
    query_model = Exercise
    serializer_class = ExerciseSerializer

class WorkoutList(OwndedListView):
    """
    API endpoint that allows workouts to be viewed or edited
    """
    query_model = Workout
    serializer_class = WorkoutSerializer

class WorkoutDetail(OwndedDetailView):
    """
    API endpoint that allows workouts to be viewed or edited
    """
    query_model = Workout
    serializer_class = WorkoutSerializer


class SetDetail(OwndedDetailView):
    """
    API endpoint that allows workouts to be viewed or edited
    """
    query_model = Set
    serializer_class = SetSerializer

class ProgressionList(OwndedListView):
    serializer_class = ProgressionSerializer
    query_model = Progression

class ProgressionDetail(OwndedDetailView):
    """Retrieve, update or delete a progression instance"""
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

class RoutineList(OwndedListView):
    serializer_class = RoutineSerializer
    query_model = Routine

class RoutineDetail(OwndedDetailView):
    """Retrieve, update or delete a routine instance"""
    serializer_class = RoutineSerializer
    query_model = Routine

class RoutineDayList(generics.ListCreateAPIView):
    # queryset = RoutineDay.objects.all()
    serializer_class = RoutineDaySerializer

    def get_queryset(self):
        routine = Routine.objects.get(pk=self.kwargs['routine_pk'],
                                              owner=self.request.user)
        return routine.routinedays.all()

    def perform_create(self, serializer):
        routine = Routine.objects.get(pk=self.kwargs['routine_pk'],
                                              owner=self.request.user)
        serializer.save(routine=routine, owner=self.request.user)

class RoutineDayDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoutineDaySerializer

    def get_queryset(self):
        user = self.request.user
        routine = Routine.objects.get(pk=self.kwargs['routine_pk'],
                                      owner=user)
        return routine.routinedays.all()

class RoutineDaySlotList(generics.ListCreateAPIView):
    serializer_class = RoutineDaySlotSerializer

    def get_routineday(self):
        return RoutineDay.objects.get(
            pk=self.kwargs['pk'],
            routine__pk=self.kwargs['routine_pk'],
            )

    def get_queryset(self):
        return self.get_routineday().routinedayslots.all()

    def perform_create(self, serializer):
        routineday = self.get_routineday()
        serializer.save(routineday=routineday, owner=self.request.user)

class RoutineDaySlotDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoutineDaySlotSerializer

    def get_queryset(self):
        user = self.request.user
        routine = Routine.objects.get(pk=self.kwargs['routine_pk'],
                                              owner=user)
        return routine.routinedays.all()

class WorkoutSetList(generics.ListCreateAPIView):
    serializer_class = WorkoutSetSerializer

    def get_queryset(self):
        workout = Workout.objects.get(pk=self.kwargs['pk'],
                                      owner=self.request.user)
        return workout.sets.all()

    def perform_create(self, serializer):
        workout = Workout.objects.get(pk=self.kwargs['pk'],
                                      owner=self.request.user)
        serializer.save(workout=workout, owner=self.request.user)

class WorkoutSetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutSetSerializer

    def get_queryset(self):
        user = self.request.user
        workout = Workout.objects.get(pk=self.kwargs['workout_pk'],
                                      owner=user)
        return workout.sets.all()
