"""unit tests for muscleup core models and functions"""

import datetime
from django.test import TestCase
from core.models import Set
from core.models import Exercise
from core.models import Workout
from core.models import Routine
from core.models import RoutineDay


class ExerciseModelTest(TestCase):

    def test_saving_and_retrieving_exercises(self):
        first_exercise = Exercise()
        first_exercise.name = "Pushup"
        first_exercise.save()

        second_exercise = Exercise()
        second_exercise.name = "Pullup"
        second_exercise.save()

        saved_exercises = Exercise.objects.all()
        self.assertEqual(saved_exercises.count(), 2)

        first_saved_exercise = saved_exercises[0]
        second_saved_exercise = saved_exercises[1]
        self.assertEqual(first_saved_exercise.name, "Pushup")
        self.assertEqual(second_saved_exercise.name, "Pullup")


class WorkoutModelTest(TestCase):

    def test_saving_and_retrieving_workouts(self):
        first_workout = Workout()
        first_workout.name = "Workout One"
        first_workout.save()

        second_workout = Workout()
        second_workout.name = "Workout Two"
        second_workout.save()

        saved_workouts = Workout.objects.all()
        self.assertEqual(saved_workouts.count(), 2)

        first_saved_workout = saved_workouts[0]
        second_saved_workout = saved_workouts[1]
        self.assertEqual(first_saved_workout.name, "Workout One")
        self.assertEqual(first_saved_workout.date, datetime.date.today())
        self.assertEqual(second_saved_workout.name, "Workout Two")


class SetModelTest(TestCase):

    def setUp(self):
        Exercise.objects.create(name="Pushup")
        Exercise.objects.create(name="Pullup")
        Workout.objects.create(name="Bodyweight A")
        Workout.objects.create(name="Bodyweight B")

    def test_saving_and_retrieving_sets(self):
        first_set = Set()
        first_set.reps = 10
        first_set.weight = 10
        first_set.exercise = Exercise.objects.get(name="Pushup")
        first_set.workout = Workout.objects.get(name="Bodyweight A")
        first_set.save()

        second_set = Set()
        second_set.reps = 9
        second_set.weight = 9
        second_set.exercise = Exercise.objects.get(name="Pullup")
        second_set.workout = Workout.objects.get(name="Bodyweight B")
        second_set.save()

        saved_sets = Set.objects.all()
        self.assertEqual(saved_sets.count(), 2)

        first_saved_set = saved_sets[0]
        second_saved_set = saved_sets[1]
        self.assertEqual(first_saved_set.reps, 10)
        self.assertEqual(first_saved_set.weight, 10)
        self.assertEqual(first_saved_set.exercise.name, "Pushup")
        self.assertEqual(first_saved_set.workout.name, "Bodyweight A")
        self.assertEqual(second_saved_set.reps, 9)
        self.assertEqual(second_saved_set.weight, 9)
        self.assertEqual(second_saved_set.exercise.name, "Pullup")
        self.assertEqual(second_saved_set.workout.name, "Bodyweight B")


class RoutineModelTest(TestCase):

    def test_saving_and_retrieving_routine(self):
        first_routine = Routine()
        first_routine.name = "Routine One"
        first_routine.save()

        second_routine = Routine()
        second_routine.name = "Routine Two"
        second_routine.cycle_length = 7
        second_routine.cycle_position = 2
        second_routine.save()

        saved_routines = Routine.objects.all()
        self.assertEqual(saved_routines.count(), 2)

        first_saved_routine = saved_routines[0]
        second_saved_routine = saved_routines[1]
        self.assertEqual(first_saved_routine.name, "Routine One")
        self.assertEqual(second_saved_routine.name, "Routine Two")
        self.assertEqual(second_saved_routine.cycle_length, 7)
        self.assertEqual(second_saved_routine.cycle_position, 2)


class RoutineDayModelTest(TestCase):

    def setUp(self):
        Routine.objects.create(name="Routine One", cycle_length=7,
                               cycle_position=1)

    def test_saving_and_retrieving_routineday(self):
        first_routineday = RoutineDay()
        first_routineday.name = "RoutineDay One"
        first_routineday.routine = Routine.objects.get(name="Routine One")
        first_routineday.save()

        second_routineday = RoutineDay()
        second_routineday.name = "RoutineDay Two"
        next_date = datetime.date.today() + datetime.timedelta(7)
        second_routineday.next_date = next_date
        second_routineday.save()

        saved_routinedays = RoutineDay.objects.all()
        self.assertEqual(saved_routinedays.count(), 2)

        first_saved_routineday = saved_routinedays[0]
        second_saved_routineday = saved_routinedays[1]
        self.assertEqual(first_saved_routineday.name, "RoutineDay One")
        self.assertEqual(second_saved_routineday.name, "RoutineDay Two")
        self.assertEqual(second_saved_routineday.next_date, next_date)


class RoutineDaySlotModelTest(TestCase):
    pass


class ProgressionModelTest(TestCase):
    pass


class ProgressionSlotModelTest(TestCase):
    pass


class ExerciseWorkoutSetTest(TestCase):

    def setUp(self):
        exercise_names = ["Pushup", "Pullup", "Squat", "Plank"]
        exercises = [Exercise.objects.create(name=name)
                     for name in exercise_names]
        workout_names = ["Bodyweight 1", "Bodyweight 2", "Bodyweight 3"]
        workouts = [Workout.objects.create(name=name)
                    for name in workout_names]
        for workout in workouts:
            for exercise in exercises:
                for i in [10, 9, 8]:
                    Set.objects.create(
                        exercise=exercise,
                        reps=i,
                        workout=workout)

    def test_right_number_of_sets(self):
        saved_sets = Set.objects.all()
        self.assertEqual(saved_sets.count(), 36)

    def test_sets_deleted_with_workout(self):
        Workout.objects.get(name="Bodyweight 3").delete()
        saved_sets = Set.objects.all()
        self.assertEqual(saved_sets.count(), 24)

    def test_change_workout_date(self):
        first_workout = Workout.objects.get(name="Bodyweight 1")
        first_workout.date = first_workout.date - datetime.timedelta(1)
        first_workout.save()

        self.assertEqual(
            first_workout.date, datetime.date.today() - datetime.timedelta(1)
            )

        todays_sets = Set.objects.filter(workout__date=datetime.date.today())
        self.assertEqual(todays_sets.count(), 24)
