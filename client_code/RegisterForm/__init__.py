import re
from ._anvil_designer import RegisterFormTemplate
from anvil import *
import anvil.server

class RegisterForm(RegisterFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
      
    def email_is_valid(self, email):
        """Check if the email format is valid using regex."""
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email) is not None

    def login_page_button_click(self, **event_args):
        # This will take the user to the LoginForm when the button is clicked
        open_form('LoginForm')

    def register_button_click(self, **event_args):
        email = self.email_box.text.strip()  # Get email
        password = self.password_box.text.strip()  # Get password

        if not email or not password:
            alert("Please enter both email and password!")
            return

        # Validate email format
        if not self.email_is_valid(email):
            alert("Please enter a valid email address!")
            return

        try:
            # Call the server function to register the new user
            result = anvil.server.call('register_user', email, password)
            alert(result)
            open_form('LoginForm')  # Open login page after successful registration
        except Exception as e:
            alert(f"Error: {str(e)}")
