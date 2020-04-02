# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RawMilkSample(Document):
	def validate(self):
		if self.milk_entry:
			doc = frappe.get_doc("Milk Entry", self.milk_entry)
			res = frappe.db.sql("""select docstatus from `tabPurchase Receipt` where milk_entry =%s limit 1""",
								(doc.name))
			if res:
				if res[0][0] == 1 and doc.sample_created:
					doc.status = "To Sample"
				elif res[0][0] ==0 and not doc.sample_created:
					doc.status = "To Post"
				elif res[0][0] ==1 and not doc.sample_created:
					doc.status = "Posted"
				elif res[0][0] == 0 and doc.sample_created:
					doc.status = "To Post and Sample"
				else:
					doc.status = "To Post and Sample"
			else:
				doc.status = "To Post and Sample"
			doc.db_update()

	def on_submit(self):
		if self.milk_entry:
			doc = frappe.get_doc("Milk Entry", self.milk_entry)
			res = frappe.db.sql("""select docstatus from `tabPurchase Receipt` where milk_entry =%s limit 1""",
								(doc.name))
			if res:
				if res[0][0] == 0 and doc.sample_created:
					doc.status = "To Post"
				elif res[0][0] == 0 and not doc.sample_created:
					doc.status = "To Post"
				elif res[0][0] == 1 and not doc.sample_created:
					doc.status = "Posted"
				else:
					doc.status = "To Post"
			else:
				doc.status = "To Post"
			doc.db_update()



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



