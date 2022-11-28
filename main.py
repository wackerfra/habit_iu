import sqlite3
from datetime import datetime

import click

import src.habit as ha
from src.analytics import analytic_group
def connect_db():
    try:
        conn = sqlite3.connect('habit.db')
        c = conn.cursor()

    except ConnectionError as ex:
        print(ex)

    return conn


@click.group
def main_cli():
    pass


@click.command(name='new')
@click.option(
    "--name",
    "-n",
    default=None,
    help="Please specify a short name to identify the habit"
)
@click.option(
    "--description",
    "-d",
    default=None,
    help="Describe the habit in more detail"
)
@click.option(
    "--period",
    "-p",
    type=click.IntRange(1, 4),
    default=1,
    help="1=daily, 2=weekly, 3=monthly, 4=yearly"
)
def new_habit(name,description,period):
    """ create a new custom habit.

    :param name:
    :type name:
    :param description:
    :type description:
    :param period:
    :type period:
    :return:
    :rtype:
    """
    new = ha.Habit(name,description,period)
    new.save_to_db()
@click.command()
def show_all():
    """ list all active habits"""
    ha.show_all_habits()

@click.command(name='mark-completed')
@click.argument("hid", type=click.IntRange(1))
def mark_done_today(hid):
    """ mark the task as done for today

    :param hid:
    :type hid
    :return:
    :rtype:
    """
    try:
        conn = connect_db()
        cur = conn.cursor()
        rs = cur.execute(
            """ SELECT * FROM habits WHERE  habits_id = ?  """,
            str(hid))
        rows = list(rs.fetchone())
    except sqlite3.Error as ex:
        print(ex)

    try:
        print(rows, rows[7])
        rows[7] = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        cur.executemany("""INSERT INTO habits  VALUES (?,?,?,?,?,?,?,?,?)""", [rows])
        conn.commit()
    except sqlite3.Error as ex:
        conn.close()
        print(ex)


main_cli.add_command(new_habit)
main_cli.add_command(show_all)
main_cli.add_command(mark_done_today)
main_cli.add_command(analytic_group)

# if __name__ == '__main__':
#     main_cli()
