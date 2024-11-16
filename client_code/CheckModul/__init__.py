from ._anvil_designer import CheckModulTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables


class CheckModul(CheckModulTemplate):
    def __init__(self, user_email=None, **properties):
        self.init_components(**properties)

        # Store the user_email passed from LoginForm
        self.user_email = user_email

        # Now, you can use this user_email to fetch items for the user
        if self.user_email:
            items = anvil.server.call('get_user_items', self.user_email)

            if items:
                # Prepare the item names and descriptions to be displayed
                item_names = [{'item_name': f"{item['item_name']}: {item['item_description']}"} for item in items]

                # Set the items to the RepeatingPanel (assuming it is named repeating_panel_items)
                self.repeating_panel_items.items = item_names
            else:
                alert("You have no items yet.")
        else:
            open_form('LoginForm')  # If no user email exists, prompt login
          
    def add_item_button_click(self, **event_args):
        # Open a form to add a new item
        open_form('AddItemForm',user_email=self.user_email)