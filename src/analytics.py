from datetime import datetime

import click
import sqlite3

from tabulate import tabulate

from src.habit import connect_db, show_all_habits


def get_cursor():
    try:
        conn = connect_db()
        c = conn.cursor()
    except ConnectionError as ex:
        print(ex)
    return c
@click.group(name="analytics")
def analytic_group():
    """ Commands for your analysis"""



@click.command(name='all')
def show_all():
    show_all_habits()

@click.command(name='streak-all')
def longest_streak_all():
    pass

@click.command(name='streak')
@click.argument('habit_id', type= click.IntRange(1))
def longest_streak_habit(habit_id):
    dateformat = "%Y-%m-%d %H:%M:%S"
    streak = 1
    longest = 1
    try:
        cur = get_cursor()
        rs = cur.execute(""" SELECT habits_id, name,periods_fk, last_completion_date FROM habits WHERE habits_id = ? AND last_completion_date not null  """,str(habit_id))
        rows = rs.fetchall()
    except sqlite3.Error as ex:
        print(ex)
    data = rows[0]
    period = data[2]
    first_compl = data[3]
    habit_name = data[1]
    for row in rows:
        if streak > longest:
            longest = streak
        match period:
            case 1:
                first = datetime.strptime(first_compl,dateformat)
                current = datetime.strptime(row[3],dateformat)
                delta = current - first
                if delta.days <= 1:
                    streak += 1
                else:
                    streak = 0
                    continue
            case 2:
                first = datetime.strptime(first_compl,dateformat)
                current = datetime.strptime(row[3],dateformat)
                delta = current - first
                if delta.days <= 7:
                    streak += 1
                else:
                    streak = 0
                    continue
            case 3:
                first = datetime.strptime(first_compl,dateformat)
                current = datetime.strptime(row[3],dateformat)
                delta = current - first
                if delta.days <= 30:
                    streak += 1
                else:
                    streak = 0
                    continue
            case 4:
                first = datetime.strptime(first_compl,dateformat)
                current = datetime.strptime(row[3],dateformat)
                delta = current - first
                if delta.days <= 365:
                    streak += 1
                else:
                    streak = 0
                    continue

    print(f'The longest streak for your habit {habit_name} is {longest} times')

@click.command(name='periodicy')
@click.argument("period", type=click.IntRange(1, 4))
def same_periodicy(period):
    table_format = 'fancy_outline'
    first_row = ['id', 'name', 'description', 'period', 'duration']
    try:
        cur = get_cursor()
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
