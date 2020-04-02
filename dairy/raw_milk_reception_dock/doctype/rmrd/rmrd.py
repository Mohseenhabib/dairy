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
	#
	# 	result2 = frappe.db.sql("""select count(*) as sam_count,milk_type from `tabMulti Row Milk Sample` where parent in
	# 										(select name from `tabVan Collection Items`
	# 										where route =%s and shift =%s and date =%s) group by milk_type""",
	# 							(self.route, self.shift, self.date), as_dict=True)
	# 	for res in result2:
	# 		if res.get('milk_type') == 'Cow':
	# 			self.total_cow_milk_sample = res.get('sam_count')
	# 		if res.get('milk_type') == 'Buffalow':
	# 			self.total_buf_milk_sample = res.get('sam_count')
	# 		if res.get('milk_type') == 'Mix':
	# 			self.total_mix_milk_sample = res.get('sam_count')
	#
	# 	result3 = frappe.db.sql("""select sum(cow_milk_collected) as cow_collected,
	# 									sum(buffalow_milk_collected) as buf_collected,
	# 									sum(mix_milk_collected) as mix_collected,
	# 									sum(cow_milk_cans) as cow_m_cans,
	# 									sum(buf_milk_cans) as buf_m_cans,
	# 									sum(mix_milk_cans) as mix_m_cans,
	# 									dcs
	# 									from `tabVan Collection Items`
	# 									where route =%s and shift =%s and date =%s and gate_pass is not null
	# 									group by dcs
	# 									""", (self.route, self.shift, self.date), as_dict=True)
	# 	for res in result3:
	# 		self.append("rmrd_lines", {
	# 			"g_cow_milk":res.get('cow_collected'),
	# 			"g_buf_milk":res.get('buf_collected'),
	# 			"g_mix_milk":res.get('mix_collected'),
	# 			"g_cow_milk_can":res.get('cow_m_cans'),
	# 			"g_buf_milk_can":res.get('buf_m_cans'),
	# 			"g_mix_milk_can":res.get('mix_m_cans'),
	# 			"dcs":res.get('dcs')
	# 		})
	# 	self.save(ignore_permissions=True)

	def start_rmrd(self):
		print("----------------------",self.route, self.shift, self.date)
		result3 = frappe.db.sql("""select sum(cow_milk_collected) as cow_collected,
								sum(buffalow_milk_collected) as buf_collected,
								sum(mix_milk_collected) as mix_collected,
								sum(cow_milk_cans) as cow_m_cans,
								sum(buf_milk_cans) as buf_m_cans,
								sum(mix_milk_cans) as mix_m_cans,
								dcs 
								from `tabVan Collection Items` 
								where route =%s and shift =%s and date =%s and gate_pass is not null
								group by dcs
								""", (self.route, self.shift, self.date), as_dict=True)
		print("------------result3",result3)
		for res in result3:
			print("-----------",res.get('cow_collected'),type(res.get('cow_collected')))
			doc = frappe.new_doc("RMRD Lines")
			doc.g_cow_milk = res.get('cow_collected')
			doc.g_buf_milk = res.get('buf_collected')
			doc.g_mix_milk = res.get('mix_collected')
			doc.g_cow_milk_can = res.get('cow_m_cans')
			doc.g_buf_milk_can = res.get('buf_m_cans')
			doc.g_mix_milk_can = res.get('mix_m_cans')
			doc.dcs = res.get('dcs')
			doc.rmrd = self.name
			print("---------------------doc.g_cow_milk",doc.g_cow_milk)
			doc.insert(ignore_permissions=True)


	# def before_save(self):
	# 	if not self.get('__islocal'):
	# 		cow_collected=0
	# 		buf_collected=0
	# 		mix_collected=0
	# 		cow_cans=0
	# 		buf_cans=0
	# 		mix_cans=0
	# 		for i in self.rmrd_lines:
	# 			cow_collected += i.cow_milk_collected
	# 			buf_collected += i.buffalow_milk_collected
	# 			mix_collected += i.mix_milk_collected
	# 			cow_cans += i.cow_milk_cans
	# 			buf_cans += i.buf_milk_cans
	# 			mix_cans += i.mix_milk_cans
	# 		self.total_cow_weight = cow_collected
	# 		self.total_buf_weight = buf_collected
	# 		self.total_mix_weight = mix_collected
	# 		self.total_cow_can = cow_cans
	# 		self.total_buf_can = buf_cans
	# 		self.total_mix_can = mix_cans