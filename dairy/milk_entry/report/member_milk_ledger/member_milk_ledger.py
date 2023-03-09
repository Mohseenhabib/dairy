# Copyright (c) 2023, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _

TRANSLATIONS = frappe._dict()

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters, columns)
	update_total()
	return columns, data



def get_columns():
	columns = [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Datetime", "width": 150},
		{"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 150},
		{"label": _("Ltr"), "fieldname": "litre", "fieldtype": "Float", "width": 150},
		{"label": _("Fat"), "fieldname": "fat", "fieldtype": "Percent", "width": 150},
		{"label": _("SNF"), "fieldname": "snf", "fieldtype": "Percent", "width": 150},
		{"label": _("Rate"), "fieldname": "unit_price", "fieldtype": "Currency", "width": 150},
		{"label": _("Amount"), "fieldname": "total", "fieldtype": "Currency", "width": 150},
	]

	return columns

def get_data(filters, columns):
	data =[]
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')
	member = filters.get('member')
	
	
	result = frappe.db.sql("""select date,shift,litre,fat, snf,unit_price,total
                                    from `tabMilk Entry` 
                                    where member = '{0}' and date between '{1}' and '{2}'
                                    """.format(member,from_date,to_date ), as_dict=True)

	print(result)
	data = result
	return data


def update_total():
	TRANSLATIONS.update(
		dict( TOTAL=_("Total"))
	)


def get_totals_dict():
	def add_total(label):
		return _dict(
			date = "'{0}'".format(label),
			litre = 0.0,
			fat = 0,
			snf = 0,
			rate = 0,
			amount= 0,
		)

	return _dict(
		total = add_total(TRANSLATIONS.TOTAL),
	)