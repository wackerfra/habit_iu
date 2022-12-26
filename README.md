<h1>Habit Tracker IU</h1> 
Welcome to my Habit tracker for the IU International University of applied science for Data Science. 

<h2>1 Instalation</h2>

The programm requires Python 3.10 or above to run properly. </br>
To install the latest Python version go to https://www.python.org/downloads/source/ and install the version for your system

Open a Terminal session at the folder you downloaded the habit app. </br>
Check that the right Python version is running by typing <code>python --version</code></br>
The response should be Python 3.10.X or above

Additionally, pip is required to install additional packages. </br>
To install pip follow the instructions on https://pip.pypa.io/en/stable/installation/

Run: <code>pip install .</code> (Don't ignore the whitespace and dot)  </br>
To complete the installation run 
<code>pip install -r requirements.txt</code> </br>
This will install all additional packages required for the app. </br>

<h2>2 Start the app</h2> </br>
Open a Terminal session on the directory the app is stored. 
If you are on a Windows machine make sure to use "cmd" and not a powershell. </br>
Activate the virtual environment by typing <code>venv\Scripts\activate.bat</code> </br>
Start the app by typing </br>
<code>habit</code>

<h3>2.1 Create a new habit</h3> </br>
You can create a new individual habit by typing <code>habit new</code> with the following parameters</br>
--name or -n for the short name of the habit</br>
--description or -d for a description of the habit</br>
--period or -p for the period how often you repeat the habit as integer 1=daily, 2=weekly, 3=monthly, 4=yearly</br>
for example <code>habit new -n "dentist" -d "have my teeth checked" -p 4</code> use double quotes for the string parameters

or copy a habit from a example habit using</br>
<code>habit new-from-template</code> </br>

<h3>2.2 complete a habit today</h3> </br>
List all habits to check the ID of your habits. <code>habit all-habits</code> </br>
To complete a habit type <code>habit mark-completed id</code>  change id with the id of the habit you completed today

<h3>2.3 Show all habits</h3> </br>
To show all habits type <code>habit all-habits</code> </br>

<h3>2.4 Delete a habit</h3> </br>
To delete a habit type <code>habit delete id</code> </br>
change id with the id of the habit you want to delete </br>

<h2>3 Analytics</h2> </br>
In the analytics module you can anlyse your activities. </br>
To get an overview of the possible commands type <code>habit analytics</code> </br>
 - all-habits - list of all active habits </br>
 - list-all-activities - list of all entries of completed tasks </br>
 - periodiciy followed by the periodicy number 1-4 lists all habits with the same periodicy </br>
 - streak followed by the habit id lists the longest streak for this habit </br>
 - streak-all list the longest streak of all habits </br>

Have fun and keep up the good progress




