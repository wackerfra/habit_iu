import click
import sqlite3

from tabulate import tabulate

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
@click.argument("period", type=click.IntRange(1, 4))
def same_periodicy(period):
    table_format = 'fancy_outline'
    first_row = ['id', 'name', 'description', 'period', 'duration']
    try:
        conn = connect_db()
        cur = conn.cursor()
        rs = cur.execute(""" SELECT DISTINCT habits_id,name,description,periods_fk,duration FROM habits 
        WHERE periods_fk = ?""", str(period))
    except ConnectionError as ex:
        print(ex)

    rows = list(rs.fetchall())
    print(tabulate(rows, headers=first_row, tablefmt=table_format))

analytic_group.add_command(show_all)
analytic_group.add_command(longest_streak_all)
analytic_group.add_command(longest_streak_habit)
analytic_group.add_command(same_periodicy)
