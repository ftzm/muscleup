#pylint: disable=too-many-ancestors

"""
Website and API views for muscleup
"""
from rest_framework import generics
from core.models import (
    Exercise,
    Routine,
    RoutineDay,
    Workout,
    Progression,
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
    ExerciseSetSerializer,
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
            owner=self.request.user
            )

    def get_queryset(self):
        return self.get_routineday().routinedayslots.all()

    def perform_create(self, serializer):
        routineday = self.get_routineday()
        serializer.save(routineday=routineday, owner=self.request.user)

class RoutineDaySlotDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoutineDaySlotSerializer

    def get_routineday(self):
        return RoutineDay.objects.get(
            pk=self.kwargs['routineday_pk'],
            routine__pk=self.kwargs['routine_pk'],
            owner=self.request.user
            )

    def get_queryset(self):
        return self.get_routineday().routinedayslots.all()

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

class ExerciseSetList(generics.ListCreateAPIView):
    serializer_class = ExerciseSetSerializer

    def get_queryset(self):
        exercise = Exercise.objects.get(pk=self.kwargs['pk'],
                                        owner=self.request.user)
        return exercise.sets.all()

    def perform_create(self, serializer):
        exercise = Exercise.objects.get(pk=self.kwargs['pk'],
                                        owner=self.request.user)
        serializer.save(exercise=exercise, owner=self.request.user)

class ExerciseSetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseSetSerializer

    def get_queryset(self):
        user = self.request.user
        exercise = Exercise.objects.get(pk=self.kwargs['exercise_pk'],
                                        owner=user)
        return exercise.sets.all()
