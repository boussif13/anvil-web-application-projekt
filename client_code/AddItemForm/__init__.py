from ._anvil_designer import AddItemFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class AddItemForm(AddItemFormTemplate):
    def __init__(self, user_email=None, **properties):
        self.init_components(**properties)
        self.user_email = user_email  # Store the user email passed from CheckModul

    def submit_button_click(self, **event_args):
        # Get the item details from the form fields
        item_name = self.item_name_textbox.text
        item_description = self.item_description_textbox.text

        if item_name and item_description:
            # Call the server function to add the item, passing all required arguments
            anvil.server.call('add_item', self.user_email, item_name, item_description)
            # Go back to the CheckModul form
            open_form('CheckModul', user_email=self.user_email)
        else:
            alert("Please provide both item name and description.")
