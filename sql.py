import sqlite3
from sqlite3 import Error
# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL users Database

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
        self.execute("""CREATE TABLE IF NOT EXISTS Users(
            Id INT,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0,
            status INTEGER DEFAULT 0,
            public_key INTEGER DEFAULT 'None'
        )""")

        self.commit()

        # Add our admin user if not exist
        if self.check_user_exists('admin') != True:
            self.add_user('admin', admin_password, admin=1)
        
        self.logout_all()
        

    #-----------------------------------------------------------------------------
    
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
                    VALUES({id}, '{username}', '{password}', {admin}, {status}, {public_key})
                """

            sql_cmd = sql_cmd.format(id=id, username=username, 
                                     password=password, admin=admin, status=0, public_key=0)
        
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
        
    #-----------------------------------------------------------------------------

    # Check user online status
    def check_user_online(self, username):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}' AND status = 1
            """
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        if self.cur.fetchone():
            return True
        
        else:
            return False
        
    #-----------------------------------------------------------------------------
    
    # change user status to online
    def login_user(self, username, public_key):
        sql_query = """
                UPDATE Users
                SET status = 1,
                    public_key = '{public_key}'
                WHERE username = '{username}'
            """
        sql_query = sql_query.format(username=username, public_key=public_key)
        self.execute(sql_query)
        self.commit()
        return True

    #-----------------------------------------------------------------------------
    
    # change user status to offline
    def logout_user(self, username):
        sql_query = """
                UPDATE Users
                SET status = 0
                WHERE username = '{username}'
            """
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        self.commit()
        return True

    def logout_all(self):
        sql_query = """
                UPDATE Users
                SET status = 0, public_key = 'None'
            """
        self.execute(sql_query)
        self.commit()
        return True
    
    def get_users(self):
        with self.conn:
            try:
                self.cur.execute("SELECT * FROM Users")
                print(self.cur.fetchall())
            except:
                print("ERROR: Cannot get users from an empty table")
    
    def get_friends(self, user):
        #Get all usernames in database
        with self.conn:
            try:
                self.cur.execute("SELECT * FROM Users")
                friends = [username[0] for username in self.cur.execute(
                    "SELECT username FROM Users")]
                friends.remove(user)
                return friends
            except:
                print("ERROR: Cannot get users from an empty table")
    
    def get_public_key(self, username):
        if (self.check_user_exists(username=username)) == False:
            return 0

        sql_query = """
                SELECT public_key 
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)
        self.cur.execute(sql_query)
        public_key = self.cur.fetchone()
        return public_key

class MSGDatabase():
    '''
        Our SQL message Database

    '''

    def __init__(self, database_arg: str):
        try:
            self.conn = sqlite3.connect(database_arg)
            print("Connect to MSG DB success.")
        except Error as e:
            print(f"Exception: {e}")
            
        self.cur = self.conn.cursor()
        self.id_counter = 1

    def execute(self, sql_string: str):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    def commit(self):
        self.conn.commit()

    def database_setup(self):
        # Create the messages table
        self.execute("""CREATE TABLE IF NOT EXISTS Messages(
            sender TEXT,
            recipient TEXT,
            message TEXT
        )""")

        self.commit()
    
    def add_message(self, sender, recipient, message, db):
    
        if (db.check_user_exists(username=sender) and db.check_user_exists(username=recipient)) == False:
            print("ERROR: Either the sender or the recipient does not exist")
            return False
        
        sql_cmd = """
                INSERT INTO Messages
                VALUES('{sender}', '{recipient}', '{message}')
            """

        sql_cmd = sql_cmd.format(sender = sender, recipient=recipient, message=message)

        self.execute(sql_cmd)
        self.commit()
        
        return True

    def delete_messages(self, recipient):
        sql_query = """
            DELETE FROM Messages
            WHERE recipient = '{recipient}'
        """
        sql_query = sql_query.format(recipient=recipient)
        self.cur.execute(sql_query)
        self.conn.commit()

        return

    def get_messages(self, recipient, db):
        if (db.check_user_exists(username=recipient)) == False:
            return []

        sql_query = """
                SELECT * 
                FROM Messages
                WHERE recipient = '{recipient}'
            """

        sql_query = sql_query.format(recipient=recipient)
        self.cur.execute(sql_query)
        messages = self.cur.fetchall()
        self.delete_messages(recipient)

        ls = [message[2] for message in messages]
        if len(ls) != 0:
            ls.append(db.get_public_key(messages[0][0])[0])

        return ls
        
    def print_table(self):
        with self.conn:
            try:
                self.cur.execute("SELECT * FROM Messages")
                print(self.cur.fetchall())
            except:
                print("ERROR: Cannot print messages from an empty table")

    def database_wipe(self):
        
        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Messages")
        self.commit()