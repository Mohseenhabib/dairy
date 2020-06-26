from __future__ import unicode_literals
import frappe
from frappe import _

def change_milk_entry_status(pc,method):
    if pc.milk_entry:
        doc = frappe.get_doc("Milk Entry",pc.milk_entry)
        res = frappe.db.sql(""" select docstatus from `tabRaw Milk Sample` where name in 
                                (Select distinct(parent) from `tabSample lines`  where milk_entry =%s) limit 1""",(doc.name))
        if res:
            if res[0][0] ==1 and doc.sample_created:
                doc.status = "To Post"
            elif res[0][0] ==0 and doc.sample_created:
                doc.status ="To Post and Sample"
            else:
                doc.status = "To Post and Sample"
        else:
            doc.status = "To Post and Sample"
        doc.db_update()

def change_milk_status(pc,method):
    if pc.milk_entry:
        doc = frappe.get_doc("Milk Entry",pc.milk_entry)
        res = frappe.db.sql("""select docstatus from `tabRaw Milk Sample` where name in 
                                (Select distinct(parent) from `tabSample lines`  where milk_entry =%s) limit 1""",(doc.name))
        if res:
            if res[0][0] ==1 and doc.sample_created:
                doc.status = "Posted"
            elif res[0][0] == 1 and not doc.sample_created:
                doc.status = "Posted"
            else:
                doc.status ="To Sample"
        else:
            doc.status = "To Sample"
        doc.db_update()