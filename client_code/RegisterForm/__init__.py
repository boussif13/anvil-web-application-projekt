from ._anvil_designer import RegisterFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RegisterForm(RegisterFormTemplate):
    def register_button_click(self, **event_args):
        username = self.username_box.text
        email = self.email_box.text
        password = self.password_box.text
        
        result = anvil.server.call('register_user', username, email, password)
        alert(result)
        if "successfully" in result:
            open_form('LoginForm')