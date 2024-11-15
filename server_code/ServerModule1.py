import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import hashlib

def hash_password(password):
    # Use SHA-256 for hashing the password
    return hashlib.sha256(password.encode()).hexdigest()

@anvil.server.callable
def register_user(username, email, password):
    if app_tables.users.get(email=email):
        return "User already exists!"

    password_hash = hash_password(password)
    app_tables.users.add_row(username=username, email=email, password_hash=password_hash)
    return "User registered successfully!"
  

@anvil.server.callable
def login_user(email, password):
    user = app_tables.users.get(email=email)
    if user and user['password_hash'] == hash_password(password):
        return "Login successful!"
    else:
        return "Invalid email or password."