# Copyright (c) 2013, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [

        {
            "label": _("Customer"),
            "options": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "width": 150
        },
        {
            "label": _("Route"),
            "options": "Route Master",
            "fieldname": "route",
            "fieldtype": "Link",
            "width": 150
        },
        {
            "label": _("Delivery Note"),
            "options": "Delivery Note",
            "fieldname": "delivery_note",
            "fieldtype": "Link",
            "width": 150
        },
        {
            "label": _("Delivery Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Vehicle"),
            "options":"Vehicle",
            "fieldname": "vehicle",
            "fieldtype": "Link",
            "width": 150
        },
        {
            "label": _("Item"),
            "options": "Item",
            "fieldname": "item",
            "fieldtype": "Link",
            "width": 150
        },
        {
            "label": _("Crate Count"),
            "fieldname": "crate_count",
            "fieldtype": "Float",
            "width": 100
        }
    ]
    return columns

def get_data(filters):
    data =[]

    result = frappe.db.sql("""select TDN.customer,TDN.route,TDN.name,TDN.posting_date,TR.vehicle,TDNI.item_code,TDNI.crate_count 
                            from `tabDelivery Note` TDN 
                            inner join `tabDelivery Note Item` TDNI on TDNI.parent =TDN.name
                            inner join `tabRoute Master` TR on TR.name = TDN.route""",as_dict =True)
    for res in result:
        data.append({
            "customer":res.get('customer'),
            "route":res.get('route'),
            "delivery_note":res.get('name'),
            "date":res.get('posting_date'),
            "vehicle":res.get('vehicle'),
            "item":res.get('item_code'),
            "crate_count":res.get('crate_count')
        })
    return data