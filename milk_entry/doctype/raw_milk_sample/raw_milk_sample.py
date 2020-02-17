# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class RawMilkSample(Document):
	pass
	


class Samplelines(Document):
	pass


	# def get_milk_entry_data(self):
	# 	print("====get_milk_entry_data")
	# 	if self.milk_entry:
	# 		milk_entry = frappe.model.get_doc("Milk Entry",self.milk_entry);
	# 		print("===milk_entry",milk_entry)
	# 		frappe.db.set(self, 'dcs_id',milk_entry.dcs_id)
	# 		frappe.db.set(self, 'milk_type',milk_entry.milk_type)
	# 		frappe.db.set(self, 'fat',milk_entry.fat)
	# 		frappe.db.set(self, 'clr',milk_entry.clr)



