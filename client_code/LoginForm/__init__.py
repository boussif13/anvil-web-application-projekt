from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class LoginForm(LoginFormTemplate):

    def __init__(self, **properties):
        # This sets up the form
        self.init_components(**properties)

    def login_button_click(self, **event_args):
        # Get the email and password from input boxes
        email = self.email_box.text
        password = self.password_box.text

        if not email or not password:
            alert("Please enter both email and password!")
            return

        # Call the server function to login the user
        result = anvil.server.call('login_user', email, password)
        alert(result)

        # If login is successful, open the dashboard or main page
        if "successful" in result:
            open_form('CheckModul')  

    def form_refreshing_data_bindings(self, **event_args):
      """This method is called when refresh_data_bindings is called"""
      pass
