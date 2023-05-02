# Copyright (c) 2023, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

import calendar
import frappe
from frappe import _, _dict

TRANSLATIONS = frappe._dict()

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters, columns)
	# chart = get_chart_data(data,filters)
	update_total()

	return columns, data 



def get_columns():
	columns = [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Datetime", "width": 150},
		{"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 150},
		{"label": _("Member"), "fieldname": "member", "fieldtype": "Data", "width": 150},
		# {"label": _("Name"), "fieldname": "name", "fieldtype": "Link","options":"Milk Entry","width": 150},
		{"label": _("DCS"), "fieldname": "dcs_id", "fieldtype": "Data", "width": 150},
		{"label": _("Ltr"), "fieldname": "volume", "fieldtype": "Float", "width": 150},
		{"label": _("Fat%"), "fieldname": "fat", "fieldtype": "Percent", "width": 150},
		{"label": _("Fat(in kg)"), "fieldname": "fat_kg", "fieldtype": "Float", "width": 150},
		{"label": _("SNF%"), "fieldname": "snf", "fieldtype": "Percent", "width": 150},
		{"label": _("SNF(in kg)"), "fieldname": "snf_kg", "fieldtype": "Float", "width": 150},
		{"label": _("CLR%"), "fieldname": "clr", "fieldtype": "Percent", "width": 150},
		{"label": _("CLR(in kg)"), "fieldname": "clr_kg", "fieldtype": "Float", "width": 150},
		{"label": _("Weight(in kg)"), "fieldname": "litre", "fieldtype": "Float", "width": 150},
		{"label": _("Rate"), "fieldname": "unit_price", "fieldtype": "Currency", "width": 150},
		{"label": _("Amount"), "fieldname": "total", "fieldtype": "Currency", "width": 150},
		{"label": _("Purchase Invoice"), "fieldname": "parent", "fieldtype": "Link","options":"Purchase Invoice", "width": 150},
		# {"label": _("Fat Deduction"), "fieldname": "fat_deduction", "fieldtype": "Currency", "width": 150},
		# {"label": _("SNF Deduction"), "fieldname": "snf_deduction", "fieldtype": "Currency", "width": 150},
	]

	return columns

def group_wise_column(group_by):
	if group_by:
		if group_by == "dcs":
			return ["DCS:Link/Warehouse:120"]
		if group_by == "member":
			return ["Member:Link/Supplier:120"]
		if group_by == "shift":
			return ["Shift:Link/Milk Entry:120"]
	else:
		return []

def get_data(filters, columns):
	conditions = get_conditions(filters)
	data =[]
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')
	result=[]
	# doc = frappe.get_all('Purchase Invoice Item',['milk_entry'])
	# print('filterssssssssssssssssssssssssss',doc)
	if not filters.get('group_by'):
		print('kkkkkkkkkkkkkkkkkkkkkkkkkkkk')
		result = frappe.db.sql("""select pi.parent,me.name,me.date,me.shift,me.member,me.dcs_id,me.volume,me.fat,me.fat_kg, me.snf,me.snf_kg,me.clr,me.clr_kg,me.litre,me.unit_price,me.total
								from `tabMilk Entry` as me inner join `tabPurchase Receipt` as pr on pr.milk_entry = me.name join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
								where me.date between '{0}' and '{1}'
								""".format(from_date,to_date), as_dict=True)
		print('result--------------------$$$$$$$$$$$$$$$$$$$$$$$$$$$$',result)	



	if filters.get('group_by')=='Member':
		print('member###########################')
		result = frappe.db.sql("""select pi.parent,me.name,me.date,me.shift,me.member,me.dcs_id,me.volume,me.fat,me.fat_kg, me.snf,me.snf_kg,me.clr,me.clr_kg,me.litre,me.unit_price,me.total
								from `tabMilk Entry` as me inner join `tabPurchase Receipt` as pr on pr.milk_entry = me.name join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
								where me.date between '{0}' and '{1}' {conditions}
								""".format(from_date,to_date,conditions=conditions), as_dict=True)
		print('result--------------------$$$$$$$$$$$$$$$$$$$$$$$$$$$$',result)	
		
	if filters.get('group_by')=='DCS':
		result = frappe.db.sql("""select pi.parent,me.name,me.date,me.shift,me.member,me.dcs_id,me.volume,me.fat,me.fat_kg, me.snf,me.snf_kg,me.clr,me.clr_kg,me.litre,me.unit_price,me.total
								from `tabMilk Entry` as me inner join `tabPurchase Receipt` as pr on pr.milk_entry = me.name join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
								where me.date between '{0}' and '{1}' {conditions}
								""".format(from_date,to_date,conditions=conditions), as_dict=True)
	
	if filters.get('group_by')=='Shift':
		result = frappe.db.sql("""select pi.parent,me.name,me.date,me.shift,me.member,me.dcs_id,me.volume,me.fat,me.fat_kg, me.snf,me.snf_kg,me.clr,me.clr_kg,me.litre,me.unit_price,me.total
								from `tabMilk Entry` as me inner join `tabPurchase Receipt` as pr on pr.milk_entry = me.name join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
								where me.date between '{0}' and '{1}' {conditions}
								""".format(from_date,to_date,conditions=conditions), as_dict=True)
	
	if filters.get('group_by')=='Date':
		result = frappe.db.sql("""select pi.parent,me.name,me.date,me.shift,me.member,me.dcs_id,sum(me.volume) as volume,sum(me.fat) as fat,
								sum(me.fat_kg) as fat_kg, sum(me.snf) as snf,sum(me.snf_kg) as snf_kg,
								sum(me.clr) as clr,sum(me.clr_kg) as clr_kg,sum(me.litre) as litre,
								sum(me.unit_price) as unit_price,sum(me.total) as total
								from `tabMilk Entry` as me inner join `tabPurchase Receipt` as pr on pr.milk_entry = me.name join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
								where me.date between '{0}' and '{1}' group by shift
								""".format(from_date,to_date,), as_dict=True)
	
	
	return result


def update_total():
	TRANSLATIONS.update(
		dict( TOTAL=_("Total"))
	)


def get_totals_dict():
	def add_total(label):
		return _dict(
			date = "'{0}'".format(label),
			volume = 0.0,
			fat = 0,
			snf = 0,
			clr = 0,
			litre = 0.0,
			rate = 0,
			amount= 0,
			# incentive = 0,
			# fat_deduction = 0,
			# snf_deduction = 0,
		)

	return _dict(
		total = add_total(TRANSLATIONS.TOTAL),
	)

def group_wise_column(group_by):
	print("=====group_by",group_by)
	if group_by:
		if group_by=="dcs":
			return [group_by + ":Link/Warehouse:120"]
		elif group_by=="member":
			return [group_by + ":Link/Supplier:120"]
		elif group_by=="shift":
			return [group_by + ":Link/Milk Entry:120"]
	else:
		return []
	

def get_conditions(filters):
	query=""
	
	if filters.get('dcs'):
		query += """ and  dcs_id = '%s'  """%filters.dcs
	if filters.get('member'):
		query += """ and  member = '%s'  """%filters.member
	if filters.get('shift'):
		query += """ and  shift = '%s'  """%filters.shift
	if filters.get('date'):
		query += """ and  date = '%s'  """%filters.date
	    
	return query