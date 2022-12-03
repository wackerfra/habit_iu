from datetime import datetime, timedelta
import sqlite3


def connect_db():
        try:
            conn = sqlite3.connect('habit.db')

        except ConnectionError as ex:
            conn = None
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
        self.is_template = is_template
        self.habits_id = None
        self.habits_id = self.get_habits_id()

        # check if the Habit is still open
        status = self.check_duration()
        print(status)
    def get_habits_id(self):
        """ get the habits_id from the database """

        if self.habits_id is None:
            # connect to DB and get current record
            try:
               conn = connect_db()
               cur = conn.cursor()
            except ConnectionError as ex:
                conn.close()
                print(ex)
            rs = cur.execute("""SELECT MAX(habits_id) FROM habits """)
            nxt = rs.fetchone()[0]
            nxt += 1
            conn.close()
            return nxt
        return self.habits_id


    def check_duration(self):
        """ check if the habit is still open """

        diff = datetime.now() - self.created
        diff_days = int(diff / timedelta(days=1))
        if self.duration <= diff_days and self.closed == False:
            self.closed = True
            conn = connect_db()
            cur = conn.cursor()
            try:
               cur.execute(""" UPDATE habits SET closed = 1 WHERE habits_id = ?""", self.habits_id)
               conn.commit()
               # close connection
               conn.close()
            except ConnectionError as ex:
                conn.close()
                print(ex)
        return f'You have {self.duration - diff_days} days left to complete the task'


    def save_to_db(self):
        """ save changes to database """
        try:
           conn = connect_db()
           cur = conn.cursor()
           habit_data = [
               (self.habits_id,self.habit, self.description, self.period, self.duration, self.created, self.closed, self.last_completion_date, self.is_template)
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


