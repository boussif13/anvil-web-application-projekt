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
        item_id = self.item_id_textbox.text  # Get item ID from the textbox
        item_name = self.item_name_textbox.text
        item_description = self.item_description_textbox.text
        item_location = self.item_location_textbox.text  # Get location from the textbox
        item_date_of_check_in = self.item_date_of_check_in_datepicker.date  # Get date from the date picker

        # Ensure that all required fields are filled
        if item_id and item_name and item_description and item_location and item_date_of_check_in:
            # Call the server function to add the item, passing all required arguments
            result = anvil.server.call('add_item', self.user_email, item_id, item_name, item_description, item_location, item_date_of_check_in)
            
            # Check if the result contains an error message
            if result and result.startswith("Item with ID"):
                # If the result message indicates that the item ID already exists, show an alert
                alert(result)  # Display the message returned from the server
            else:
                # If the item is successfully added, go back to CheckModul
                open_form('CheckModul', user_email=self.user_email)
        else:
            alert("Please provide all the required information: item ID, name, description, location, and date of check-in.")
