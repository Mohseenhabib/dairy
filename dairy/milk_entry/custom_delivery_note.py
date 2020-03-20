from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def calculate_crate(doc_name = None):
    if doc_name:
        doc = frappe.get_doc("Delivery Note",doc_name)
        frappe.db.sql("delete from `tabCrate Count Child` where parent = %s",(doc.name))
        dict_create_type = {}
        for itm in doc.items:
            crate_count = frappe.get_doc("Item",itm.item_code)
            if crate_count.crate_quantity and crate_count.crate_type:
                count =0
                qty = itm.qty
                while(qty > 0):
                    count += 1
                    qty = qty - crate_count.crate_quantity

                if crate_count.crate_type in dict_create_type.keys():
                    dict_create_type[crate_count.crate_type] = dict_create_type[crate_count.crate_type]+count
                else:
                    dict_create_type[crate_count.crate_type] = count
        for i in dict_create_type:
            doc.append('crate_count',{
                'crate_type':i,
                'outgoing_count':dict_create_type[i]
            })
        doc.save(ignore_permissions=True)
        return dict_create_type


@frappe.whitelist()
def calculate_crate_after_insert(doc,method):
    if doc:
        doc = frappe.get_doc("Delivery Note",doc.name)
        frappe.db.sql("delete from `tabCrate Count Child` where parent = %s",(doc.name))
        dict_create_type = {}
        for itm in doc.items:
            crate_count = frappe.get_doc("Item",itm.item_code)
            count =0
            qty = itm.qty
            while(qty > 0):
                count += 1
                qty = qty - crate_count.crate_quantity

            if crate_count.crate_type in dict_create_type.keys():
                dict_create_type[crate_count.crate_type] = dict_create_type[crate_count.crate_type]+count
            else:
                dict_create_type[crate_count.crate_type] = count
        for i in dict_create_type:
            doc.append('crate_count',{
                'crate_type':i,
                'outgoing_count':dict_create_type[i]
            })
        doc.save(ignore_permissions=True)
        return dict_create_type