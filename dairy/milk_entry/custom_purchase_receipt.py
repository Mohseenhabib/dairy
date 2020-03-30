from __future__ import unicode_literals
import frappe
from frappe import _

def change_milk_entry_status(pc,method):
    if pc.milk_entry:
        doc = frappe.get_doc("Milk Entry",pc.milk_entry)
        doc.status = "To Bill"
        doc.db_update()