from datetime import datetime

import pytest

import src.habit as habit


# happy path
def test_connect_db():
    assert habit.connect_db() is not None


def test_get_instance():
    habit1 = habit.Habit.get_instance(4)
    assert habit1.habit == 'Exercise'
    assert habit1.description == 'Exercise weekly'
    assert habit1.period == 2
    assert habit1.duration == 90
    assert habit1.closed == False

def test_get_habits_id():
    habit1 = habit.Habit('Test', 'test my script', 1, 30)
    assert habit1.get_habits_id() == 11

def test_check_duration():
    habit1 = habit.Habit.get_instance(4)
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    a = datetime.today()
    b = datetime.strptime(habit1.created, date_format)
    diff = a - b

    assert habit1.check_duration() == diff.days

def test_completed_today():
    habit1 = habit.Habit.get_instance(2)
    if habit1.last_completion_date is not None:
        if habit1.last_completion_date[0: 10] == datetime.now().strftime("%Y-%m-%d"):
            with pytest.raises(ValueError):
                habit1.complete_today()
            return True
    habit1.complete_today()
    habit1_1 = habit.Habit.get_instance(2)
    assert habit1_1.last_completion_date.strftime("%Y-%m-%d") == habit1.last_completion_date.strftime("%Y-%m-%d")



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

