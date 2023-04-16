'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

from bottle import route, get, post, error, request, static_file, response
import json
import model

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    username = request.get_cookie('username')

    return model.index(username)

#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()


#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    public_key = request.forms.get('public_key')
    
    
    # Call the appropriate method
    response.set_cookie('username', username)
    return model.login_check(username, password, public_key)


#-----------------------------------------------------------------------------

# Display the sign up page
@get('/sign_up')
def get_sign_up_controller():
    '''
        get_sign_up
        
        Serves the sign_up page
    '''
    return model.sign_up_form()

#-----------------------------------------------------------------------------

# Attempt the sign up
@post('/sign_up')
def post_sign_up():
    '''
        post_sign_up
        
        Handles sign up attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    public_key = request.forms.get('public_key')
    
    # Call the appropriate method
    response.set_cookie('username', username)
    response.set_cookie('public_key', public_key)
    return model.sign_up_check(username, password, public_key)

#-----------------------------------------------------------------------------

# Redirect to user page
@post('/valid')
def post_valid():
    '''
        post_valid
    '''
    
    # Call the appropriate method
    return model.user()

#-----------------------------------------------------------------------------

# Attempt logout
@get('/logout')
def get_logout_controller():
    '''
        get_logout
        
        Logout from current user
    '''
    username = request.get_cookie('username')
    response.delete_cookie('username')
    return model.logout(username)

#-----------------------------------------------------------------------------

# Friends
@get('/friends')
def get_logout_controller():
    '''
        Friends page
        
    '''

    return model.friends()

#-----------------------------------------------------------------------------

@post('/send_message')
def send_message():
    recipient = request.forms.get('recipient')
    message = request.forms.get('message')
    sender = request.get_cookie('username')

    #print("Recipient: " + recipient + " Message: " + message + " Sender: " + sender)
    return model.send_message(recipient, message, sender)

@get('/get_messages')
def get_messages():
    recipient = request.get_cookie('username')

    messages = model.get_message(recipient)

    # Convert the messages to JSON and return them
    response.content_type = 'application/json'

    return json.dumps(messages)


@get('/get_friends')
def get_friends():
    user = request.get_cookie('username')
    friends = model.get_friends(user)

    # Convert the messages to JSON and return them
    response.content_type = 'application/json'

    return json.dumps(friends)


@get('/get_public_key/<recipient>')
def get_public_key(recipient):
    public_key = model.get_public_key(recipient)

    response.content_type = 'application/json'
    #print(public_key)
    return json.dumps({"public_key": public_key})

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()
#-----------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error): 
    return model.handle_errors(error)
