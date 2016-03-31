"""unit tests for muscleup core models and functions"""

import datetime
from django.test import TestCase
from core.models import Set
from core.models import Exercise
from core.models import Workout
from core.models import Routine
from core.models import RoutineDay
from core.models import RoutineDaySlot

from core.signals import trigger_routinedayslot_gapclose
from unittest.mock import patch


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
    """todo"""

    def test_saving_and_retrieving_routine(self):
        first_routine = Routine()
        first_routine.name = "Routine One"
        first_routine.save()

        second_routine = Routine()
        second_routine.name = "Routine Two"
        second_routine.cycle_length = 7
        second_routine.cycle_position = 2
        second_routine.cycle_last_set = datetime.date.today()
        second_routine.save()

        saved_routines = Routine.objects.all()
        self.assertEqual(saved_routines.count(), 2)

        first_saved_routine = saved_routines[0]
        second_saved_routine = saved_routines[1]
        self.assertEqual(first_saved_routine.name, "Routine One")
        self.assertEqual(second_saved_routine.name, "Routine Two")
        self.assertEqual(second_saved_routine.cycle_length, 7)
        self.assertEqual(second_saved_routine.cycle_position, 2)
        self.assertEqual(second_saved_routine.cycle_last_set,
                         datetime.date.today())

    def test_no_invalid_cycle_position(self):
        first_routine = Routine()
        first_routine.name = "Routine One"
        first_routine.cycle_length = 7
        first_routine.save()

        first_routine.cycle_position = 8
        first_routine.save()

        self.assertEqual(first_routine.cycle_position, 1)

    def test_update_cycle_position(self):
        first_routine = Routine()
        first_routine.name = "Routine One"
        first_routine.cycle_length = 7
        first_routine.cycle_position = 1
        first_routine.cycle_last_set = \
            datetime.date.today() - datetime.timedelta(1)
        first_routine.save()
        second_routine = Routine()
        second_routine.name = "Routine One"
        second_routine.cycle_length = 7
        second_routine.cycle_position = 1
        second_routine.cycle_last_set = \
            datetime.date.today() - datetime.timedelta(15)
        second_routine.save()

        first_routine.update_cycle_position()
        second_routine.update_cycle_position()

        self.assertEqual(first_routine.cycle_position, 2)
        self.assertEqual(first_routine.cycle_last_set, datetime.date.today())
        self.assertEqual(second_routine.cycle_position, 2)
        self.assertEqual(second_routine.cycle_last_set, datetime.date.today())

    def test_keep_cycle_position_inbounds(self):
        first_routine = Routine()
        first_routine.name = "Routine One"
        first_routine.cycle_length = 7
        first_routine.cycle_position = 7

        first_routine.cycle_length = 3

        self.assertEqual(first_routine.cycle_position, 3)

    def test_keep_workoutday_positions_inbounds(self):
        first_routine = Routine()
        first_routine.name = "Routine One"
        first_routine.cycle_length = 7
        first_routine.cycle_position = 1
        first_routine.cycle_last_set = \
            datetime.date.today() - datetime.timedelta(1)
        first_routine.save()
        first_routineday = RoutineDay()
        first_routineday.name = "RoutineDay One"
        first_routineday.routine = Routine.objects.get(name="Routine One")
        first_routineday.position = 7
        first_routineday.save()

        first_routine.cycle_length = 3
        first_routine.save()

        first_routineday = RoutineDay.objects.get(name="RoutineDay One")
        self.assertEqual(first_routineday.position, 3)


class RoutineDayModelTest(TestCase):
    """todo"""

    def setUp(self):
        Routine.objects.create(name="Routine One", cycle_length=7,
                               cycle_position=1)

    def test_saving_and_retrieving_routineday(self):
        first_routineday = RoutineDay()
        first_routineday.name = "RoutineDay One"
        first_routineday.routine = Routine.objects.get(name="Routine One")
        first_routineday.position = 3
        first_routineday.save()

        second_routineday = RoutineDay()
        second_routineday.name = "RoutineDay Two"
        second_routineday.routine = Routine.objects.get(name="Routine One")
        second_routineday.position = 5
        second_routineday.save()

        saved_routinedays = RoutineDay.objects.all()
        self.assertEqual(saved_routinedays.count(), 2)

        first_saved_routineday = saved_routinedays[0]
        second_saved_routineday = saved_routinedays[1]
        self.assertEqual(first_saved_routineday.name, "RoutineDay One")
        self.assertEqual(first_saved_routineday.routine,
                         Routine.objects.get(name="Routine One"))
        self.assertEqual(first_saved_routineday.position, 3)
        self.assertEqual(second_saved_routineday.name, "RoutineDay Two")
        self.assertEqual(second_saved_routineday.routine,
                         Routine.objects.get(name="Routine One"))
        self.assertEqual(second_saved_routineday.position, 5)

    def test_no_invalid_position(self):
        first_routineday = RoutineDay()
        first_routineday.name = "RoutineDay One"
        first_routineday.routine = Routine.objects.get(name="Routine One")
        first_routineday.save()

        first_routineday.position = 9

        self.assertEqual(first_routineday.position, 1)

    def test_assign_exercises_to_routineday(self):
        routineday = RoutineDay(
            name="RoutineDay One",
            routine=Routine.objects.get(name="Routine One"))
        routineday.save()

        exercise = Exercise.objects.create(name="Situp")
        routineday.add_exercise(exercise)

        self.assertEqual(routineday.routinedayslots.count(), 1)
        self.assertEqual(
            routineday.routinedayslots.first().exercise.name, "Situp")

    def test_remove_exercises_from_routineday(self):
        routineday = RoutineDay(
            name="RoutineDay One",
            routine=Routine.objects.get(name="Routine One"))
        routineday.save()
        exercise = Exercise.objects.create(name="Situp")
        routineday.add_exercise(exercise)

        routineday.remove_exercise(exercise.name)

        self.assertEqual(routineday.routinedayslots.count(), 0)


