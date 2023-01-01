import click
import pytest
from click.testing import CliRunner

from src.analytics import *


# happy path
def test_show_all_habits():
    runner = CliRunner()
    result = runner.invoke(show_all_habits)
    assert result.exit_code == 0
    assert result.output.__len__() > 0


def test_show_all_activities():
    runner = CliRunner()
    result = runner.invoke(show_all_activities)
    print(result)
    assert result.exit_code == 0
    assert result.output.__len__() > 10


def test_longest_streak_all():
    runner = CliRunner()
    result = runner.invoke(longest_streak_all)
    assert result.exit_code == 0
    assert result.output == 'The longest streak is for your habit sleep with 37 times\n'


def test_longest_streak():
    runner = CliRunner()
    result = runner.invoke(longest_streak_habit, ['3'])
    assert result.exit_code == 0
    assert result.output == 'The longest streak for your habit Coffee is 8 times\n'


def test_same_periodicy_day():
    runner = CliRunner()
    result = runner.invoke(same_periodicy, ['1'])
    assert result.exit_code == 0
    assert result.output.find('Coffee') > 0


# sad path

def test_longest_streak_fail():
    runner = CliRunner()
    result = runner.invoke(longest_streak_habit, ['99'])
    assert 'No habit with this id\n' in result.output

#
def test_same_periodicy_fail():
    runner = CliRunner()
    result = runner.invoke(same_periodicy, ['5'])
    assert result.exit_code != 0
    # assert SystemExit == click.exceptions.BadParameter




