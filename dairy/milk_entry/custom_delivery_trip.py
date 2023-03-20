from __future__ import unicode_literals
import frappe
from frappe import _

@frappe.whitelist()
def get_jinja_data(doc):
	res =frappe.db.sql("""
	select 
            ds.customer,ds.delivery_note,
            dn.route,
            dni.item_code,dni.item_name,dni.qty,dni.uom,dni.total_weight,dni.crate_count
        from
            `tabDelivery Trip` dt, `tabDelivery Stop` ds, `tabDelivery Note` dn, `tabDelivery Note Item` dni
        where 
            dt.docstatus =1 and dt.name = %(name)s and ds.parent = %(name)s and dn.name = ds.delivery_note and dni.parent = ds.delivery_note
             
             """,{"name":doc.name}, as_dict=True)

	return res

# *******************  Following Methods Use in gate pass print format  *******************************

@frappe.whitelist()
def get_jinja_data_del_note(doc):
	res = frappe.db.sql("""
	select distinct(delivery_note) from `tabGate Pass Item` where parent = %(name)s """, {"name": doc.name}, as_dict=True)
	return res

@frappe.whitelist()
def del_note_details(del_note):
	res = frappe.db.sql("""
	select 
		name,customer_name,route
	from 
		`tabDelivery Note` where name = %(name)s """, {"name": del_note}, as_dict=True)
	return res

@frappe.whitelist()
def get_jinja_data_del_note_item(del_note):
	res = frappe.db.sql("""
	select 
		A.item_code,A.item_name,A.batch_no,A.stock_uom,A.stock_qty,B.free_qty,B.outgoing_count,B.incoming_count,B.crate_type
	from 
		`tabDelivery Note Item` A
	right outer Join `tabCrate Count Child` B
	on A.item_code = B.item_code
	where 
		A.parent = %(name)s and B.parent = %(name)s and A.is_free_item = 0 """, {"name": del_note}, as_dict=True)

	dist_itm = frappe.db.sql(""" select distinct(item_code) from `tabDelivery Note Item` where parent = %(name)s """,
							 {'name':del_note})
	for itm in dist_itm:
		obj = frappe.get_doc("Item",itm[0])
		if len(obj.crate) == 0:
			res2 = frappe.db.sql(""" select item_code,item_name,batch_no,stock_uom,sum(stock_qty) as stock_qty
									from `tabDelivery Note Item` where parent = %(name)s and item_code = %(item_code)s""",
								{'name':del_note,'item_code':obj.item_code}, as_dict=True)

			for i in range(0, len(res2)):
				res.append(res2[i])


	return res

@frappe.whitelist()
def del_note_total(del_note):
	f_res = []
	res = {}

	supp_qty = frappe.db.sql(""" select sum(stock_qty) as stock_qty  from `tabDelivery Note Item` 
								 where parent = %(name)s and is_free_item = 0""",{'name':del_note},as_dict=True)
	res["stock_qty"] = supp_qty[0]["stock_qty"]

	free_qty = frappe.db.sql(""" select sum(stock_qty) as fre_qty from `tabDelivery Note Item` 
								 where parent = %(name)s and is_free_item = 1""",{'name':del_note},as_dict=True)
	res["fre_qty"] = free_qty[0]["fre_qty"]

	crate_qty = frappe.db.sql(""" select sum(outgoing_count) as crate_qty from `tabCrate Count Child` 
								  where parent = %(name)s """,{'name':del_note},as_dict=True)
	res["crate_qty"] = crate_qty[0]["crate_qty"]

	f_res.append(res)
	return f_res

@frappe.whitelist()
def total_supp_qty_based_on_itm_grp(gate_pass):
	itm_grp = frappe.db.sql(""" select item_group_name from `tabItem Group` where is_total_supplier_quantity_item_group_ = 1 """,as_dict=True)
	based_itm_grp =  itm_grp[0]['item_group_name']

	total_qty = frappe.db.sql(""" select sum(total_weight) from `tabMerge Gate Pass Item` where parent = %(gate_pass)s and 
	 								item_group = %(item_group)s """,{'gate_pass':gate_pass,'item_group':based_itm_grp})
	final_total_qty = total_qty[0][0]

	return final_total_qty

@frappe.whitelist()
def warehouse_address(warehouse):
	lst = []
	org_warehouse = warehouse.split(" ")
	print("*************************",org_warehouse)
	address =  frappe.db.sql(""" select address_line_1, address_line_2, city, state, pin, phone_no, mobile_no 
	 				from `tabWarehouse` where warehouse_name = %(warehouse)s """,{'warehouse':org_warehouse[0]},as_dict=True)
	print("*******************",address)
	add = ''
	for f in ['address_line_1', 'address_line_2', 'city', 'state', 'pin']:
		if address[0][f]:
			add += address[0][f] + " "
	lst.append(add)
	cont = ''
	for f in ['phone_no', 'mobile_no']:
		if address[0][f]:
			cont += address[0][f] + "  "
	lst.append(cont)
	print("**********************************",lst)
	return lst


