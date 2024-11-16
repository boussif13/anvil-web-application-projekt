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

@anvil.server.callable
def add_item(user_email, item_id, item_name, item_description, item_location, item_date_of_check_in):
    if user_email:
        # Step 1: Check if the item_id already exists for the user
        existing_item = app_tables.user_item.get(user_email=user_email, item_id=item_id)
        if existing_item:
            # If item with the same ID exists, return a message instead of raising an exception
            return "Item with ID {} already exists for this user. Please use a different ID.".format(item_id)

        # Step 2: Add a new item to the user_item table, including the new fields
        item_row = app_tables.user_item.add_row(
            user_email=user_email, 
            item_id=item_id, 
            item_name=item_name, 
            item_description=item_description, 
            item_location=item_location, 
            item_date_of_check_in=item_date_of_check_in
        )

        # Step 3: Find the user row in the users table
        user = app_tables.users.get(email=user_email)
        if user:
            # Step 4: Retrieve the current list of items for this user
            user_items = user['items'] or []

            # Step 5: Append the new item row to the user's list and update the column explicitly
            user_items.append(item_row)
            user['items'] = user_items  # Explicitly set the updated list back to the column

        else:
            return f"User with email {user_email} not found."
    else:
        return "User email is required."

@anvil.server.callable
def delete_item(item_id):
    try:
        # Find the item in the user_item table
        item = app_tables.user_item.get(item_id=item_id)
        
        if item:
            # Find the user who owns the item
            user_email = item['user_email']
            user = app_tables.users.get(email=user_email)
            
            if user:
                # Remove the item from the user's items list (if it's there)
                user_items = user['items'] or []
                user_items = [i for i in user_items if i['item_id'] != item_id]
                user['items'] = user_items  # Save the updated list
                
                # Now, delete the item from the user_item table
                item.delete()
                
                return True  # Return True to indicate success
            else:
                return f"User with email {user_email} not found."
        else:
            return "Item not found."
    
    except Exception as e:
        return f"Error deleting item: {str(e)}"


 