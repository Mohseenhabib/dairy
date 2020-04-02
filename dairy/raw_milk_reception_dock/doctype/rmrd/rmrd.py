# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RMRD(Document):
	# def get_van_collection(self):
	# 	to_remove = []
	# 	for s in self.get("rmrd_lines"):
	# 		to_remove.append(s)
	# 	for d in to_remove:
	# 		self.remove(d)
	# 	result1 = frappe.db.sql("""select sum(cow_milk_collected) as cow_collected,
	# 									sum(buffalow_milk_collected) as buf_collected,
	# 									sum(mix_milk_collected) as mix_collected,
	# 									sum(cow_milk_cans) as cow_m_cans,
	# 									sum(buf_milk_cans) as buf_m_cans,
	# 									sum(mix_milk_cans) as mix_m_cans,
	# 									from `tabVan Collection Items`
	# 									where route =%s and shift =%s and date =%s and gate_pass is not null
	# 									""", (self.route, self.shift, self.date), as_dict=True)
	# 	for res in result1:
	# 		self.total_cow_weight = res.get('cow_collected')
	# 		self.total_buf_weight = res.get('buf_collected')
	# 		self.total_mix_weight = res.get('mix_collected')
	# 		self.total_cow_can = res.get('cow_m_cans')
	# 		self.total_buf_can = res.get('buf_m_cans')
	# 		self.total_mix_can = res.get('mix_m_cans')
	# 	self.save(ignore_permissions=True)

	def start_rmrd(self):
		result1 = frappe.db.sql("""select sum(cow_milk_collected) as cow_collected,
								sum(buffalow_milk_collected) as buf_collected,
								sum(mix_milk_collected) as mix_collected,
								sum(cow_milk_cans) as cow_m_cans,
								sum(buf_milk_cans) as buf_m_cans,
								sum(mix_milk_cans) as mix_m_cans,
								sum(cow_milk_fat) as cow_milk_fat,
								sum(buf_milk_fat) as buf_milk_fat,
								sum(mix_milk_fat) as mix_milk_fat,
								sum(cow_milk_clr) as cow_milk_clr,
								sum(buf_milk_clr) as buf_milk_clr,
								sum(mix_milk_clr) as mix_milk_clr,
								dcs 
								from `tabVan Collection Items` 
								where route =%s and shift =%s and date =%s and gate_pass is not null
								group by dcs
								""", (self.route, self.shift, self.date), as_dict=True)
		for res in result1:
			doc = frappe.new_doc("RMRD Lines")
			doc.g_cow_milk = res.get('cow_collected')
			doc.g_buf_milk = res.get('buf_collected')
			doc.g_mix_milk = res.get('mix_collected')
			doc.g_cow_milk_can = res.get('cow_m_cans')
			doc.g_buf_milk_can = res.get('buf_m_cans')
			doc.g_mix_milk_can = res.get('mix_m_cans')

			doc.cow_milk_fat = res.get('cow_milk_fat')
			doc.buf_milk_fat = res.get('buf_milk_fat')
			doc.mix_milk_fat = res.get('mix_milk_fat')

			doc.cow_milk_clr = res.get('cow_milk_clr')
			doc.buf_milk_clr = res.get('buf_milk_clr')
			doc.mix_milk_clr = res.get('mix_milk_clr')

			doc.dcs = res.get('dcs')
			doc.rmrd = self.name

			result2 = frappe.db.sql("""select count(*) as sam_count,milk_type from `tabMulti Row Milk Sample` where parent in
									(select name from `tabVan Collection Items`
									where route =%s and shift =%s and date =%s and dcs =%s) group by milk_type""",
									(self.route, self.shift, self.date,res.get('dcs')), as_dict=True)
			for res in result2:
				if res.get('milk_type') == 'Cow':
					doc.cow_milk_sam = res.get('sam_count')
				if res.get('milk_type') == 'Buffalow':
					doc.buf_milk_sam = res.get('sam_count')
				if res.get('milk_type') == 'Mix':
					doc.mix_milk_sam = res.get('sam_count')
			doc.insert(ignore_permissions=True)
			doc.calculate_total_cans_wt()

