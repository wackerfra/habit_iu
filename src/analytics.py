import sqlite3
from datetime import datetime

import click
from tabulate import tabulate

from src.habit import connect_db


def get_cursor():
    """
    Get a cursor to the database
    :return: cursor
    """
    try:
        conn = connect_db()
        c = conn.cursor()
    except ConnectionError as ex:
        print(ex)
    return c


@click.group(name="analytics")
def analytic_group():
    """ Commands for your analysis"""


@click.command(name='all-habits')
def show_all_habits():
    """list all habits"""

    # define output format
    table_format = 'fancy_outline'
    first_row = ['id', 'name', 'description', 'period', 'duration in days']
    try:
        cur = get_cursor()
        rs = cur.execute(
            """ SELECT DISTINCT h.habits_id,h.name,h.description,p.name,h.duration FROM habits as h 
            INNER JOIN periods as p ON h.periods_fk = p.periods_id  WHERE closed == FALSE ORDER BY habits_id ASC """)
    except ConnectionError as ex:
        print(ex)

    rows = list(rs.fetchall())
    cur.close()
    click.echo(tabulate(rows, headers=first_row, tablefmt=table_format))


@click.command(name='list-all-activities')
def show_all_activities():
    """list all activities for all habit"""

    # define output format
    table_format = 'fancy_outline'
    first_row = ['id', 'name', 'description', 'period', 'duration in days', 'last completion date']
    try:
        cur = get_cursor()
        rs = cur.execute(
            """ SELECT  h.habits_id,h.name,h.description,p.name,h.duration, h.last_completion_date FROM habits as h 
            INNER JOIN periods as p ON h.periods_fk = p.periods_id  WHERE closed == FALSE 
            ORDER BY habits_id ASC, last_completion_date DESC """)

    except ConnectionError as ex:
        print(ex)

    rows = list(rs.fetchall())
    cur.close()
    click.echo(tabulate(rows, headers=first_row, tablefmt=table_format))


@click.command(name='streak-all')
def longest_streak_all():
    """show longest streak of all habits"""

    # define output format
    dateformat = "%Y-%m-%d %H:%M:%S"
    streak = 0
    longest = 0
    h_name = None
    max_habit = None
    try:
        cur = get_cursor()
        rs = cur.execute(
            """ SELECT habits_id, name,periods_fk, last_completion_date FROM habits WHERE last_completion_date not null 
            ORDER BY habits_id ASC, last_completion_date ASC """)
        rows = rs.fetchall()
    except sqlite3.Error as ex:
        print(ex)
        cur.close()
    except TypeError as ex:
        raise ValueError('No habit found')

    for row in rows:
        # helping variables
        habit_name = row[1]
        period = row[2]
        if habit_name != h_name:  # if new habit
            streak = 0
            first_compl = row[3]

        if streak >= longest:  # if new longest streak
            longest = streak
            max_habit = h_name
        match period:
            case 1:  # daily
                first = datetime.strptime(first_compl, dateformat)
                current = datetime.strptime(row[3], dateformat)
                delta = current - first
                first_compl = row[3]
                h_name = habit_name
                if delta.days <= 1:
                    streak += 1
                    if streak >= longest:
                        longest = streak
                else:
                    streak = 0
                    continue
            case 2:  # weekly
                first = datetime.strptime(first_compl, dateformat)
                current = datetime.strptime(row[3], dateformat)
                delta = current - first
                first_compl = row[3]
                h_name = habit_name
                if delta.days <= 7:
                    streak += 1
                    if streak >= longest:
                        longest = streak
                else:
                    streak = 0
                    continue
            case 3:  # monthly
                first = datetime.strptime(first_compl, dateformat)
                current = datetime.strptime(row[3], dateformat)
                delta = current - first
                first_compl = row[3]
                h_name = habit_name
                if delta.days <= 30:
                    streak += 1
                    if streak >= longest:
                        longest = streak
                else:
                    streak = 0
                    continue
            case 4:  # yearly
                first = datetime.strptime(first_compl, dateformat)
                current = datetime.strptime(row[3], dateformat)
                delta = current - first
                first_compl = row[3]
                h_name = habit_name
                if delta.days <= 365:
                    streak += 1
                    if streak >= longest:
                        longest = streak
                else:
                    streak = 0
                    continue

    # Output
    cur.close()
    click.echo(f'The longest streak is for your habit {max_habit} with {longest} times')



