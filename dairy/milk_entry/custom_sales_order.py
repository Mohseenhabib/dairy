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
            if item.leakage_applicable and applicable_on == "Stock UOM" and line.stock_qty > leakage_qty :
                sales.append("items",{
                    "item_code": line.item_code,
                    "item_name": line.item_name,
                    "delivery_date": line.delivery_date,
                    "description": str(line.description)+" Leakage Scheme applied",
                    "gst_hsn_code": line.gst_hsn_code,
                    "is_nil_exempt": line.is_nil_exempt,
                    "qty": (line.stock_qty * leakage_perc)/100,
                    "uom": line.stock_uom,
                    "stock_uom": line.stock_uom,
                    # "conversion_factor": line.conversion_factor,
                    "rate": 0.0,
                    # "rate": line.rate,
                    "warehouse": line.warehouse,
                })
                sales.validate()

            if item.leakage_applicable and applicable_on == "Order UOM" and line.qty > leakage_qty :
                sales.append("items",{
                    "item_code": line.item_code,
                    "item_name": line.item_name,
                    "delivery_date": line.delivery_date,
                    "description": str(line.description)+" Leakage Scheme applied",
                    "gst_hsn_code": line.gst_hsn_code,
                    "is_nil_exempt": line.is_nil_exempt,
                    "qty": (line.qty * leakage_perc)/100,
                    "uom": line.uom,
                    "stock_uom": line.stock_uom,
                    # "conversion_factor": line.conversion_factor,
                    "rate": 0.0,
                    # "rate": line.rate,
                    "warehouse": line.warehouse,
                })
                sales.validate()

