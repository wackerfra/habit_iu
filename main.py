import sqlite3
import click

import src.habit as ha
def connect_db():
    try:
        conn = sqlite3.connect('habit.db')
        c = conn.cursor()

    except ConnectionError as ex:
        print(ex)

# Press the green button in the gutter to run the script.


@click.group
def main_cli():
    pass

@click.command(name='new')
def new_habit(name,description,period):
    new = ha.Habit(name,description,period)
    new.save_to_db()


if __name__ == '__main__':
    main_cli()
