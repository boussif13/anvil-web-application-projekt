from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
    def __init__(self, item, **properties):
        self.init_components(**properties)
        
        # Bind the data passed to this template to the labels in the template
        self.item_name.text = item['item_name']
        self.item_description.text = item['item_description']
        self.item_id.text = str(item['item_id'])  # Convert ID to string if it's an integer
        self.item_location.text = item['item_location']
        self.item_date_of_check_in.text = str(item['item_date_of_check_in']) 