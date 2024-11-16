from ._anvil_designer import RegisterFormTemplate
from anvil import *
import anvil.server  

class RegisterForm(RegisterFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def login_page_button_click(self, **event_args):
        # Navigate to the LoginForm when the button is clicked
        open_form('LoginForm')

    def register_button_click(self, **event_args):
        email = self.email_box.text.strip()  # Get email and remove leading/trailing spaces
        password = self.password_box.text.strip()  # Get password and remove leading/trailing spaces

        if not email or not password:
            alert("Please enter both email and password!")
            return

        try:
            # Call the server function to register the new user
            result = anvil.server.call('register_user', email, password)
            alert(result)
            
            # If registration is successful, go to the LoginForm
            if "successfully" in result.lower():  # Assuming the server returns a success message with "successfully"
                open_form('LoginForm')  # Navigate to the LoginForm after successful registration
            else:
                alert("Registration failed. Please try again.")

        except Exception as e:
            alert(f"Error: {str(e)}")
