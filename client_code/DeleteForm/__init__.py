from ._anvil_designer import DeleteFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class DeleteForm(DeleteFormTemplate):
    def __init__(self, user_email=None, **properties):
        self.init_components(**properties)
        self.user_email = user_email  # Capture the user_email passed from CheckModul

    def delete_button_click(self, **event_args):
        item_id = self.item_id_box.text.strip()  # Get item_id entered by the user

        if not item_id:
            alert("Please enter an item ID!")
            return

        try:
            # Call the server function to delete the item based on the item_id
            result = anvil.server.call('delete_item', item_id)

            if result is True:
                alert("Item deleted successfully!")
                open_form('CheckModul', user_email=self.user_email)
            else:
                alert(result)  # Display the error message from the server function

        except Exception as e:
            alert(f"Error: {str(e)}")
          
    def cancel_button_click(self, **event_args):
        # Open the CheckModul form and pass the user_email to it
        open_form('CheckModul', user_email=self.user_email)