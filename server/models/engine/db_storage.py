#!/usr/bin/python3

"""
db_storage:
    This module holds the defination of the class DBStorage
    which handles the storage of objects in a database.
"""

import mysql
from mysql.connector import Error
from os import getenv


class_table_pair = {
        "Raffle": "raffles",
        "RaffleGames": "raffle_games"
    }


class DBStorage:
    """
    DBStorage: handles object storage persistency
    """
    
    __objects = {}

    def __init__(self, mysql_user, mysql_pwd, mysql_host, mysql_db):
        self.MYSQL_USER = mysql_user
        self.MYSQL_PWD = mysql_pwd
        self.MYSQL_HOST = mysql_host
        self.MYSQL_DB = mysql_db


    def create_connection(self):
        """
        create_connection: Creats a connection with the database and
            returnes the connection object
        
        Args:
            None
        
        Return:
            On successful connection connection is returned else
            None is returned.
        """
        try:
            conn = mysql.connector.connect(host=self.MYSQL_HOST,
                                           user=self.MYSQL_USER,
                                           password=self.MYSQL_PWD,
                                           database=self.MYSQL_DB)
            conn.query('SET GLOBAL connect_timeout=28800')
            conn.query('SET GLOBAL wait_timeout=28800')
            conn.query('SET GLOBAL interactive_timeout=28800')
            return conn
        except Error as e:
            print("Error connecting to the MySQL database:", e)
            return None
    
    @staticmethod
    def generate_insert_query(value, table):
        
        id = value.id
        created_at = value.created_at
        updated_at = value.updated_at
        unique_id = \
            getattr(value,
                    "unique_id",
                    "NULL") if getattr(value,
                                       "unique_id",
                                       "NULL") is not None else "NULL"
        winner_id = getattr(value,
                            "winner",
                            "NULL") if getattr(value,
                                               "winner",
                                               "NULL") is not None else "NULL"
        total_gifts = getattr(value,
                        "gifts",
                        "NULL") if getattr(value,
                                           "gifts",
                                           "NULL") is not None else "NULL"
        
        if table == "raffles":
            query = f"""
            INSERT INTO {table} (id, unique_id, created_at, updated_at)
            VALUES ({id}, {value.unique_id}, {created_at}, {updated_at});
            """
        elif table == "raffle_games":
            query
    def insert(self, conn, value, table):
        """
        insert: inserts `value` in to `table`.

        Args:
            value (:object:): An object from models package.
            table (:str:): The table to insert value into. 
        """
        cursor = conn.cursor()



        query = DBStorage.generate_insert_query("insert", value, table)

    def new(self, obj):
        """
        new(self, obj):
            Inserts new object to the collection of objects.

        Args:
            obj: The object to be stored.

        Return:
            None.
        """
        DBStorage.__objects[f'{type(obj).__name__}.{obj.id}'] = obj

    def save(self):
        """
        save(self):
            Saves the objects collection dictionary in the database

        Return:
            None.
        """
        conn = self.create_connection()
        if conn is None:
            print("Unable to connect to database")
            return
        cursor = conn.cursor(dictionary=True)

        values = DBStorage.__objects.values()
        for value in values:
            table = class_table_pair[type(value).__name__]

            query = f"""
            SELECT *
            FROM {table}
            WHERE id = {value.id}
            """
            
            cursor.execute(query)
            old_value = cursor.fetchone()
            cursor.close()

            if old_value is None:
                self.insert(conn, value, table)
            else:
                self.update(conn, value, old_value, table)

        conn.close()
