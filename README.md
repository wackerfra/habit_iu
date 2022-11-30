# habit_iu
Welcome to my Habit tracker for the Iu International University of applied science for Data Science. 

1. Instalation
The programm requires Python 3.10 or above to run properly. 
To install the latest Python version go to https://www.python.org/downloads/source/ and install the version for your system

Open a Terminal session at the folder you downloaded the habit app. 
Check that the right Python version is running by typing "python --version". 
The response should be Python 3.10.X or above

Additionally pip is required to install additional packages. 
To install pip follow the instructions on https://pip.pypa.io/en/stable/installation/

Run: <<< pip install . >>> (Don't ignore the whitespace dot)  
To complete the installation run <<< pip install -r requirements.txt >>>
This will install all additional packages required for the app. 

2. Start the app
Open a Terminal session on the directory the app is stored. 
If you are on a Windows mashine make sure to use "cmd" and not a powershell. 
Start the app by typing <<< habit >>>

2.1 Create a new habit
You can create a new individual habit by typing <<< habit new >>> with the following parameters
--name or -n for the short name of the habit
--description or -d for a description of the habit
--period or -p for the period how often you repeat the habit as integer 1=daily, 2=weekly, 3=monthly, 4=yearly
for example <<< habit new -n "dentist" -d "have my teeth checked" -p 4 >>> use double quptes for the string parameters

or copy a habit from a example habit using
TODO

2.2 complete a habit today
List all habits to check the ID of your habits. <<< habit show-all >>>
To complete a habit type <<< habit mark-completed id >>> change id with the id of the habit you completed today

3. Analytics
In the analytics module you can anlyse your activities. 
To get an overview of the possible commands type <<< habit analytics >>>
all - list of all active habits
periodiciy followed by the periodicy number 1-4 lists all habits with the same periodicy
streak followed by the habit id lists the longest streak for this habit
streak-all list the longest streak of all habits

Have fun and keep up the good progress




