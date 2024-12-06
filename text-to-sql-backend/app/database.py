import sqlite3
from sqlite3 import Error
import pandas as pd

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def execute_query(self, query):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Execute the query
            cursor.execute(query)
            
            # For SELECT queries, return results
            if query.strip().upper().startswith('SELECT'):
                columns = [description[0] for description in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                conn.commit()
                results = [{"message": "Query executed successfully"}]
            
            return results
            
        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()
        conn = self.get_connection()
        if not conn:
            raise Exception("Could not connect to database")
        
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                columns = [description[0] for description in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                conn.commit()
                results = [{"message": "Query executed successfully"}]
            
            return results
            
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
        finally:
            conn.close()

    def get_table_schema(self, table_name):
        conn = self.get_connection()
        if not conn:
            raise Exception("Could not connect to database")
        
        try:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            schema = []
            for col in columns:
                schema.append({
                    "name": col[1],
                    "type": col[2],
                    "notnull": col[3],
                    "pk": col[5]
                })
            
            return schema
        except Error as e:
            raise Exception(f"Error getting schema: {str(e)}")
        finally:
            conn.close()

    def get_all_tables(self):
        conn = self.get_connection()
        if not conn:
            raise Exception("Could not connect to database")
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            return [table[0] for table in tables]
        except Error as e:
            raise Exception(f"Error getting tables: {str(e)}")
        finally:
            conn.close()