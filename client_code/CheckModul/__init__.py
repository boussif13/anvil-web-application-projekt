from ._anvil_designer import CheckModulTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables


class CheckModul(CheckModulTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Retrieve the user email from the session
        user_email = anvil.server.session.get('user_email')

        if user_email:
            # Fetch user items after navigation
            items = anvil.server.call('get_user_items')

            if items:
                # Loop through the items and display them
                item_names = [f"{item['item_name']}: {item['item_description']}" for item in items]
                alert(f"Your items:\n{', '.join(item_names)}")
            else:
                alert("You have no items yet.")
        else:
            open_form('LoginForm')  # If no user is logged in, open the login form
