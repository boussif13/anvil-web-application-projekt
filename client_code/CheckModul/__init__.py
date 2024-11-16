from ._anvil_designer import CheckModulTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables


class CheckModul(CheckModulTemplate):
    def __init__(self, user_email=None, **properties):
        self.init_components(**properties)

        # Store the user_email passed from LoginForm
        self.user_email = user_email

        # Fetch the user's items (assuming you're calling a server function)
        if self.user_email:
            try:
                items = anvil.server.call('get_user_items', self.user_email)

                if items:
                    # Prepare the item details to be displayed, including the new columns
                    item_details = [{'item_name': item['item_name'],
                                     'item_description': item['item_description'],
                                     'item_id': item['item_id'],
                                     'item_location': item['item_location'],
                                     'item_date_of_check_in': item['item_date_of_check_in']} for item in items]

                    # Set the items to the RepeatingPanel (assuming it is named repeating_panel_items)
                    self.repeating_panel_items.items = item_details
                else:
                    alert("You have no items yet.")
            except Exception as e:
                alert(f"Error fetching user items: {str(e)}")
        else:
            open_form('LoginForm')  # If no user email exists, prompt login

    def add_item_button_click(self, **event_args):
        # Open a form to add a new item, passing the user_email
        open_form('AddItemForm', user_email=self.user_email)

    def delete_item_click(self, **event_args):
        # Open the DeleteForm and pass the user_email to it
        open_form('DeleteForm', user_email=self.user_email)
