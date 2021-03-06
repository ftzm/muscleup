# pylint: disable=C0111
"""unit tests for muscleup core models and functions"""

import datetime
from django.test import TestCase
from core.models import MuscleupUser
from core.models import Set
from core.models import Exercise
from core.models import Workout
from core.models import Routine
from core.models import RoutineDay
from core.models import RoutineDaySlot
from core.models import Progression
from core.models import ProgressionSlot

# importing the signals module gets it running automatically
# complains of being unused since it isn't used explicitly
import core.signals  # pylint: disable=unused-import

def create_user():
    return MuscleupUser.objects.create_user('guy@test.com', 'passward')

def get_user():
    return MuscleupUser.objects.first()

class UserModelTest(TestCase):
    def setUp(self):
        create_user()

    def test_create_user(self):
        self.assertEqual(MuscleupUser.objects.count(), 1)
        self.assertEqual(MuscleupUser.objects.first().email, "guy@test.com")

    def test_verify_password(self):
        self.assertTrue(MuscleupUser.objects.first().check_password('passward'))

class ExerciseModelTest(TestCase):
    def setUp(self):
        create_user()

    def test_saving_and_retrieving_exercises(self):
        user = get_user()
        Exercise.objects.create(name="Pushup", owner=user)
        Exercise.objects.create(name="Pullup", owner=user)

        saved_exercises = user.exercises.all()
        self.assertEqual(saved_exercises.count(), 2)

        first_saved_exercise = saved_exercises[0]
        second_saved_exercise = saved_exercises[1]
        self.assertEqual(first_saved_exercise.name, "Pushup")
        self.assertEqual(second_saved_exercise.name, "Pullup")


class SetModelTest(TestCase):

    def setUp(self):
        user = create_user()
        Exercise.objects.create(name="Pushup", owner=user)
        Exercise.objects.create(name="Pullup", owner=user)
        Workout.objects.create(name="Bodyweight A", owner=user)
        Workout.objects.create(name="Bodyweight B", owner=user)

    def test_saving_and_retrieving_sets(self):
        user = get_user()
        Set.objects.create(owner=user, reps=10, weight=10,
                           exercise=Exercise.objects.get(name="Pushup"),
                           workout=Workout.objects.get(name="Bodyweight A"))
        Set.objects.create(owner=user, reps=9, weight=9,
                           exercise=Exercise.objects.get(name="Pullup"),
                           workout=Workout.objects.get(name="Bodyweight B"))

        saved_sets = user.sets.all()
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

    def setUp(self):
        create_user()

    def test_saving_and_retrieving_routine(self):
        user = get_user()
        Routine.objects.create(owner=user, name="Routine One")
        r2 = Routine.objects.create(owner=user, name="Routine Two", \
            cycle_length=7, cycle_last_set=datetime.date.today())
        r2.cycle_position = 2
        r2.save()

        saved_routines = user.routines.all()
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
        first_routine = Routine.objects.create(name="Routine One", \
            cycle_length=7)

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
        routine = Routine.objects.create(
            name="Routine One",
            cycle_length=7,
            cycle_position=1,
            cycle_last_set=datetime.date.today() - datetime.timedelta(1)
        )
        RoutineDay.objects.create(
            name="RoutineDay One",
            routine=routine,
            position=3
        )
        Exercise.objects.create(name="Pushup")
        Exercise.objects.create(name="Plank")
        Exercise.objects.create(name="Squat")

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
        first_progression = Progression.objects.create(name="handstand")
        second_progression = Progression.objects.create(name="muscleup")

        self.assertEqual(Progression.objects.count(), 2)
        self.assertEqual(first_progression.name, "handstand")
        self.assertEqual(second_progression.name, "muscleup")

    def test_assign_exercises_to_progression(self):
        progression = Progression(name="Progression One",)
        progression.save()

        exercise = Exercise.objects.create(name="Situp")
        progression.add_exercise(exercise)

        self.assertEqual(progression.progressionslots.count(), 1)
        self.assertEqual(
            progression.progressionslots.first().exercise.name, "Situp")

    def test_remove_exercises_from_progression(self):
        progression = Progression(name="Progression One")
        progression.save()

        exercise = Exercise.objects.create(name="Situp")
        progression.add_exercise(exercise)

        progression.remove_exercise(exercise.name)
        self.assertEqual(progression.progressionslots.count(), 0)


