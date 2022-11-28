import click
import sqlite3

from src.habit import connect_db, show_all_habits

@click.group(name="analytics")
def analytic_group():
    """ Commands for your analysis"""

@click.command(name='all')
def show_all():
    pass

@click.command(name='streak-all')
def longest_streak_all():
    pass

@click.command(name='streak')
def longest_streak_habit(habit_id):
    pass

@click.command(name='periodicy')
def same_periodicy():
    pass

analytic_group.add_command(show_all)
analytic_group.add_command(longest_streak_all)
analytic_group.add_command(longest_streak_habit)
analytic_group.add_command(same_periodicy)
