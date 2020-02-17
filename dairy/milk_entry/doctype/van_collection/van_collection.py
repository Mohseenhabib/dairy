# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today


class VanCollection(Document):
	pass

	def submit_van_collection(self):
		frappe.db.set(self,'status','Submitted')
	
# 	def check_van_collections(self):
# 		van_colle = frappe.db.get_value("Van Collection",{"route": self.route,
# 							"date":today(),
# 							"shift":self.shift,
# 							"vehicle":self.vehicle,
# 							"status":["!=","Cancelled"]
# 							})
# 		
# 		if van_colle:
# 			frappe.throw(_("Already vehicle has been scheduled in this period."))


	def van_start_collection(self):
		print("==========self",self)
		van_col = frappe.get_doc('Van Collection',self.name)
		
		warehouse = frappe.db.get_all("Warehouse",{"route": van_col.route})
	# 	print("====warehouse",warehouse)
		if not warehouse:
			frappe.throw(_("No Warehouse present in this Route"))
		
		nameing_series = frappe.db.sql(""" select options from `tabDocField` where fieldname='naming_series' and parent='Van Collection Items' """)
	# 	print("====warehouse",warehouse,"====van_col",van_col)
		for ware in warehouse:
			row = van_col.append('collections', {
				'naming_series':nameing_series[0][0],
				'parent':van_col,
				'dcs':ware['name']
				})
			row.save()
		
		van_col.save()
		
		frappe.db.set(van_col, 'status', "In-Progress")

		return True
	