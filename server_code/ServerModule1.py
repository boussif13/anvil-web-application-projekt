import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *

import bcrypt

@anvil.server.callable
def register_user(username, email, password):
    if app_tables.users.get(email=email):
        return "User already exists!"
    
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    app_tables.users.add_row(username=username, email=email, password_hash=password_hash)
    return "User registered successfully!"

@anvil.server.callable
def login_user(email, password):
    user = app_tables.users.get(email=email)
    if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        return "Login successful!"
    else:
        return "Invalid email or password."