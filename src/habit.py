from datetime import datetime, timedelta
import sqlite3

from tabulate import tabulate


def connect_db():
        try:
            conn = sqlite3.connect('habit.db')
           # c = conn.cursor()

        except ConnectionError as ex:
            print(ex)

        return conn

class Habit:
    periods = {1:'daily', 2:'weekly', 3:'monthly', 4:'yearly'}


    def __init__(self, habit, description, period, duration=60,is_template=0):

        if habit is None or len(str(habit).strip()) == 0:
            raise ValueError('Habit can not be empty')
        self.habit = habit

        if description is None or len(str(description).strip()) == 0:
            raise ValueError('You must describe the habit')
        self.description = description

        if period not in Habit.periods:
            raise ValueError('Period must be daily, weekly, monthly or yearly')
        self.period = period

        self.duration = duration
        self.created = datetime.now()
        self.completed = False
        self.closed = False
        self.last_completion_date = None
        self.habits_id = None
        self.is_template = is_template

        # check if the Habit is still open
        status = self.check_duration()
        print(status)

    def mark_completed(self):
        # connect to DB and get current record
        try:
           conn = connect_db()
           cur = conn.cursor()
        except ConnectionError as ex:
            print(ex)
        if self.last_completion_date.strftime("%Y-%m-%d") == datetime.now().strftime(
                "%Y-%m-%d"):
            raise ValueError('The habit is already completed today')
        self.last_completion_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
       # update record
        try:
           cur.execute(""" UPDATE habits SET last_completion_date = ? WHERE name = ? """, (self.last_completion_date,self.habit))
           conn.commit()
           print('commit...')
           # close connection
           conn.close()
           print('connection closed...')
        except ConnectionError as ex:
            print(ex)


    def check_duration(self):
        diff = datetime.now() - self.created
        diff_days = int(diff / timedelta(days=1))
        if self.duration <= diff_days and self.closed == False:
            self.closed = True
            conn = connect_db()
            cur = conn.cursor()
            try:
               cur.execute(""" UPDATE habits SET closed = 1 WHERE habits_id = ? """, self.habits_id)
               conn.commit()
               # close connection
               conn.close()
            except ConnectionError as ex:
                print(ex)
        return f'You have {self.duration - diff_days} days left to complete the task'

    def delete_habit(self):
        try:
           conn = connect_db()
           cur = conn.cursor()

           cur.execute("""DELETE FROM habits  WHERE habits_id = ?""", self.habits_id)
           conn.commit()
               # close connection
           conn.close()
        except ConnectionError as ex:
            print(self.habit)
            print(ex)

    def save_to_db(self):
        try:
           conn = connect_db()
           cur = conn.cursor()
           print('connected...')
           habit_data = [
               (None,self.habit, self.description, self.period, self.duration, self.created, self.closed, self.last_completion_date, self.is_template)
           ]
           cur.executemany("""INSERT INTO habits  VALUES (?,?,?,?,?,?,?,?,?)""", habit_data)
        except ConnectionError as ex:
            print(ex)

        try:
            conn.commit()
            # close connection
            conn.close()
        except ConnectionError as ex:
            print(ex)


    def read_habit(self, hid):
        try:
           conn = connect_db()
           cur = conn.cursor()
           rs = cur.execute(""" SELECT * FROM habits WHERE habits_id = ? """, hid)
        except ConnectionError as ex:
            print(ex)
        return rs.fetchone()

def show_all_habits():
    table_format = 'fancy_outline'
    first_row = ['name','description','periode','duration','last_completion_date']
    try:
        conn = connect_db()
        cur = conn.cursor()
        rs = cur.execute(""" SELECT name,description,periods_fk,duration,last_completion_date FROM habits WHERE closed == FALSE""")
    except ConnectionError as ex:
            print(ex)

    rows = list(rs.fetchall())
    return tabulate(rows,headers= first_row,tablefmt=table_format)








