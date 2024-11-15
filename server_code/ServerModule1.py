import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
import hashlib
import datetime

# Hash the password before storing it
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new user
@anvil.server.callable
def register_user(username, email, password):
    # Check if the user already exists by email
    if app_tables.users.get(email=email):
        return "User already exists!"
    
    # Hash the password before storing it
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new user
@anvil.server.callable
def register_user(username, email, password):
    if app_tables.users.get(email=email):
        return "User already exists!"
    
    password_hash = hash_password(password)
    
    # Create the user, do not set confirmed_email here unless it's required
    app_tables.users.add_row(username=username, email=email, password_hash=password_hash, enabled=False)
    
    return "User registered successfully!"

# Login a user
@anvil.server.callable
def login_user(email, password):
    user = app_tables.users.get(email=email)
    if user:
        # Compare the hashed password
        if user['password_hash'] == hash_password(password):
            return user  # Successful login, return the user object
    return None  # Login failed

# Get items for the logged-in user
@anvil.server.callable
def get_user_items(user_email):
    user = app_tables.users.get(email=user_email)
    
    if user:
        # Retrieve items that belong to the logged-in user
        items = app_tables.items.search(user=user)
        return items
    else:
        return []

# Add an item to the user's inventory
@anvil.server.callable
def add_item(user_email, name, quantity, location):
    user = app_tables.users.get(email=user_email)
    
    if user:
        app_tables.items.add_row(
            user=user,  # Link the item to the user
            name=name,
            quantity=quantity,
            location=location,
            date_of_check_in=datetime.datetime.utcnow()  # Add current time for check-in
        )
        return "Item added successfully!"
    else:
        return "User not found!"