class RoutineDaySlotModelTest(TestCase):
    """todo"""

    def setUp(self):
        first_routine = Routine()
        first_routine.name = "Routine One"
        first_routine.cycle_length = 7
        first_routine.cycle_position = 1
        first_routine.cycle_last_set = \
            datetime.date.today() - datetime.timedelta(1)
        first_routine.save()
        first_routineday = RoutineDay()
        first_routineday.name = "RoutineDay One"
        first_routineday.routine = Routine.objects.get(name="Routine One")
        first_routineday.position = 3
        first_routineday.save()
        first_exercise = Exercise()
        first_exercise.name = "Pushup"
        first_exercise.save()
        second_exercise = Exercise()
        second_exercise.name = "Plank"
        second_exercise.save()
        second_exercise = Exercise()
        second_exercise.name = "Squat"
        second_exercise.save()

    def test_saving_and_retrieving_routinedayslot(self):
        first_routinedayslot = RoutineDaySlot()
        first_routinedayslot.routineday = RoutineDay.objects.get(
            name="RoutineDay One")
        first_routinedayslot.exercise = Exercise.objects.get(name="Pushup")
        first_routinedayslot.save()
        second_routinedayslot = RoutineDaySlot()
        second_routinedayslot.routineday = RoutineDay.objects.get(
            name="RoutineDay One")
        second_routinedayslot.exercise = Exercise.objects.get(name="Plank")
        second_routinedayslot.save()

        saved_routinedayslots = RoutineDaySlot.objects.all()
        self.assertEqual(saved_routinedayslots.count(), 2)
        first_routinedayslot = RoutineDaySlot.objects.all()[0]
        second_routinedayslot = RoutineDaySlot.objects.all()[1]

        self.assertEqual(first_routinedayslot.routineday,
                         RoutineDay.objects.get(name="RoutineDay One"))
        self.assertEqual(second_routinedayslot.routineday,
                         RoutineDay.objects.get(name="RoutineDay One"))
        self.assertEqual(first_routinedayslot.exercise,
                         Exercise.objects.get(name="Pushup"))
        self.assertEqual(second_routinedayslot.exercise,
                         Exercise.objects.get(name="Plank"))
        self.assertEqual(first_routinedayslot.order, 1)
        self.assertEqual(second_routinedayslot.order, 2)

    def test_reordering_slots(self):
        "todo"

        first_routinedayslot = RoutineDaySlot()
        first_routinedayslot.routineday = RoutineDay.objects.get(
            name="RoutineDay One")
        first_routinedayslot.exercise = Exercise.objects.get(name="Pushup")
        first_routinedayslot.save()
        second_routinedayslot = RoutineDaySlot()
        second_routinedayslot.routineday = RoutineDay.objects.get(
            name="RoutineDay One")
        second_routinedayslot.exercise = Exercise.objects.get(name="Plank")
        second_routinedayslot.save()
        third_routinedayslot = RoutineDaySlot()
        third_routinedayslot.routineday = RoutineDay.objects.get(
            name="RoutineDay One")
        third_routinedayslot.exercise = Exercise.objects.get(name="Squat")
        third_routinedayslot.save()

        first_routinedayslot.order = 3
        second_routinedayslot.refresh_from_db()
        third_routinedayslot.refresh_from_db()

        self.assertEqual(first_routinedayslot.order, 3)
        self.assertEqual(second_routinedayslot.order, 1)
        self.assertEqual(third_routinedayslot.order, 2)

        first_routinedayslot.order = 1
        second_routinedayslot.refresh_from_db()
        third_routinedayslot.refresh_from_db()

        self.assertEqual(first_routinedayslot.order, 1)
        self.assertEqual(second_routinedayslot.order, 2)
        self.assertEqual(third_routinedayslot.order, 3)

    def test_remove_slot_gaps_function(self):
        first_routinedayslot = RoutineDaySlot()
        first_routinedayslot.routineday = RoutineDay.objects.get(
            name="RoutineDay One")
        first_routinedayslot.exercise = Exercise.objects.get(name="Pushup")
        first_routinedayslot.save()
        second_routinedayslot = RoutineDaySlot()
        second_routinedayslot.routineday = RoutineDay.objects.get(
            name="RoutineDay One")
        second_routinedayslot.exercise = Exercise.objects.get(name="Plank")
        second_routinedayslot.save()
        third_routinedayslot = RoutineDaySlot()
        third_routinedayslot.routineday = RoutineDay.objects.get(
            name="RoutineDay One")
        third_routinedayslot.exercise = Exercise.objects.get(name="Squat")
        third_routinedayslot.save()

        first_routinedayslot.delete()
        self.assertEqual(RoutineDaySlot.objects.count(), 2)

        second_routinedayslot.refresh_from_db()
        third_routinedayslot.refresh_from_db()

        self.assertEqual(second_routinedayslot.order, 1)
        self.assertEqual(third_routinedayslot.order, 2)


class ProgressionModelTest(TestCase):

    def test_saving_and_retrieving_progression(self):
        pass

    def test_assign_exercise_to_progression(self):
        pass

    def test_remove_exercise_from_progression(self):
        pass


class ProgressionSlotModelTest(TestCase):

    def test_saving_and_retrieving_progressionslot(self):
        pass
        # new slots increase in order number

    def test_ordering_progression_slots(self):
        pass

    def test_no_slot_gaps(self):
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
