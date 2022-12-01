import sqlite3
from datetime import datetime

import click
from tabulate import tabulate

import src.habit as ha
from src.analytics import analytic_group


def connect_db():
    try:
        conn = sqlite3.connect('habit.db')
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
def new_habit(name, description, period):
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
    new = ha.Habit(name, description, period)
    new.save_to_db()
@click.command(name='new-from-template')
def new_template():
    """ create a new habit from a template """

    table_format = 'fancy_outline'
    first_row = ['id', 'name', 'description', 'period', 'duration in days']
    try:
        conn = connect_db()
        cur = conn.cursor()
        rs = cur.execute(
            """ SELECT h.habits_id,h.name,h.description,p.name,h.duration FROM habits as h 
            INNER JOIN periods as p ON h.periods_fk = p.periods_id  WHERE is_template == TRUE ORDER BY habits_id ASC """)
    except ConnectionError as ex:
        print(ex)


    rows = list(rs.fetchall())
    print(tabulate(rows, headers=first_row, tablefmt=table_format))

    userinput = int(input("Enter the ID of the habit you want to create.\n"))
    try:
        for row in rows:
            if row[0] == userinput:
                match row[3]:
                    case 'daily':
                        period = 1
                    case 'weekly':
                        period = 2
                    case 'monthly':
                        period = 3
                    case 'yearly':
                        period = 4
                new = ha.Habit(row[1], row[2], period)
                new.save_to_db()
                print("Habit created.")
                break
            else:
                continue
    except ValueError as ex:
        print('ID not found. \n' + ex)


@click.command(name='all-habits')
def show_all():
    """ show all habits in the database  """
    table_format = 'fancy_outline'
    first_row = ['id', 'name', 'description', 'period', 'duration in days']
    try:
        conn = connect_db()
        cur = conn.cursor()
        rs = cur.execute(
            """ SELECT DISTINCT h.habits_id,h.name,h.description,p.name,h.duration FROM habits as h 
            INNER JOIN periods as p ON h.periods_fk = p.periods_id  WHERE closed == FALSE AND is_template == FALSE 
            ORDER BY habits_id ASC """)
    except ConnectionError as ex:
        print(ex)

    rows = list(rs.fetchall())
    print(tabulate(rows, headers=first_row, tablefmt=table_format))
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
        # conn.row_factory = sqlite3.Row
        rs = cur.execute(
            """ SELECT * FROM habits WHERE  habits_id = ? ORDER BY last_completion_date DESC """, str(hid))
        rows = list(rs.fetchone())
    except sqlite3.Error as ex:
        conn.close()
        print(ex)

    try:
        if rows[7] is not None:
            if rows[7][0: 10] == datetime.now().strftime("%Y-%m-%d") :
                raise ValueError('The habit is already completed today')
        rows[7] = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        cur.executemany("""INSERT INTO habits  VALUES (?,?,?,?,?,?,?,?,?)""", [rows])
        conn.commit()
        print(f'You have completed the habit {rows[1]}')
        conn.close()
    except sqlite3.Error as ex:
        conn.close()
        print(ex)
    except ValueError as ex:
        conn.close()
        print(ex)

main_cli.add_command(show_all)
main_cli.add_command(new_habit)
main_cli.add_command(new_template)
main_cli.add_command(mark_done_today)
main_cli.add_command(analytic_group)

# if __name__ == '__main__':
#     main_cli()
