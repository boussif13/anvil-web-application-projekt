from ._anvil_designer import CheckModulTemplate
import anvil.server
import anvil.users
from anvil import *

class CheckModul(CheckModulTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.show_user_items()

    def show_user_items(self):
        user = anvil.users.get_user()  # Get the current logged-in user
        if user is None:
            alert("You need to log in to see your items!")
            open_form('LoginForm')  # Redirect to login if not logged in
            return
        
        user_email = user['email']  # Get email of the logged-in user
        items = anvil.server.call('get_user_items', user_email)

        if items is None or len(items) == 0:
            alert("No items found!")
        else:
            # Bind the fetched items to the repeating panel
            self.repeating_panel_1.items = items

    def add_item_button_click(self, **event_args):
        user = anvil.users.get_user()

        if user is None:
            alert("You need to log in to add items!")
            open_form('LoginForm')
            return
        
        name = self.name_box.text
        quantity = self.quantity_box.text
        location = self.location_box.text

        if not name or not quantity or not location:
            alert("All fields are required!")
            return

        result = anvil.server.call('add_item', user['email'], name, int(quantity), location)
        alert(result)

        # Refresh the item list
        self.show_user_items()
