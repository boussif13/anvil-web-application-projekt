from ._anvil_designer import RegisterFormTemplate
from anvil import *
import anvil.server  

class RegisterForm(RegisterFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def register_button_click(self, **event_args):
        email = self.email_box.text.strip()  # Get email
        password = self.password_box.text.strip()  # Get password

        if not email or not password:
            alert("Please enter both email and password!")
            return

        try:
            # Call the server function to register the new user
            result = anvil.server.call('register_user', email, password)
            alert(result)
            open_form('LoginForm')  # Open login page after successful registration
        except Exception as e:
            alert(f"Error: {str(e)}")
