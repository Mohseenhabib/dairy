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
            "label": _("Name"),
            "fieldname": "name",
            "fieldtype": "Data",
            "width": 120
        },
		{
            "label": _("DCS"),
            "options": "Warehouse",
            "fieldname": "dcs_id",
            "fieldtype": "Link",
            "width": 160
        },
#         {
#             "label": _("Cow Milk Volume"),
#             "fieldname": "cow_milk_vol",
#             "fieldtype": "Float",
#             "width": 100
#         },
#         {
#             "label": _("Buffalow Milk Volume"),
#             "fieldname": "buf_milk_vol",
#             "fieldtype": "Float",
#             "width": 100            
#         },
# 		{
#             "label": _("Mix Milk Volume"),
#             "fieldname": "mix_milk_vol",
#             "fieldtype": "Float",
#             "width": 100
#         },
		
		
		{
            "label": _("Cow Milk Cans"),
            "fieldname": "cow_milk_cans",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Buffalo Milk Cans"),
            "fieldname": "buf_milk_cans",
            "fieldtype": "Float",
            "width": 100
        },
		{
            "label": _("Mix Milk Cans"),
            "fieldname": "mix_milk_cans",
            "fieldtype": "Float",
            "width": 100
        },
		
		
		{
            "label": _("Cow Sample Number"),
            "fieldname": "cow_milk_sam",
            "fieldtype": "Link",
            "options" : "Raw Milk Sample",
            "width": 100
        },
        {
            "label": _("Buffalo Sample Number"),
            "fieldname": "buf_milk_sam",
            "fieldtype": "Link",
            "options" : "Raw Milk Sample",
            "width": 100
        },
		{
            "label": _("Mix Sample Number"),
            "fieldname": "mix_milk_sam",
            "fieldtype": "Link",
            "options" : "Raw Milk Sample",
            "width": 100
        },
		
		
#         {
#             "label": _("Gate Pass"),
#             "fieldname": "gate_pass",
#             "fieldtype": "Link",
#             ""
#             "width": 80
#         },
        {
            "label": _("Time"),
            "fieldname": "time",
            "fieldtype": "Time",
            "width": 80
        },
		{
            "label": _("Van Collection"),
            "fieldname": "van_col",
            "fieldtype": "Link",
            "options":"Van Collection",
            "width": 120
        }
        
    ]
    return columns

def get_data(filters):
    # print("======")
    conditions = get_conditions(filters)

    query = """ select name,dcs,cow_milk_vol,buf_milk_vol,mix_milk_vol,cow_milk_cans,buf_milk_cans,
    			mix_milk_cans,cow_milk_sam,buf_milk_sam,mix_milk_sam,time,parent from `tabVan Collection Items` """

    print("====query",query+conditions)
    q_data = frappe.db.sql(query+conditions)
    data = []
    for q in q_data:
        row = {
            "name": q[0],
            "dcs_id": q[1],
            "cow_milk_vol": q[2],
            "buf_milk_vol": q[3],
            "mix_milk_vol": q[4],
            "cow_milk_cans": q[5],
            "buf_milk_cans": q[6],
            "mix_milk_cans": q[7],
            "cow_milk_sam": q[8],
            "buf_milk_sam": q[9],
            "mix_milk_sam":q[10],
            "time":q[11],
            "van_col":q[12]
        }
        print("======row",row)
        data.append(row)
		
    return data


def get_conditions(filters):
	print("=====filters",filters)
	if filters:
		query = """      """
		if filters.get('parent'):
		    query += """ where  parent = '%s' """%filters.parent
# 		if filters.get('dcs'):
# 		    query += """ and  dcs_id = '%s'  """%filters.dcs
# 		if filters.get('member'):
# 		    query += """ and  member = '%s'  """%filters.member
# 		if filters.get('pricelist'):
# 		    query += """ and  milk_rate = '%s'  """%filters.pricelist
# 		if filters.get('shift') != 'All':
# 		    query += """ and  shift = '%s' """%filters.shift
# 		if filters.get('milk_type') != 'All':
# 		    query += """ and  milk_type = '%s' """%filters.milk_type
		
		return query
