# DB-Comparison-Shortcut
This is a script to compare the results of two databases (production and dev) to test an enhancement feature

To run the script, place the queries for production or a staging region database in t2.txt and the queries for the developement region in the s432 regon. You can rename the files, but be sure to change the names inside the code as well.
This script currently will run on a Microsoft SQL Server database. You just have to place the correct connection credentials in the code.

Please install "pyodbc" package but running "pip install pyodbc" in your command prompt.

After you are all set, just run the script from either the command prompt (> python shortcut.py) or through the IDE itself. 


