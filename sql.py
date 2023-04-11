import sqlite3
from sqlite3 import Error
# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg: str):
        try:
            self.conn = sqlite3.connect(database_arg)
            print("Connect to SQL DB success.")
        except Error as e:
            print(f"Exception: {e}")
            
        self.cur = self.conn.cursor()
        self.id_counter = 1

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string: str):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password: str):

        # # Clear the database if needed
        # self.execute("DROP TABLE IF EXISTS Users")
        # self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            Id INT,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0
        )""")

        self.commit()

        # Add our admin user
        self.add_user('admin', admin_password, admin=1)
        

    def database_wipe(self):
        
        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()


    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, admin):
        
        
        if self.check_user_exists(username=username):
            return False
        
        else:
            id = self.id_counter
            self.id_counter += 1
            
            sql_cmd = """
                    INSERT INTO Users
                    VALUES({id}, '{username}', '{password}', {admin})
                """

            sql_cmd = sql_cmd.format(id=id, username=username, password=password, admin=admin)

            self.execute(sql_cmd)
            self.commit()
            return True

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, password=password)
        self.execute(sql_query)
        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False

    #-----------------------------------------------------------------------------

    # Check user exists
    def check_user_exists(self, username):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}'
            """
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        if self.cur.fetchone():
            return True
        
        else:
            return False