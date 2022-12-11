import src.habit as habit
import pytest

# happy path
def test_connect_db():
    assert habit.connect_db() is not None


def test_get_instance():
    habit1 = habit.Habit.get_instance(2)
    assert habit1.habit == 'Tea'
    assert habit1.description == 'drink more Tea'
    assert habit1.period == 1
    assert habit1.duration == 30
    # assert habit1.last_completion_date == '2022-12-10 14:14:00'
    assert habit1.closed == False

def test_get_habits_id():
    habit1 = habit.Habit('Test', 'test my script', 1, 30)
    assert habit1.get_habits_id() == 11

def test_check_duration():
    habit1 = habit.Habit.get_instance(2)
    assert habit1.check_duration() == 21

# def test_completed_today():
#     habit1 = habit.Habit.get_instance(2)
#     habit1.complete_today()
#     assert habit1.completed == True

# sad path
def test_get_instance_fail():
    with pytest.raises(ValueError):
        habit.Habit.get_instance(100)

def test_get_habits_id_fail():
    habit1 = habit.Habit.get_instance(2)
    habit1.habits_id = 2
    assert habit1.get_habits_id() == 2

def test_new_habit_fail_name():
    with pytest.raises(ValueError):
        habit1 = habit.Habit('Hello','','',30)

def test_new_habit_fail_description():
    with pytest.raises(ValueError):
        habit1 = habit.Habit('','Hello','',30)

def test_completed_today_fail():
    habit1 = habit.Habit.get_instance(2)
    with pytest.raises(ValueError):
        habit1.complete_today()