class ProgressionSlotModelTest(TestCase):

    def setUp(self):
        Progression.objects.create(name="Handstand")
        Exercise.objects.create(name="Pushup")
        Exercise.objects.create(name="Plank")
        Exercise.objects.create(name="Squat")

    def test_saving_and_retrieving_progressionslot(self):
        first_progressionslot = ProgressionSlot.objects.create(
            progression=Progression.objects.get(name="Handstand"),
            exercise=Exercise.objects.get(name="Pushup"))
        second_progressionslot = ProgressionSlot.objects.create(
            progression=Progression.objects.get(name="Handstand"),
            exercise=Exercise.objects.get(name="Plank"))

        self.assertEqual(ProgressionSlot.objects.count(), 2)
        self.assertEqual(first_progressionslot.exercise,
                         Exercise.objects.get(name="Pushup"))
        self.assertEqual(second_progressionslot.exercise,
                         Exercise.objects.get(name="Plank"))
        self.assertEqual(first_progressionslot.order, 1)
        self.assertEqual(second_progressionslot.order, 2)

    def test_ordering_progression_slots(self):
        first_progressionslot = ProgressionSlot()
        first_progressionslot.progression = Progression.objects.get(
            name="Handstand")
        first_progressionslot.exercise = Exercise.objects.get(name="Pushup")
        first_progressionslot.save()
        second_progressionslot = ProgressionSlot()
        second_progressionslot.progression = Progression.objects.get(
            name="Handstand")
        second_progressionslot.exercise = Exercise.objects.get(name="Plank")
        second_progressionslot.save()
        third_progressionslot = ProgressionSlot()
        third_progressionslot.progression = Progression.objects.get(
            name="Handstand")
        third_progressionslot.exercise = Exercise.objects.get(name="Squat")
        third_progressionslot.save()

        first_progressionslot.order = 3
        second_progressionslot.refresh_from_db()
        third_progressionslot.refresh_from_db()

        self.assertEqual(first_progressionslot.order, 3)
        self.assertEqual(second_progressionslot.order, 1)
        self.assertEqual(third_progressionslot.order, 2)

        first_progressionslot.order = 1
        second_progressionslot.refresh_from_db()
        third_progressionslot.refresh_from_db()

        self.assertEqual(first_progressionslot.order, 1)
        self.assertEqual(second_progressionslot.order, 2)
        self.assertEqual(third_progressionslot.order, 3)

    def test_remove_slot_gaps_function(self):
        first_progressionslot = ProgressionSlot()
        first_progressionslot.progression = Progression.objects.get(
            name="Handstand")
        first_progressionslot.exercise = Exercise.objects.get(name="Pushup")
        first_progressionslot.save()
        second_progressionslot = ProgressionSlot()
        second_progressionslot.progression = Progression.objects.get(
            name="Handstand")
        second_progressionslot.exercise = Exercise.objects.get(name="Plank")
        second_progressionslot.save()
        third_progressionslot = ProgressionSlot()
        third_progressionslot.progression = Progression.objects.get(
            name="Handstand")
        third_progressionslot.exercise = Exercise.objects.get(name="Squat")
        third_progressionslot.save()

        self.assertEqual(first_progressionslot.order, 1)
        self.assertEqual(second_progressionslot.order, 2)
        self.assertEqual(third_progressionslot.order, 3)

        first_progressionslot.delete()
        self.assertEqual(ProgressionSlot.objects.count(), 2)

        second_progressionslot.refresh_from_db()
        third_progressionslot.refresh_from_db()

        self.assertEqual(second_progressionslot.order, 1)
        self.assertEqual(third_progressionslot.order, 2)

    def test_set_current(self):
        progression = Progression.objects.first()
        progressionslots = [ProgressionSlot.objects.create(
            exercise=e, progression=progression)
                            for e in Exercise.objects.all()]

        progressionslots[1].current = True
        progressionslots[1].save()
        progressionslots = progression.progressionslots.all()

        self.assertTrue(progressionslots[1].current)

    def test_only_one_current(self):
        progression = Progression.objects.first()
        progressionslots = [ProgressionSlot.objects.create(
            exercise=e, progression=progression)
                            for e in Exercise.objects.all()]
        progressionslots[0].current = True
        progressionslots[0].save()
        self.assertTrue(progressionslots[0].current)

        progressionslots[1].current = True
        progressionslots[1].save()

        self.assertEqual(ProgressionSlot.objects.
                         filter(_current=True).count(), 1)


