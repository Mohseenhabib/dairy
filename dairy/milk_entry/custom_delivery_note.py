from __future__ import unicode_literals
import frappe
from frappe import _

@frappe.whitelist()
def calculate_crate(doc_name = None):
    if doc_name:
        doc = frappe.get_doc("Delivery Note",doc_name)
        add_crate_count_item_line(doc)
        frappe.db.sql("delete from `tabCrate Count Child` where parent = %s",(doc.name))
        doc = frappe.get_doc("Delivery Note", doc_name)
        dict_create_type = {}
        for itm in doc.items:
            crate_count = frappe.get_doc("Item",itm.item_code)
            if itm.crate_count and itm.crate_type:
                if crate_count.crate_type in dict_create_type.keys():
                    dict_create_type[ itm.crate_type] = dict_create_type[ itm.crate_type] + itm.crate_count
                else:
                    dict_create_type[crate_count.crate_type] = itm.crate_count

        for i in dict_create_type:
            doc.append('crate_count',{
                'crate_type':i,
                'outgoing_count':dict_create_type[i]
            })
        doc.save(ignore_permissions=True)
        return dict_create_type


@frappe.whitelist()
def calculate_crate_after_insert(doc, method):
    if doc:
        doc = frappe.get_doc("Delivery Note",doc.name)
        add_crate_count_item_line(doc)
        frappe.db.sql("delete from `tabCrate Count Child` where parent = %s",(doc.name))
        doc = frappe.get_doc("Delivery Note", doc.name)
        dict_create_type = {}
        for itm in doc.items:
            crate_count = frappe.get_doc("Item", itm.item_code)
            if itm.crate_count and itm.crate_type:
                if crate_count.crate_type in dict_create_type.keys():
                    dict_create_type[itm.crate_type] = dict_create_type[itm.crate_type] + itm.crate_count
                else:
                    dict_create_type[crate_count.crate_type] = itm.crate_count

        for i in dict_create_type:
            doc.append('crate_count',{
                'crate_type':i,
                'outgoing_count':dict_create_type[i]
            })
        doc.save(ignore_permissions=True)
        return dict_create_type

def add_crate_count_item_line(doc):
    if doc:
        for itm in doc.items:
            crate_count = frappe.get_doc("Item", itm.item_code)
            overage = 0
            if crate_count.allow_crate_overage and crate_count.crate_overage:
                overage = crate_count.crate_overage

            # qty = round((itm.qty / (crate_count.crate_quantity * (1 + overage / 100))),2)
            qty = 0
            if crate_count.crate_quantity:
                qty = round((itm.qty / (crate_count.crate_quantity)),2)
            if 0 < qty < 1:
                qty =1.0
            itm.crate_count = float(((str(qty) + ".").split("."))[0])
            itm.crate_type = crate_count.crate_type
            itm.db_update()

# @frappe.whitelist()
# def make_sales_order(source_name, target_doc=None):
#     print("---------------------------make_sales_order")

@frappe.whitelist()
def route_validation(obj, method):
    doc = frappe.get_doc(obj)
    item_code_lst = ['0000']
    for i in doc.items:
        item_code_lst.append(i.item_code)
    query = """select TIG.route_required,TI.name from `tabItem Group` TIG 
                inner join `tabItem` TI on TIG.name =TI.item_group 
                where route_required != 0 and TI.name in {0} """.format(tuple(item_code_lst))
    result = frappe.db.sql(query)
    if result and not doc.route:
        frappe.throw(_("Please select route is Mandatory"))

@frappe.whitelist()
def get_route_price_list(doc_name=None):
    if doc_name:
        route_name = frappe.db.sql("""select link_name from `tabDynamic Link` 
                                where parenttype ='Customer'  
                                and link_doctype ='Route Master' 
                                and parent =%s limit 1""",(doc_name))
        if route_name:
            dic ={}
            doc = frappe.get_doc("Route Master",route_name[0][0])
            dic['route'] = doc.name
            dic['p_list'] = doc.price_list
            dic['warehouse'] = doc.source_warehouse
            return dic
        return  False

@frappe.whitelist()
def get_route_price_list_route(doc_name=None):
    if doc_name:
        route_name = frappe.db.sql("""select parent from `tabDynamic Link`
                                where parenttype ='Customer'
                                and link_doctype ='Route Master'
                                and link_name =%s limit 1""",(doc_name))
        print("*************",route_name)
        if route_name:
            dic = {}
            dic['route'] = route_name[0][0]
            return dic
        return False