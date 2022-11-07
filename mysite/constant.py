import os, environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Database constants
USER = env('DB_USER')
PASSWORD = env('DB_PASSWORD')
HOST = "localhost"
DATABASE = env('DB_NAME')

# Model object and its corresponding column in the data list
LABLE = 0
TERMINAL_1 = 1
TERMINAL_2 = 2
TERMINAL_3 = 3
TERMINAL_4 = 4
TERMINAL_5 = 5
DATETIME = 6
