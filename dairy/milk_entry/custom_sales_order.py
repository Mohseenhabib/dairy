from __future__ import unicode_literals
import frappe

def before_submit(sales, method):
    if frappe.db.get_single_value("Dairy Settings", "leakage_percentage") and frappe.db.get_single_value("Dairy Settings", "leakage_qty"):
        leakage_perc = float(frappe.db.get_single_value("Dairy Settings", "leakage_percentage"))
        leakage_qty = float(frappe.db.get_single_value("Dairy Settings", "leakage_qty"))
        applicable_on = (frappe.db.get_single_value("Dairy Settings", "applicable_on"))
        lst = []
        for line in sales.items:
            lst.append(line)
        for line in lst:
            item = frappe.get_doc("Item",line.item_code)
            if item.leakage_applicable and applicable_on == "Stock UOM" and line.stock_qty > leakage_qty:
                qty = (line.stock_qty * leakage_perc)/100
                uom = frappe.get_doc("UOM",line.stock_uom)
                if uom.must_be_whole_number:
                    qty = round((line.stock_qty * leakage_perc) / 100)
                if qty == 0:
                    qty = 1
                sales.append("items",{
                    "item_code": line.item_code,
                    "item_name": line.item_name,
                    "delivery_date": line.delivery_date,
                    "description": str(line.description)+" Leakage Scheme applied",
                    "gst_hsn_code": line.gst_hsn_code,
                    "is_nil_exempt": line.is_nil_exempt,
                    "qty": qty,
                    "uom": line.stock_uom,
                    "stock_uom": line.stock_uom,
                    "rate": 0.0,
                    "warehouse": line.warehouse,
                    "is_free_item": 1,
                    "price_list_rate": 0
                })
                sales.validate()

            if item.leakage_applicable and applicable_on == "Order UOM" and line.qty > leakage_qty:
                qty = (line.qty * leakage_perc)/100
                uom1 = frappe.get_doc("UOM", line.stock_uom)
                uom2 = frappe.get_doc("UOM", line.uom)
                if uom1.must_be_whole_number or uom2.must_be_whole_number:
                    qty = round((line.qty * leakage_perc) / 100)
                if qty == 0:
                    qty = 1
                sales.append("items",{
                    "item_code": line.item_code,
                    "item_name": line.item_name,
                    "delivery_date": line.delivery_date,
                    "description": str(line.description)+" Leakage Scheme applied",
                    "gst_hsn_code": line.gst_hsn_code,
                    "is_nil_exempt": line.is_nil_exempt,
                    "qty": qty,
                    "uom": line.uom,
                    "stock_uom": line.stock_uom,
                    "rate": 0.0,
                    "warehouse": line.warehouse,
                    "is_free_item": 1,
                    "price_list_rate": 0
                })
                sales.validate()

@frappe.whitelist()
def validate_multiple_orders(customer,delivery_shift,route,delivery_date):
    if frappe.db.get_single_value("Dairy Settings", "restrict_multiple_orders_in_single_shift"):
        result = 0
        pre_sale_order = frappe.db.sql("""select count(*) from `tabSales Order` where customer = %(customer)s and
          delivery_shift = %(delivery_shift)s and route = %(route)s and delivery_date = %(delivery_date)s and docstatus = 1 """,
         {'customer': customer, 'delivery_shift': delivery_shift, 'route':route,'delivery_date':delivery_date})
        result = pre_sale_order[0][0]
        if (result > 0):
            return 1


@frappe.whitelist()
def validate_multiple_orders_in_quotation(customer,delivery_shift,route,delivery_date):

    if frappe.db.get_single_value("Dairy Settings", "restrict_multiple_orders_in_single_shift"):
        result = 0
        pre_sale_order = frappe.db.sql("""select count(*) from `tabQuotation` where customer_name = %(customer)s and
          delivery_shift = %(delivery_shift)s and route = %(route)s and delivery_date = %(delivery_date)s and docstatus = 1 """,
         {'customer': customer, 'delivery_shift': delivery_shift, 'route':route,'delivery_date':delivery_date})
        result = pre_sale_order[0][0]
        if(result > 0):
            return 1

@frappe.whitelist()
def order_role():
    role = frappe.get_roles(frappe.session.user)
    fixed_role = frappe.db.get_single_value("Dairy Settings", "order_controller")
    if fixed_role in role:
        return 1

@frappe.whitelist()
def get_customer(doc_name):
    route = list(frappe.db.sql(""" select link_name from `tabDynamic Link` where parent = %(doc_name)s and link_doctype = "Route Master" """,{"doc_name": doc_name}))
    return route

@frappe.whitelist()
def set_territory():
    territory = frappe.db.get_single_value("Dairy Settings", "get_territory")
    return territory

