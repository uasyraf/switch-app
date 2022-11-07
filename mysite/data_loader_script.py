import mariadb
import csv
import constant
import os, environ

from datetime import datetime

class DataModel:
    def __init__(self):
        self._lable = None
        self._t1 = None
        self._t2 = None
        self._t3 = None
        self._t4 = None
        self._t5 = None
        self._datetime = None

    ### lable ###
    @property
    def lable(self):
        return self._lable

    @lable.setter
    def lable(self, a):
        self._lable = a
 
    ### t1 ###
    @property
    def t1(self):
        return self._t1

    @t1.setter
    def t1(self, a):
        self._t1 = a
 
    ### t2 ###
    @property
    def t2(self):
        return self._t2

    @t2.setter
    def t2(self, a):
        self._t2 = a
 
    ### t3 ###
    @property
    def t3(self):
        return self._t3

    @t3.setter
    def t3(self, a):
        self._t3 = a
 
    ### t4 ###
    @property
    def t4(self):
        return self._t4

    @t4.setter
    def t4(self, a):
        self._t4 = a
 
    ### t5 ###
    @property
    def t5(self):
        return self._t5

    @t5.setter
    def t5(self, a):
        self._t5 = a
 
    ### datetime ###
    @property
    def datetime(self):
        return self._datetime

    @datetime.setter
    def datetime(self, a):
        dt_object = datetime.fromtimestamp(int(a), None)
        self._datetime = dt_object


def CSV_ToListOfModels(path_to_csv):
    reader = None
    _model = DataModel()
    ls = []

    try:
        with open(path_to_csv, 'r') as file:
            reader = csv.reader(file)

            next(reader)
            for row in reader:
                _model.lable = row[constant.LABLE]
                _model.t1 = row[constant.TERMINAL_1]
                _model.t2 = row[constant.TERMINAL_2]
                _model.t3 = row[constant.TERMINAL_3]
                _model.t4 = row[constant.TERMINAL_4]
                _model.t5 = row[constant.TERMINAL_5]
                _model.datetime = row[constant.DATETIME]
                
                ls.append([_model.lable,
                        _model.t1,
                        _model.t2,
                        _model.t3,
                        _model.t4,
                        _model.t5,
                        _model.datetime
                    ]
                )
        
    except Exception as e:
        print(e)
    
    return ls



def main():  
    # Initialise environment variables
    env = environ.Env()
    environ.Env.read_env()

    try:
        connection = mariadb.connect(
            user="<your-user>",
            password="<your-password>",
            host="localhost",
            database="your-database-name>",
        )

        cursor = connection.cursor()

    except Exception as e:
        raise e

    # Insert switches data for first time only
    cursor.execute("SELECT * FROM signalrecord_switch")
    if cursor.rowcount == 0:
        for i in range(1, 4):
            cursor.execute(
                "INSERT INTO signalrecord_switch(name) VALUES(?)",
                (f"S{i}",),
            )
        connection.commit()

    path_to_csv = ".\mysite\Data_Terminals.csv"
    data_models_ls = CSV_ToListOfModels(path_to_csv)
    
    # Insert db_status data for first time only
    cursor.execute("SELECT * FROM signalrecord_databasestatus")
    if cursor.rowcount == 0:
        print("db_status is empty.")
        sql_update_dbstatus = "INSERT INTO signalrecord_databasestatus(raw, parsed) VALUES(?, ?)"
        tup_dbstatus = (0, 0)
        cursor.execute(
            sql_update_dbstatus,
            tup_dbstatus,
        )
        connection.commit()

    # Get population status
    cursor.execute("SELECT raw FROM signalrecord_databasestatus WHERE id = 1")
    populated = cursor.fetchone()[0]

    # Load csv to db only if it hasn't been populated previously
    if not populated:
        print("Populating database based on the data list.")

        try:
            sql_load_data = "INSERT INTO signalrecord_pingstatusraw(terminal_1, terminal_2, terminal_3, terminal_4, terminal_5, date_n_time, switch_id) VALUES(?, ?, ?, ?, ?, ?, (SELECT id FROM signalrecord_switch WHERE name = ?))"

            for i, k in enumerate(data_models_ls):
                tup_data = (
                    k[constant.TERMINAL_1],
                    k[constant.TERMINAL_2],
                    k[constant.TERMINAL_3],
                    k[constant.TERMINAL_4],
                    k[constant.TERMINAL_5],
                    k[constant.DATETIME],
                    k[constant.LABLE],
                )
                
                cursor.execute(
                    sql_load_data,
                    tup_data,
                )
            
            sql_update_dbstatus = "UPDATE signalrecord_databasestatus SET raw = 1 WHERE id = 1"
            tup_dbstatus = (1,)
            cursor.execute(
                sql_update_dbstatus,
                tup_dbstatus,
            )

            connection.commit()
        except Exception as e:
            raise e
        # except mariadb.Error as e:
        #     print(f"MariaDB Error: {e}")

    else:
        print("Database has been populated previously. Skipped.")

    # Insert initial data for App to work on first launch
    cursor.execute("SELECT * FROM signalrecord_pingstatusclean")
    if cursor.rowcount == 0:
        ls = [1, 1, 0]
        for i in range(1, 4):
            cursor.execute(
                "INSERT INTO signalrecord_pingstatusclean(state, date_n_time, switch_id) VALUES(?, ?, (SELECT id FROM signalrecord_switch WHERE name = ?))",
                (ls[i-1], '2019-11-28 08:00:00', f'S{i}'),
            )
        connection.commit()

    cursor.execute("SELECT * FROM signalrecord_alertreport")
    if cursor.rowcount == 0:
        cursor.execute(
            "INSERT INTO signalrecord_alertreport(alert_type, alert_datetime, alert_notification_datetime, switch_id) VALUES(?, ?, ?, (SELECT id FROM signalrecord_switch WHERE name = ?))",
            ('Ping lost', '2019-11-28 08:00:00', '2019-11-28 08:05:00', 'S3'),
        )
        connection.commit()



if __name__ == '__main__':
    main()