import anvil.server
import bcrypt
import anvil.users
from anvil.tables import app_tables
from anvil.server import session 

@anvil.server.callable
def register_user(email, password):
    # Check if the email already exists
    if app_tables.users.get(email=email):
        raise ValueError("Email already exists. Please use a different email.")
    
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Convert the hashed password to a string (encode to base64 to store safely in a text field)
    hashed_password_str = hashed_password.decode('utf-8')  # Convert bytes to string
    
    # Store the new user in the database (with empty items list initially)
    app_tables.users.add_row(email=email, password=hashed_password_str, items=[])
    
    return "User registered successfully"
  
@anvil.server.callable
def check_user_login(email, password):
    # Ensure that password is treated as a string
    if isinstance(password, bytes):
        password = password.decode('utf-8')
    
    # Retrieve the user from the database
    user = app_tables.users.get(email=email)
    
    if user:
        # Compare the entered password with the stored hash
        stored_hash = user['password']
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return True
    
    # If the user doesn't exist or passwords don't match
    return False

# Store the user email in the session on the server-side
@anvil.server.callable
def store_user_email_in_session(email):
    session["user_email"] = email  # Store the email in the session

# Fetch the user's items from the database
@anvil.server.callable
def get_user_items(user_email):
    # Retrieve the user row from the database using the email
    user_row = app_tables.users.get(email=user_email)

    if user_row:
        # Return the list of items (user_item rows) for the logged-in user
        return user_row['items']
    else:
        raise ValueError("User not found in the database.")