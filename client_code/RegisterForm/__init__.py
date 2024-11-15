from ._anvil_designer import RegisterFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RegisterForm(RegisterFormTemplate):

    def __init__(self, **properties):
        # This sets up the form
        self.init_components(**properties)

    def register_button_click(self, **event_args):
        # Using 'self' to access the form components
        username = self.username_box.text
        email = self.email_box.text
        password = self.password_box.text

        if not username or not email or not password:
            alert("All fields are required!")
            return

        # Call the server function to register the user
        result = anvil.server.call('register_user', username, email, password)
        alert(result)

        # If registration is successful, open the login form
        if "successfully" in result:
            open_form('LoginForm')