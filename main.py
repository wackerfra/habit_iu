import sqlite3

import click
from tabulate import tabulate

import src.habit as ha
from src.analytics import analytic_group


def connect_db():
    """
    Connect to the database
    :return: connection
    """
    try:
        conn = sqlite3.connect('habit.db')
    except ConnectionError as ex:
        print(ex)

    return conn


# Manage the click group and subcommands
@click.group(name="habit")
def main_cli():
    """ defines the subcommand of click """
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
@click.option(
    "--duration",
    "-dur",
    default=60,
    help="How long should the habit be tracked in days"
)
@click.option(
    "--is_template",
    "-t",
    default=0,
    help="Is this habit used as template? 1=yes, 0=no"
)
def new_habit(name, description, period, duration, is_template=0):
    """     Create a new custom habit

    :param name:
    :type string:
    :param description:
    :type string:
    :param period:
    :type int:
    :param duration:
    :type int:
    :param is_template:
    :type boolean:
    :return: new habit
    :rtype: Habit
    """
    try:
        new = ha.Habit(name, description, period, duration, is_template)
    except ValueError as ex:
        print(ex)
        print("Please use the --help option to see the correct usage")
        return

    try:
        new.save_to_db()
    except sqlite3.IntegrityError as ex:
        print(ex)
        return


@click.command(name='new-from-template')
def new_template():
    """ create a new habit from a template """

    table_format = 'fancy_outline'
    first_row = ['id', 'name', 'description', 'period', 'duration in days']
    created = False
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
                new = ha.Habit(row[1], row[2], period, is_template=0)
                new.save_to_db()
                print("Habit created.")
                created = True
                break
            else:
                continue

    except ValueError as ex:
        print('ID not found. \n' + ex)
    if created == False:
        print(f"Habit ID {userinput} not found. \nPlease try again.")


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
        conn.close()
        print(ex)

    rows = list(rs.fetchall())
    print(tabulate(rows, headers=first_row, tablefmt=table_format))
    conn.close()


@click.command(name='mark-completed')
@click.argument("hid", type=click.IntRange(1))
def mark_done_today(hid):
    """ mark the task as done for today

    :param hid:
    :type hid
    :return: None
    """
    if hid is None or hid <= 0:
        raise ValueError('Please enter a valid habit ID')

    try:
        hab = ha.Habit.get_instance(hid)
        hab.complete_today()
    except Exception as ex:
        print(ex)
        print('- Please use "habit all-habits" and try again.')


@click.command(name='delete')
@click.argument("hid", type=click.IntRange(1))
def delete_habit(hid):
    """
     Delete a habit from Database

    :param hid:
    :type int:
      """
    if hid is None or hid <= 0:
        raise ValueError('Please enter a valid habit ID')

    try:
        hab = ha.Habit.get_instance(hid)
        hab.delete()
    except ValueError as ex:
        print(ex)


# add commands to the click-group
main_cli.add_command(show_all)
main_cli.add_command(new_habit)
main_cli.add_command(new_template)
main_cli.add_command(mark_done_today)
main_cli.add_command(analytic_group)
main_cli.add_command(delete_habit)


if __name__ == '__main__':
    main_cli()