# Copyright (c) 2013, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.controllers.trends	import get_columns,get_data
from frappe.utils import getdate


# *******************************************************
def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "options": "Item Group",
            "fieldtype": "Link",
            "width": 160
        },
        {
            "label": _("Item"),
            "options": "Item",
            "fieldname": "item",
            "fieldtype": "Link",
            "width": 140
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Warehouse"),
            "options": "Warehouse",
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "width": 160
        },

        {
            "label": _("Delivery Shift"),
            "fieldname": "delivery_shift",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 160
        },
        {
            "label": _("Stock UOM"),
            "options": "UOM",
            "fieldname": "stock_uom",
            "fieldtype": "Link",
            "width": 160
        },
        {
            "label": _("Total Weight"),
            "fieldname": "total_weight",
            "fieldtype": "Float",
            "width": 160
        },
		{
			"label": _(" Weight UOM"),
			"options": "UOM",
			"fieldname": "weight_uom",
			"fieldtype": "Link",
			"width": 160
		},
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Float",
            "width": 160
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "options": "Customer",
            "fieldtype": "Link",
            "width": 160
        }

    ]
    return columns

def get_data(filters):
    print("======")

    if filters:
        if filters.get('based_on'):
            q_data = frappe.db.sql( """
                    select
                        distinct( SOI.%s)
                    from
                        `tabSales Order` SO, `tabSales Order Item` SOI
                    where
                        SO.docstatus =1 and SO.name = SOI.parent
                        """%filters.based_on)
            print("********************************************", q_data)
            field = filters.based_on
            print("*****************",field)
            data = []
            for q in q_data:
                print("************",q)
                if field == "item_group":
                    row = {
                        "item_group": q[0]
                    }
                    data.append(row)

                    p_data = frappe.db.sql(""" select SOI.item_group, SOI.item_code, SOI.item_name, SO.set_warehouse, 
                    SO.delivery_shift, SOI.qty, SOI.stock_uom, SOI.total_weight,SOI.weight_uom, SOI.amount, SO.customer
                    from `tabSales Order` SO, `tabSales Order Item` SOI
                    where
                    SO.docstatus =1 and SO.name = SOI.parent and SOI.item_group = %(item_group)s 
                     group by SOI.item_code """,{'item_group':q[0]})
                    for p in p_data:
                        row = {
                            # "item_group": q[0],
                            "item": p[1],
                            "item_name": p[2],
                            "warehouse": p[3],
                            "delivery_shift": p[4],
                            "qty": p[5],
                            "stock_uom": p[6],
                            "total_weight": p[7],
                            "weight_uom": p[8],
                            "amount":p[9],
                            "customer":p[10]
                        }
                        data.append(row)

            return data

        # else:
        query = """
            select
                SOI.item_group, SOI.item_code, SOI.item_name, SO.set_warehouse, SO.delivery_shift, SOI.qty, SOI.stock_uom,
                SOI.total_weight,SOI.weight_uom, SOI.amount, SO.customer
            from
                `tabSales Order` SO, `tabSales Order Item` SOI
            where
                SO.docstatus =1 and SO.name = SOI.parent
                """
        conditions = get_conditions(filters)
        print(""" conditions """,conditions)
        # print("====query",query+conditions)
        print("__-____-_",query + conditions)
        q_data = frappe.db.sql(query + conditions)
        # print("q_data **************************************",q_data)
        data = []
        for q in q_data:
            row = {
                "item_group": q[0],
                "item": q[1],
                "item_name": q[2],
                "warehouse": q[3],
                "delivery_shift": q[4],
                "qty": q[5],
                "stock_uom": q[6],
                "total_weight": q[7],
                "weight_uom": q[8],
                "amount":q[9],
                "customer":q[10]
            }
            data.append(row)

        return data


def get_conditions(filters):

    if filters:
        # query = """   and  date >= '{0}' and  date <= '{1}'  """.format(filters.from_date,filters.to_date)
        query = """ and SO.name = SOI.parent """
        if filters.get('company'):
            query += """ and  SO.company = '%s'  """%filters.company
        if filters.get('group_by'):
            var = filters.get('group_by')
            if var == "item_code":
                query += """   group by  SOI.%s  """%filters.group_by
            else:
                query += """   group by  SO.%s  """ % filters.group_by
        if filters.get('shift'):
            query += """ and  SO.delivery_shift = '%s' """%filters.shift
        if filters.get('warehouse'):
            query += """ and  SO.set_warehouse = '%s' """%filters.warehouse
        if filters.get('from_date'):
            query += """ and  SO.delivery_date > '%s' """%filters.from_date
        if filters.get('to_date'):
            query += """ and  SO.delivery_date < '%s' """%filters.to_date


        return query