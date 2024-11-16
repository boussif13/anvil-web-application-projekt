from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables

class LoginForm(LoginFormTemplate):

    def login_button_click(self, **event_args):
        # Get user input
        email = self.email_box.text.strip()  # Ensure you trim whitespace
        password = self.password_box.text.strip()

        if not email or not password:
            alert("Please enter both email and password!")
            return

        # Ensure password is a string before sending it to the server
        password = str(password)  # Convert to string just in case

        # Call the server function to check the user's credentials
        is_valid = anvil.server.call('check_user_login', email, password)

        if is_valid:
            # Login successful, navigate to CheckModule form
            alert("Login successful!")
            open_form('CheckModul',user_email=email)
        else:
            # Login failed, show error message
            alert("Invalid email or password. Please try again.")
