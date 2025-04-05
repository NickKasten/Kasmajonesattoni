# Kasmajonesattoni
LMU 2025 Datathon


## Working with MySQL

1. Download MySQL and pip install the sqlachemy package
2. Create your own config file in this format:

MYSQL_USER = 'user_name'
MYSQL_PASSWORD = 'user_password'
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_DATABASE = 'database_name'

3. Create a new user in MySQL with this command:
  - CREATE USER 'user_name'@'localhost' IDENTIFIED BY 'user_';

4. grant privileges to the user to be able to interact with the database with this command:
  - GRANT ALL PRIVILEGES ON my_database.* TO 'new_user'@'localhost';

5. Common MySQL commands:
  - USE database_name; - selects the database to interact with it
  - SHOW tables; - shows all of the tables within the database
  - SELECT * FROM table; Shows all of the information in the table. In place of *, you ca specify specific columns and you can add LIMIT x where x is the number of results you want to display.
