# switch-app
An app for a coding challenge

# Instructions to run on local
1. Create virtual environment and activate it
2. Install [MariaDB 10.8.3](https://archive.mariadb.org//mariadb-10.8.3/winx64-packages/mariadb-10.8.3-winx64.msi) in path C:\Program Files\MariaDB directory --> **IMPORTANT**
3. Install [MariaDB Connector/C](https://mariadb.com/download-confirmation?group-name=Data%20Access&release-notes-uri=https%3A%2F%2Fmariadb.com%2Fkb%2Fen%2Fmariadb-connector-c-332-release-notes%2F&documentation-uri=https%3A%2F%2Fmariadb.com%2Fkb%2Fen%2Fmariadb-connector-c%2F&download-uri=https%3A%2F%2Fdlm.mariadb.com%2F2453937%2FConnectors%2Fc%2Fconnector-c-3.3.2%2Fmariadb-connector-c-3.3.2-win64.msi&product-name=C%20connector&download-size=20.67%20MB)
4. Run "python -m pip install -r requirements.txt"
5. Create .env in **./mysite**, and paste below into the file (Change secret key, database user/password with your own):

        SECRET_KEY=<your-secret-key>
        DB_NAME=codingchallengedb
        DB_USER=<your-db-user>
        DB_PASSWORD=<your-db-password>

6. Create database by the name "codingchallengedb" on your local MariaDB
7. Run "python manage.py makemigrations"
8. Run "python manage.py migrate"
9. Modify these lines in **./mysite/data_loader_script.py --> main()** 

        user="<your-user>",
        password="<your-password>",
        host="localhost",
        database="your-database-name>",
        
9. Run "python ./mysite/data_loader_script.py"
10. Run "python manage.py runserver"
11. Enjoy.
