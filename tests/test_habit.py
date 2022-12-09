import habit
import pytest

def test_connect_db():
    assert habit.connect_db() is not None


def test_get_instance():
    habit1 = habit.Habit.get_instance(2)
    assert habit1.name == 'Tea'
    assert habit1.description == 'drink more tea'


# def test_habit():
#     # Arrange
#     #Act
#     #Assert
#
#     # calculator = Calculator()
#     # result = calculator.add(2, 3)
#     # assert result == 5
#     assert True
