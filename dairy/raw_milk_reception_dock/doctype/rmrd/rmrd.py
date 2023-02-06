# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RMRD(Document):
	def validate(self):
		result = frappe.db.sql("""select * from `tabRMRD` where route =%s and date =%s and shift =%s and docstatus = 1""",(self.route,self.date,self.shift))
		# if result and self.get('__islocal'):
		if result:
			frappe.throw("you can not create duplicate entry with same DCS,Date and Shift.")

	@frappe.whitelist()
	def submit_rmrd(self):
		self.db_set('status','Submitted')

	@frappe.whitelist()
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

		print('result1*^^^^^^^^^^^^^^^^^^^',result1)						
		if not result1:
			frappe.throw("Collection Not found!")

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
				if res.get('milk_type') == 'Buffalo':
					doc.buf_milk_sam = res.get('sam_count')
				if res.get('milk_type') == 'Mix':
					doc.mix_milk_sam = res.get('sam_count')
			doc.insert(ignore_permissions=True)
			doc.calculate_total_cans_wt()
		self.db_set('status', 'In-Progress')
		self.flags.ignore_validate_update_after_submit = True  # ignore after submit permission
		self.save(ignore_permissions=True)
		# self.hide_start_rmrd_button = 1
		return True
		# self.db_update()

	def before_submit(self):
		result = frappe.db.sql("""select sum(g_cow_milk) as g_cow,
								sum(g_buf_milk) as g_buf,
								sum(g_mix_milk) as g_mix, 
								sum(g_cow_milk_can) as g_cow_can, 
								sum(g_buf_milk_can) as g_buf_can, 
								sum(g_mix_milk_can) as g_mix_can,
								
								sum(s_cow_milk) as s_cow,
								sum(s_buf_milk) as s_buf,
								sum(s_mix_milk) as s_mix,
								sum(s_cow_milk_can) as s_cow_can,
								sum(s_buf_milk_can) as s_buf_can,
								sum(s_mix_milk_can) as s_mix_can,
								
								sum(c_cow_milk) as c_cow,
								sum(c_buf_milk) as c_buf,
								sum(c_mix_milk) as c_mix,
								sum(c_cow_milk_can) as c_cow_can,
								sum(c_buf_milk_can) as c_buf_can,
								sum(c_mix_milk_can) as c_mix_can,
								
								sum(cow_milk_sam) as cow_milk_sam,
								sum(buf_milk_sam) as buf_milk_sam,
								sum(mix_milk_sam) as mix_milk_sam,
								
								sum(cow_milk_fat) as cow_milk_fat,
								sum(buf_milk_fat) as buf_milk_fat,
								sum(mix_milk_fat) as mix_milk_fat,
								
								sum(cow_milk_clr) as cow_milk_clr,
								sum(buf_milk_clr) as buf_milk_clr,
								sum(mix_milk_clr) as mix_milk_clr,
								rmrd
								from `tabRMRD Lines` where rmrd =%s
								group by rmrd""",(self.name), as_dict=True)

		print('result*******************',result)
		for res in result:
			self.t_g_cow_wt = res.get('g_cow')
			self.t_g_buf_wt = res.get('g_buf')
			self.t_g_mix_wt = res.get('g_mix')

			self.t_g_cow_can = res.get('g_cow_can')
			self.t_g_buf_can = res.get('g_buf_can')
			self.t_g_mix_can = res.get('g_mix_can')

			self.t_s_cow_wt = res.get('s_cow')
			self.t_s_buf_wt = res.get('s_buf')
			self.t_s_mix_wt = res.get('s_mix')

			self.t_s_cow_can = res.get('s_cow_can')
			self.t_s_buf_can = res.get('s_buf_can')
			self.t_s_mix_can = res.get('s_mix_can')

			self.t_c_cow_wt = res.get('c_cow')
			self.t_c_buf_wt = res.get('c_buf')
			self.t_c_mix_wt = res.get('c_mix')

			self.t_c_cow_can = res.get('c_cow_can')
			self.t_c_buf_can = res.get('c_buf_can')
			self.t_c_mix_can = res.get('c_mix_can')

			self.t_cow_sam = res.get('cow_milk_sam')
			self.t_buf_sam = res.get('buf_milk_sam')
			self.t_mix_sam = res.get('mix_milk_sam')

			self.t_cow_m_fat = res.get('cow_milk_fat')
			self.t_buf_m_fat = res.get('buf_milk_fat')
			self.t_mix_m_fat = res.get('mix_milk_fat')

			self.t_cow_m_clr = res.get('cow_milk_clr')
			self.t_buf_m_clr = res.get('buf_milk_clr')
			self.t_mix_m_clr = res.get('mix_milk_clr')
			self.db_update()

		line_ids = frappe.db.sql("""select name from `tabRMRD Lines` where rmrd =%s""", (self.name), as_dict =True)
		for res in line_ids:
			doc =frappe.get_doc("RMRD Lines",res.get("name"))
			if doc:
				doc.submit()	