class WorkoutModelTest(TestCase):

    def setUp(self):
        first_routine = Routine()
        first_routine.name = "Spring Workout"
        first_routine.cycle_length = 7
        first_routine.cycle_position = 1
        first_routine.cycle_last_set = \
            datetime.date.today() - datetime.timedelta(1)
        first_routine.save()

        first_routineday = RoutineDay()
        first_routineday.name = "A"
        first_routineday.routine = Routine.objects.get(name="Spring Workout")
        first_routineday.position = 7
        first_routineday.save()

        second_routineday = RoutineDay()
        second_routineday.name = "B"
        second_routineday.routine = Routine.objects.get(name="Spring Workout")
        second_routineday.position = 7
        second_routineday.save()

        create_user()

    def test_saving_and_retrieving_workouts(self):
        Workout.objects.create_workout(
            RoutineDay.objects.get(name="A"), get_user())
        Workout.objects.create_workout(
            RoutineDay.objects.get(name="A"), get_user())
        Workout.objects.create_workout(
            RoutineDay.objects.get(name="B"), get_user())
        Workout.objects.create_workout(owner=get_user())

        saved_workouts = Workout.objects.all()
        self.assertEqual(saved_workouts.count(), 4)

        first_saved_workout = saved_workouts[0]
        second_saved_workout = saved_workouts[1]
        third_saved_workout = saved_workouts[2]
        fourth_saved_workout = saved_workouts[3]
        self.assertEqual(first_saved_workout.name, "Spring Workout - A - 1")
        self.assertEqual(first_saved_workout.date, datetime.date.today())
        self.assertEqual(second_saved_workout.name, "Spring Workout - A - 2")
        self.assertEqual(second_saved_workout.date, datetime.date.today())
        self.assertEqual(third_saved_workout.name, "Spring Workout - B - 1")
        self.assertEqual(third_saved_workout.date, datetime.date.today())
        self.assertEqual(fourth_saved_workout.name, "Untitled - 1")
        self.assertEqual(fourth_saved_workout.date, datetime.date.today())


class ExerciseWorkoutSetTest(TestCase):
    def setUp(self):
        first_routine = Routine()
        first_routine.name = "Spring Workout"
        first_routine.cycle_length = 7
        first_routine.cycle_position = 1
        first_routine.cycle_last_set = \
            datetime.date.today() - datetime.timedelta(1)
        first_routine.save()

        first_routineday = RoutineDay()
        first_routineday.name = "A"
        first_routineday.routine = Routine.objects.get(name="Spring Workout")
        first_routineday.position = 7
        first_routineday.save()

        exercise_names = ["Pushup", "Pullup", "Squat", "Plank"]
        exercises = [Exercise.objects.create(name=name)
                     for name in exercise_names]

        create_user()

        for exercise in exercises:
            RoutineDaySlot.objects.create(
                exercise=exercise,
                routineday=first_routineday,
                reps_min=5,
                reps_max=5,
                reps_step=0,
                sets_min=5,
                sets_max=5,
                weight_step=5,
                fail_limit=3
            )

        workouts = [Workout.objects.create_workout(routineday=first_routineday,
                                                   owner=get_user())
                    for i in range(3)]

    def test_right_number_of_sets(self):
        saved_sets = Set.objects.all()
        self.assertEqual(Workout.objects.count(), 3)
        self.assertEqual(saved_sets.count(), 60)

    def test_sets_deleted_with_workout(self):
        Workout.objects.get(name="Spring Workout - A - 2").delete()
        saved_sets = Set.objects.all()
        self.assertEqual(saved_sets.count(), 40)

    def test_change_workout_date(self):
        first_workout = Workout.objects.get(name="Spring Workout - A - 1")
        first_workout.date = first_workout.date - datetime.timedelta(1)
        first_workout.save()

        self.assertEqual(
            first_workout.date, datetime.date.today() - datetime.timedelta(1)
            )

        todays_sets = Set.objects.filter(workout__date=datetime.date.today())
        self.assertEqual(todays_sets.count(), 40)


class StrongliftsTest(TestCase):
    def setUp(self):
        create_user()

        first_routine = Routine()
        first_routine.name = "Spring Workout"
        first_routine.cycle_length = 7
        first_routine.cycle_position = 1
        first_routine.cycle_last_set = \
            datetime.date.today() - datetime.timedelta(1)
        first_routine.save()

        first_routineday = RoutineDay()
        first_routineday.name = "A"
        first_routineday.routine = Routine.objects.get(name="Spring Workout")
        first_routineday.position = 7
        first_routineday.save()

        exercise_names = ["Pushup", "Pullup", "Squat", "Plank"]
        exercises = [Exercise.objects.create(name=name)
                     for name in exercise_names]

        for exercise in exercises:
            RoutineDaySlot.objects.create(
                exercise=exercise,
                routineday=first_routineday,
                reps_min=5,
                reps_max=5,
                reps_step=0,
                sets_min=5,
                sets_max=5,
                weight_step=5
            )

        workout = Workout.objects.create_workout(
            routineday=first_routineday,
            owner=get_user()
        )

    def test_right_set_count(self):
        saved_sets = Set.objects.all()
        self.assertEqual(saved_sets.count(), 20)

    def test_sets_on_workout(self):
        workout = Workout.objects.all().first()
        self.assertEqual(workout.sets.count(), 20)

    def test_create_new_routine_with_sets(self):
        next_workout = Workout.objects.create_workout(
            routineday=RoutineDay.objects.get(name="A"),
            owner=get_user())
        saved_sets = Set.objects.all()
        self.assertEqual(saved_sets.count(), 40)
