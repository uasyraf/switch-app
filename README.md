# switch-app
An app for a coding challenge

# Instructions to run on local
1. Create virtual environment and activate it
2. Install [MariaDB 10.8.3](https://archive.mariadb.org//mariadb-10.8.3/winx64-packages/mariadb-10.8.3-winx64.msi) in path C:\Program Files\MariaDB directory --> **IMPORTANT**
4. Run "python -m pip install -r requirements.txt"
5. Create .env in **./mysite and project root**, and paste below into the file (Change secret key, database user/password with your own):

        SECRET_KEY=<your-secret-key>
        DB_NAME=codingchallengedb
        DB_USER=<your-db-user>
        DB_PASSWORD=<your-db-password>

6. Create database by the name "codingchallengedb" on your local MariaDB
7. Run "python ./data_loader_script.py"
8. Run "python manage.py makemigrations"
9. Run "python manage.py migrate"
10. Run "python manage.py runserver"
11. Enjoy.
