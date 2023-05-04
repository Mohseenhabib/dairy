# Copyright (c) 2023, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

import calendar
import frappe
from frappe import _, _dict

TRANSLATIONS = frappe._dict()

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters, columns)
	# chart = get_chart_data(data,filters)
	update_total()

	return columns, data 


def update_translations():
	TRANSLATIONS.update(
		dict(OPENING=_("Opening"), TOTAL=_("Total"), CLOSING_TOTAL=_("Closing (Opening + Total)"))
	)



def get_columns(filters):
	columns = [
			{"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 150},
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
			{"label": _("SNF Deduction"), "fieldname": "snf_deduction", "fieldtype": "Currency", "width": 150},
			{"label": _("FAT Deduction"), "fieldname": "fat_deduction", "fieldtype": "Currency", "width": 150},
			{"label": _("Incentive"), "fieldname": "incentive", "fieldtype": "Currency", "width": 150},
			{"label": _("Purchase Invoice"), "fieldname": "parent", "fieldtype": "Link","options":"Purchase Invoice", "width": 150},
			{"label": _("Purchase Invoice status"), "fieldname": "status", "fieldtype": "Link","options":"Purchase Invoice", "width": 150},
			# {"label": _("SNF Deduction"), "fieldname": "snf_deduction", "fieldtype": "Currency", "width": 150},
	]
	return columns


def get_data(filters, columns):
	# doc = frappe.get_all('Warehouse',{'is_dcs':1},['name'])
	# print('doc------------------((((((((((((((((((((((((((((((((',doc)
	# if filters.get('dcs') in doc:
	# 	dcs = "{0}_name".format(frappe.scrub(filters.get("dcs")))
	# 	print('dcs-------------------------------------',dcs)
	conditions = get_conditions(filters)
	group_by = get_group_by(filters)
	print('group by-----------------!!!!!!!!!!!!!!!!!!',group_by)
	data =[]
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')
	result=[]
	if not filters.get('group_by'):
		print('kkkkkkkkkkkkkkkkkkkkkkkkkkkk')
		result = frappe.db.sql("""select pi.parent,
									p.status,
									me.name,
									me.date,
									me.shift,
									me.member,
									me.dcs_id,
									sum(me.volume) as volume,
									sum(me.fat) as fat,
									sum(me.fat_kg) as fat_kg,
									sum(me.snf) as snf,
									sum(me.snf_kg) as snf_kg,
									sum(me.clr) as clr,
									sum(me.clr_kg) as clr_kg,
									sum(me.litre) as litre,
									sum(me.unit_price) as unit_price,
									sum(me.total) as total,
									sum(me.snf_deduction) as snf_deduction,
									sum(me.fat_deduction) as fat_deduction,
									sum(me.incentive) as incentive
									from `tabMilk Entry` as me 
									join `tabPurchase Receipt` as pr on pr.milk_entry = me.name 
									join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
									join `tabPurchase Invoice` as p on p.name = pi.parent 
									{conditions} group by date , me.member
									order by me.date asc 
									""".format(conditions=conditions,group_by = group_by), as_dict=True)
		
	if filters.get('group_by') == 'Date':
		result = frappe.db.sql("""select pi.parent,
										p.status,
										me.name,
										me.date,
										me.shift,
										me.member,
										me.dcs_id,
										sum(me.volume) as volume,
										sum(me.fat) as fat,
										sum(me.fat_kg) as fat_kg,
										sum(me.snf) as snf,
										sum(me.snf_kg) as snf_kg,
										sum(me.clr) as clr,
										sum(me.clr_kg) as clr_kg,
										sum(me.litre) as litre,
										sum(me.unit_price) as unit_price,
										sum(me.total) as total,
										sum(me.snf_deduction) as snf_deduction,
										sum(me.fat_deduction) as fat_deduction,
										sum(me.incentive) as incentive
										from `tabMilk Entry` as me 
										join `tabPurchase Receipt` as pr on pr.milk_entry = me.name 
										join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
										join `tabPurchase Invoice` as p on p.name = pi.parent 
										{conditions} {group_by} , me.member
										order by me.date asc 
										""".format(conditions=conditions,group_by = group_by), as_dict=True)

	if filters.get('group_by')=='Member':
		result = frappe.db.sql("""select pi.parent,
										p.status,
										me.name,
										me.date,
										me.shift,
										me.member,
										me.dcs_id,
										sum(me.volume) as volume,
										sum(me.fat) as fat,
										sum(me.fat_kg) as fat_kg,
										sum(me.snf) as snf,
										sum(me.snf_kg) as snf_kg,
										sum(me.clr) as clr,
										sum(me.clr_kg) as clr_kg,
										sum(me.litre) as litre,
										sum(me.unit_price) as unit_price,
										sum(me.total) as total,
										sum(me.snf_deduction) as snf_deduction,
										sum(me.fat_deduction) as fat_deduction,
										sum(me.incentive) as incentive
										from `tabMilk Entry` as me 
										join `tabPurchase Receipt` as pr on pr.milk_entry = me.name 
										join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
										join `tabPurchase Invoice` as p on p.name = pi.parent 
										{conditions} group by date , me.member
										order by me.date asc 
										""".format(conditions=conditions,group_by = group_by), as_dict=True)


	if filters.get('group_by')=='DCS':
		result = frappe.db.sql("""select pi.parent,
									p.status,
									me.name,
									me.date,
									me.shift,
									me.member,
									me.dcs_id,
									sum(me.volume) as volume,
									sum(me.fat) as fat,
									sum(me.fat_kg) as fat_kg,
									sum(me.snf) as snf,
									sum(me.snf_kg) as snf_kg,
									sum(me.clr) as clr,
									sum(me.clr_kg) as clr_kg,
									sum(me.litre) as litre,
									sum(me.unit_price) as unit_price,
									sum(me.total) as total,
									sum(me.snf_deduction) as snf_deduction,
									sum(me.fat_deduction) as fat_deduction,
									sum(me.incentive) as incentive
									from `tabMilk Entry` as me 
									join `tabPurchase Receipt` as pr on pr.milk_entry = me.name 
									join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
									join `tabPurchase Invoice` as p on p.name = pi.parent 
									{conditions} group by date, me.member
									order by me.date asc 
									""".format(conditions=conditions,group_by = group_by), as_dict=True)

	if filters.get('shift'):
		result = frappe.db.sql("""select pi.parent,
									p.status,
									me.name,
									me.date,
									me.shift,
									me.member,
									me.dcs_id,
									sum(me.volume) as volume,
									sum(me.fat) as fat,
									sum(me.fat_kg) as fat_kg,
									sum(me.snf) as snf,
									sum(me.snf_kg) as snf_kg,
									sum(me.clr) as clr,
									sum(me.clr_kg) as clr_kg,
									sum(me.litre) as litre,
									sum(me.unit_price) as unit_price,
									sum(me.total) as total,
									sum(me.snf_deduction) as snf_deduction,
									sum(me.fat_deduction) as fat_deduction,
									sum(me.incentive) as incentive
									from `tabMilk Entry` as me 
									join `tabPurchase Receipt` as pr on pr.milk_entry = me.name 
									join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
									join `tabPurchase Invoice` as p on p.name = pi.parent 
									{conditions} group by date , me.member
									order by me.date asc 
									""".format(conditions=conditions,group_by = group_by), as_dict=True)

	# if filters.get('group_by')=='Shift':
	# 	result = frappe.db.sql("""select pi.parent,
	# 									p.status,
	# 									me.name,
	# 									me.date,
	# 									me.shift,
	# 									me.member,
	# 									me.dcs_id,
	# 									sum(me.volume) as volume,
	# 									sum(me.fat) as fat,
	# 									sum(me.fat_kg) as fat_kg,
	# 									sum(me.snf) as snf,
	# 									sum(me.snf_kg) as snf_kg,
	# 									sum(me.clr) as clr,
	# 									sum(me.clr_kg) as clr_kg,
	# 									sum(me.litre) as litre,
	# 									sum(me.unit_price) as unit_price,
	# 									sum(me.total) as total,
	# 									sum(me.snf_deduction) as snf_deduction,
	# 									sum(me.fat_deduction) as fat_deduction,
	# 									sum(me.incentive) as incentive
	# 									from `tabMilk Entry` as me 
	# 									join `tabPurchase Receipt` as pr on pr.milk_entry = me.name 
	# 									join `tabPurchase Invoice Item` as pi on pi.purchase_receipt = pr.name
	# 									join `tabPurchase Invoice` as p on p.name = pi.parent 
	# 									{conditions} group by date, me.shift ,me.member
	# 									order by me.date asc 
	# 									""".format(conditions=conditions,group_by = group_by), as_dict=True)

	
	return result


def update_total():
	TRANSLATIONS.update(
		dict( TOTAL=_("Total"))
	)


def get_totals_dict():
	def add_total(label):
		return _dict(
			shift = "'{0}'".format(label),
			volume = 0.0,
			fat = 0,
			snf = 0,
			clr = 0,
			litre = 0.0,
			rate = 0,
			amount= 0,
			incentive = 0,
			fat_deduction = 0,
			snf_deduction = 0,
		)

	return _dict(
		opening= add_total(TRANSLATIONS.OPENING),
		total= add_total(TRANSLATIONS.TOTAL),
		closing= add_total(TRANSLATIONS.CLOSING_TOTAL),
	)

def get_group_by(filters):
	query = ""

	if filters.get('group_by') == 'DCS':
		query += """ group by me.dcs_id"""
	if filters.get('group_by') == 'Member':
		query += """ group by me.member"""
	if filters.get('group_by') == 'Shift':
		query += """ group by me.shift"""
	if filters.get('group_by') == 'Date':
		query += """ group by me.date"""
	print('query---------------@@@@@@@@@@@@@@@@@@@@@@@@@',query)
	return query

def get_conditions(filters):
	query=""
	
	if filters.get('from_date') and ('to_date'):
		query  += """  where me.date between '{0}' and '{1}' """.format(filters.get('from_date'),filters.get('to_date'))
	if filters.get('dcs'):
		query += """ and  dcs_id = '%s'  """%filters.dcs
	if filters.get('member'):
		query += """ and  me.member = '%s'  """%filters.member
	if filters.get('shift'):
		query += """ and  me.shift = '%s'  """%filters.shift
	if filters.get('date'):
		query += """ and  me.date = '%s'  """%filters.date
	print('conditions-----------***********************',query)
	return query