import sqlite3
from datetime import datetime, timedelta


def connect_db():
    """Connect to the database"""
    try:
        conn = sqlite3.connect('habit.db')

    except ConnectionError as ex:
        conn = None
        print(ex)

    return conn


class Habit:
    periods = {1: 'daily', 2: 'weekly', 3: 'monthly', 4: 'yearly'}

    def __init__(self, habit, description, period, duration=60, is_template=0):
        """
        :param habit: name of the habit
        :type habit: str
        :param description: description of the habit
        :type description: str
        :param period: period of the habit
        :type period: int
        :param duration: duration of the habit
        :type duration: int
        :param is_template: is the habit a template
        :type is_template: bool

        """

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


    @staticmethod
    def get_instance(hid):
        """ get the habit instance from the database """
        period = None
        try:
            conn = connect_db()
            cur = conn.cursor()
            rs = cur.execute(f"SELECT * FROM habits WHERE habits_id = {hid} ORDER BY last_completion_date DESC")
            rows = list(rs.fetchone())
        except sqlite3.Error as ex:
            print(ex)
        except TypeError as ex:
            raise ValueError('Habit not found')

        # create a new habit instance
        try:
            habit = Habit(rows[1], rows[2], rows[3], rows[4], rows[8])
            habit.habits_id = rows[0]
            habit.created = rows[5]
            habit.closed = rows[6]
            habit.last_completion_date = rows[7]
            return habit
        except ValueError as ex:
            print(ex)

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

    def delete(self):
        """ delete the habit from the database """
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(f"DELETE FROM habits WHERE habits_id = {self.habits_id}")
            conf = input(f'Are you sure you want to delete the habit {self.habit}? (y/n)\n')
            if conf == 'y':
                conn.commit()
                print(f'Habit {self.habit} has been deleted.')
            else:
                conn.rollback()
                print('Action cancelled.')
        except ConnectionError as ex:
            print(ex)
            conn.close()

    def check_duration(self):
        """ check if the habit is still open """
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        a = datetime.today()
        b = datetime.strptime(self.created, date_format)
        diff = a - b

        if self.duration <= diff.days and self.closed == False:
            self.closed = True
            conn = connect_db()
            cur = conn.cursor()
            try:
                cur.execute(f""" UPDATE habits SET closed = 1 WHERE habits_id = {self.habits_id}""")
                conn.commit()
                # close connection
                conn.close()
                print(f'Habit {self.habit} has been closed.')
            except ConnectionError as ex:
                conn.close()
                print(ex)
        days_left = int(self.duration) - int(diff.days)
        print(f'You have {days_left} days left to complete the task')
        return diff.days  # return the number of days left

    def complete_today(self):
        """ mark the habit as completed """
        if self.last_completion_date is not None:
            if self.last_completion_date[0: 10] == datetime.now().strftime("%Y-%m-%d"):  # check if habit is already completed today
                raise ValueError('The habit is already completed today')

        self.check_duration()
        self.is_template = False
        self.last_completion_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        self.save_to_db()

    def save_to_db(self):
        """ save changes to database """
        try:
            conn = connect_db()
            cur = conn.cursor()
            habit_data = [
                (self.habits_id, self.habit, self.description, self.period, self.duration, self.created, self.closed,
                 self.last_completion_date, self.is_template)
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
        print(f'Habit {self.habit} has been saved to the database.')