@click.command(name='streak')
@click.argument('habit_id', type=click.IntRange(1, 100))
def longest_streak_habit(habit_id):
    """display the longest streak of a habit"""

    # define output format
    dateformat = "%Y-%m-%d %H:%M:%S"
    streak = 0
    longest = 0
    try:
        # database connection
        cur = get_cursor()
        rs = cur.execute(
            f""" SELECT habits_id, name,periods_fk, last_completion_date FROM habits WHERE habits_id = {habit_id}
                    AND last_completion_date not null ORDER BY last_completion_date ASC """)
    except sqlite3.Error as ex:
        print(ex)
        cur.close()
        return None
    try:
        rows = rs.fetchall()
    except Exception as ex:
        print(ex)
        cur.close()
        return None
    try:
        data = rows[0]  # get first row
    except IndexError as ex:
        print(ex)
        print('No habit with this id')
        cur.close()
        return
    period = data[2]
    first_compl = data[3]
    habit_name = data[1]

    for row in rows:  # loop through all rows
        match period:  # check period
            case 1:  # daily
                first = datetime.strptime(first_compl, dateformat)
                current = datetime.strptime(row[3], dateformat)
                delta = current - first
                first_compl = row[3]
                if delta.days <= 1:
                    streak += 1
                    if streak >= longest:
                        longest = streak
                else:
                    streak = 0
                    continue
            case 2:  # weekly
                first = datetime.strptime(first_compl, dateformat)
                current = datetime.strptime(row[3], dateformat)
                delta = current - first
                first_compl = row[3]
                if delta.days <= 7:
                    streak += 1
                    if streak >= longest:
                        longest = streak
                else:
                    streak = 0
                    continue
            case 3:  # monthly
                first = datetime.strptime(first_compl, dateformat)
                current = datetime.strptime(row[3], dateformat)
                delta = current - first
                first_compl = row[3]
                if delta.days <= 30:
                    streak += 1
                    if streak >= longest:
                        longest = streak
                else:
                    streak = 0
                    continue
            case 4:  # yearly
                first = datetime.strptime(first_compl, dateformat)
                current = datetime.strptime(row[3], dateformat)
                delta = current - first
                first_compl = row[3]
                if delta.days <= 365:
                    streak += 1
                    if streak >= longest:
                        longest = streak
                else:
                    streak = 0
                    continue
    # Output
    cur.close()
    print(f'The longest streak for your habit {habit_name} is {longest} times')



@click.command(name='periodicy')
@click.argument("period", type=click.IntRange(1, 4))
def same_periodicy(period):
    """list all habits with the same periodicy

    1 = daily
    2 = weekly
    3 = monthly
    4 = yearly
    """

    # define output format
    table_format = 'fancy_outline'
    first_row = ['id', 'name', 'description', 'period', 'duration']
    try:
        cur = get_cursor()
        rs = cur.execute(""" SELECT DISTINCT h.habits_id,h.name,h.description,h.periods_fk,p.name, h.duration FROM habits as h 
            INNER JOIN periods as p ON h.periods_fk = p.periods_id WHERE h.periods_fk = ?""", str(period))
    except ConnectionError as ex:
        print(ex)

    rows = list(rs.fetchall())
    result = []
    for row in rows:
        result.append([row[0], row[1], row[2], row[4], row[5]])

    cur.close()
    click.echo(tabulate(result, headers=first_row, tablefmt=table_format))


# define the group for click commands

analytic_group.add_command(show_all_habits)
analytic_group.add_command(show_all_activities)
analytic_group.add_command(longest_streak_all)
analytic_group.add_command(longest_streak_habit)
analytic_group.add_command(same_periodicy)
