from ._anvil_designer import RegisterFormTemplate
import anvil.server
from anvil import *

class RegisterForm(RegisterFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def register_button_click(self, **event_args):
        username = self.username_box.text
        email = self.email_box.text
        password = self.password_box.text

        if not username or not email or not password:
            alert("Please fill out all fields!")
            return

        # Call the server function to register the user
        result = anvil.server.call('register_user', username, email, password)
        alert(result)

        if "successfully" in result:
            open_form('LoginForm')  # Go to LoginForm after successful registration
