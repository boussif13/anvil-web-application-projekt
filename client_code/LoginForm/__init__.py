from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class LoginForm(LoginFormTemplate):
    def login_button_click(self, **event_args):
        email = self.email_box.text
        password = self.password_box.text
        
        result = anvil.server.call('login_user', email, password)
        alert(result)
        if "successful" in result:
            open_form('MainForm')  # Redirect to your main form
