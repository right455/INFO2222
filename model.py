'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
import sql
import crypto
import json

# Initialise our views, all arguments are defaults for the template
page_view = view.View()
database_args = ":sql.db:"
msg_args = ":msg.db:"
sql_db = sql.SQLDatabase(database_args)
msg_db = sql.MSGDatabase(msg_args)
sql_db.database_setup("password")
msg_db.database_setup()

#msg_db.add_message("123", "123", "hello", sql_db)
#print(msg_db.get_messages("123", sql_db))

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index(username):
    '''
        index
        Returns the view for the index
    '''
    if username != None:
        change_header("user")
    else:
        change_header("header")

    return page_view("index")

def change_header(header):
    if header == "user":
        page_view.change_header("user")
        return True
    elif header == "header":
        page_view.change_header("header")
        return True
    
    print("ERROR: Invalid header")
    return False

#-----------------------------------------------------------------------------
# Sign up
#-----------------------------------------------------------------------------

def sign_up_form():
    '''
        sign_up_form
        Returns the view for the sign_up_form
    '''
    return page_view("sign_up")

#-----------------------------------------------------------------------------

# Check the sign up credentials
def sign_up_check(username, password, public_key):
    '''
        sign_up_check
        Store usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    sign_up = sql_db.add_user(username, password, 0)
    
    if sign_up:
        sql_db.login_user(username, public_key)
        change_header("user")
        return page_view("valid", name=username)
    else:
        err_str = "Invalid username, cannot have the same one as someone else"
        return page_view("invalid", reason=err_str)


#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password, public_key):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = True
    
    if sql_db.check_user_exists(username=username) != True:
        err_str = "Incorrect Username"
        login = False
        
    elif sql_db.check_credentials(username, password) != True:
        err_str = "Incorrect Password"
        login = False
    
    elif sql_db.check_user_online(username) == True:
        err_str = "User Already Online"
        login = False
    
    if login:
        sql_db.login_user(username, public_key)
        page_view.change_header("user")
        return page_view("valid", name=username)
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# User Page
#-----------------------------------------------------------------------------

# def user():
#     '''
#         user
#         Returns the view for the index after login
#     '''
#     print(current_user)
#     sql_db.login_user(current_user)
#     page_view.change_header("user")
#     sql_db.get_users()
#     return page_view("index")


#-----------------------------------------------------------------------------
# Logout
#-----------------------------------------------------------------------------

def logout(username):
    '''
        logout
        Returns the view for the index after logout
    '''
    sql_db.logout_user(username)
    change_header("header")
    return page_view("index")

#-----------------------------------------------------------------------------
# Friends
#-----------------------------------------------------------------------------
def friends():
    '''
        Friends
        Returns the view page for friends
    '''

    return page_view("friends")    

def send_message(recipient, message, sender):
    '''
        Send message
        Returns the view for the message after pressing send in friends
    '''

    if sql_db.check_user_exists(username=recipient) == False:
        err_str = "Invalid recipient"
        return page_view("invalid", reason=err_str)

    msg_db.add_message(sender, recipient, message, sql_db)
    msg_db.print_table()
    return page_view("valid_message")  

def get_message(recipient):
    return msg_db.get_messages(recipient, sql_db)


def get_public_key(username):
    return sql_db.get_public_key(username)

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)