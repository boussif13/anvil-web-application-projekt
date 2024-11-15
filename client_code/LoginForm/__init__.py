from ._anvil_designer import LoginFormTemplate
import anvil.users
from anvil import *

class LoginForm(LoginFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def login_button_click(self, **event_args):
        email = self.email_box.text.strip()  # Ensure no leading/trailing spaces
        password = self.password_box.text.strip()

        if not email or not password:
            alert("Please enter both email and password!")
            return

        try:
            # Attempt to log the user in
            user = anvil.users.login(email=email, password=password)
            
            # If login is successful, show a success alert and move to the next form
            alert("Login successful!")
            open_form('CheckModul')  # Redirect to CheckModul after successful login
        except anvil.users.AuthenticationFailed:
            alert("Invalid email or password. Please try again.")
