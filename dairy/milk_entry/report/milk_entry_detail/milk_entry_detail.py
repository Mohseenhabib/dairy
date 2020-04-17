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
            "label": _("Milk Entry"),
            "fieldname": "name",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("Member"),
            "options": "Supplier",
            "fieldname": "member",
            "fieldtype": "Link",
            "width": 100
        },
        {
            "label": _("DCS"),
            "options": "Warehouse",
            "fieldname": "dcs_id",
            "fieldtype": "Link",
            "width": 160
        },
        {
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 80
        },
        {
            "label": _("Time"),
            "fieldname": "time",
            "fieldtype": "Time",
            "width": 80
        },
        {
            "label": _("Shift"),
            "fieldname": "shift",
            "fieldtype": "Select",
            "width": 80
        },
        {
            "label": _("Milk Type"),
            "fieldname": "milk_type",
            "fieldtype": "Select",
            "width": 80
        },
        {
            "label": _("Volume"),
            "fieldname": "volume",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("FAT"),
            "fieldname": "fat",
            "fieldtype": "Float",
            "width": 60
        },
        {
            "label": _("CLR"),
            "fieldname": "clr",
            "fieldtype": "Float",
            "width": 60
        },
        {
            "label": _("Milk Rate"),
            "options":"Milk Rate",
            "fieldname": "milk_rate",
            "fieldtype": "Link",
            "width": 100
        },
        {
            "label": _("Unit Price"),
            "fieldname": "unit_price",
            "fieldtype": "Float",
            "width": 80
        },
        {
            "label": _("Total"),
            "fieldname": "total",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Created By"),
            "options": "User",
            "fieldname": "owner",
            "fieldtype": "Link",
            "width": 130
        },
        {
            "label": _("Create Date"),
            "fieldname": "creation",
            "fieldtype": "Datetime",
            "width": 160
        },
        {
            "label": _("Sample Collected"),
            "options":"Raw Milk Sample",
            "fieldname": "sample",
            "fieldtype": "Link",
            "width": 100
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Select",
            "width": 80
        },
        {
            "label": _("Stock Voucher"),
            "options":"Purchase Receipt",
            "fieldname": "purchase_receipt",
            "fieldtype": "Link",
            "width": 100
        }
    ]
    return columns

def get_data(filters):
    # print("======")
    conditions = get_conditions(filters)

    query = """ select tm.name,tm.member,tm.dcs_id,tm.date,tm.time,tm.shift,tm.milk_type,tm.volume,tm.fat,tm.clr,tm.milk_rate,tm.unit_price,tm.total, 
                tm.owner,tm.creation,tm.sample,tm.status,tp.name,tm.company from  `tabMilk Entry` tm inner join `tabPurchase Receipt` tp where tp.milk_entry = tm.name """

    print("====query",query+conditions)
    q_data = frappe.db.sql(query+conditions)
    data = []
    for q in q_data:
        row = {
            "name": q[0],
            "member": q[1],
            "dcs_id": q[2],
            "date": q[3],
            "time": q[4],
            "shift": q[5],
            "milk_type": q[6],
            "volume": q[7],
            "fat": q[8],
            "clr": q[9],
            "milk_rate":q[10],
            "unit_price":q[11],
            "total": q[12],
            "owner":q[13],
            "creation":q[14],
            "sample": q[15],
            "status": q[16],
            "purchase_receipt":q[17]
        }
        data.append(row)

    return data


def get_conditions(filters):

    if filters:
        query = """   and  date >= '{0}' and  date <= '{1}'  """.format(filters.from_date,filters.to_date)
        if filters.get('company'):
            query += """ and  tm.company = '%s'  """%filters.company
        if filters.get('dcs'):
            query += """ and  dcs_id = '%s'  """%filters.dcs
        if filters.get('member'):
            query += """ and  member = '%s'  """%filters.member
        if filters.get('pricelist'):
            query += """ and  milk_rate = '%s'  """%filters.pricelist
        if filters.get('shift') != 'All':
            query += """ and  shift = '%s' """%filters.shift
        if filters.get('milk_type') != 'All':
            query += """ and  milk_type = '%s' """%filters.milk_type

    return query