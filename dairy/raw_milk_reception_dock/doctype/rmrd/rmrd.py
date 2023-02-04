# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RMRD(Document):
	def validate(self):
		result = frappe.db.sql("select * from `tabRMRD` where route =%s and date =%s and shift =%s",(self.route,self.date,self.shift))
		if result and self.get('__islocal'):
			frappe.throw("you can not create duplicate entry with same DCS,Date and Shift.")

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
		self.hide_start_rmrd_button = 1
		self.db_update()

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

	def on_submit(self):
		self.make_stock_entry()
		self.create_materail_receipt()

	def make_stock_entry(self):
		if self.t_g_cow_wt > 0 or self.t_g_buf_wt > 0 or self.t_g_mix_wt > 0:
			stock_entry = frappe.new_doc("Stock Entry")
			stock_entry.purpose = "Material Transfer"
			stock_entry.stock_entry_type = "Material Transfer"
			stock_entry.company = self.company
			stock_entry.rmrd = self.name

			route = frappe.get_doc("Route Master", self.route)

			cost_center = frappe.get_cached_value('Company', self.company, 'cost_center')
			perpetual_inventory = frappe.get_cached_value('Company', self.company, 'enable_perpetual_inventory')
			expense_account = frappe.get_cached_value('Company', self.company, 'stock_adjustment_account')

			g_cow_item = frappe.db.get_single_value("Dairy Settings", "cow_pro")
			g_buf_item = frappe.db.get_single_value("Dairy Settings", "buf_pro")
			g_mix_item = frappe.db.get_single_value("Dairy Settings", "mix_pro")

			if self.t_g_cow_wt > 0:
				self.set_value_depend_milk_type(g_cow_item, stock_entry, self.t_g_cow_wt, self.t_cow_m_fat,
												self.t_cow_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

			if self.t_g_buf_wt > 0:
				self.set_value_depend_milk_type(g_buf_item, stock_entry, self.t_g_buf_wt, self.t_buf_m_fat,
												self.t_buf_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

			if self.t_g_mix_wt > 0:
				self.set_value_depend_milk_type(g_mix_item, stock_entry, self.t_g_mix_wt, self.t_mix_m_fat,
												self.t_mix_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

			stock_entry.insert()
			if not self.inspection_required:
				stock_entry.submit()


	def create_materail_receipt(self):
		if self.t_s_cow_wt > 0 or self.t_s_buf_wt > 0 or self.t_s_mix_wt > 0 or self.t_c_cow_wt > 0 or self.t_c_buf_wt > 0 or self.t_c_mix_wt > 0:
			stock_entry = frappe.new_doc("Stock Entry")
			stock_entry.purpose = "Material Receipt"
			stock_entry.stock_entry_type = "Material Receipt"
			stock_entry.company = self.company
			stock_entry.rmrd = self.name

			route = frappe.get_doc("Route Master", self.route)

			cost_center = frappe.get_cached_value('Company', self.company, 'cost_center')
			perpetual_inventory = frappe.get_cached_value('Company', self.company, 'enable_perpetual_inventory')
			expense_account = frappe.get_cached_value('Company', self.company, 'stock_adjustment_account')

			s_cow_item = frappe.db.get_single_value("Dairy Settings", "s_cow_milk")
			s_buf_item = frappe.db.get_single_value("Dairy Settings", "s_buf_milk")
			s_mix_item = frappe.db.get_single_value("Dairy Settings", "s_mix_milk")

			c_cow_item = frappe.db.get_single_value("Dairy Settings", "c_cow_milk")
			c_buf_item = frappe.db.get_single_value("Dairy Settings", "c_buf_milk")
			c_mix_item = frappe.db.get_single_value("Dairy Settings", "c_buf_milk")

			if self.t_s_cow_wt > 0:
				self.set_value_depend_milk_type(s_cow_item, stock_entry, self.t_s_cow_wt, self.t_cow_m_fat,
												self.t_cow_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

			if self.t_s_buf_wt > 0:
				self.set_value_depend_milk_type(s_buf_item, stock_entry, self.t_s_buf_wt, self.t_buf_m_fat,
												self.t_buf_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

			if self.t_s_mix_wt > 0:
				self.set_value_depend_milk_type(s_mix_item, stock_entry, self.t_s_mix_wt, self.t_mix_m_fat,
												self.t_mix_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

			if self.t_c_cow_wt > 0:
				self.set_value_depend_milk_type(c_cow_item, stock_entry, self.t_c_cow_wt, self.t_cow_m_fat,
												self.t_cow_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

			if self.t_c_buf_wt > 0:
				self.set_value_depend_milk_type(c_buf_item, stock_entry, self.t_c_buf_wt, self.t_buf_m_fat,
												self.t_buf_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

			if self.t_c_mix_wt > 0:
				self.set_value_depend_milk_type(c_mix_item, stock_entry, self.t_c_mix_wt, self.t_mix_m_fat,
												self.t_mix_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

			stock_entry.insert()
			if not self.inspection_required:
				stock_entry.submit()

	def set_value_depend_milk_type(self, item_name, stock_entry, milk_collected, fat, clr, route, target_warehouse, cost_center, expense_account, perpetual_inventory=None):
		item = frappe.get_doc("Item", item_name)
		se_child = stock_entry.append('items')
		se_child.item_code = item.item_code
		se_child.item_name = item.item_name
		se_child.uom = item.stock_uom
		se_child.stock_uom = item.stock_uom
		se_child.qty = milk_collected
		se_child.fat = (milk_collected * fat) / 100
		se_child.clr = clr / 4 + 0.21 * (fat / 100) + 0.36
		if stock_entry.purpose == "Material Transfer":
			se_child.s_warehouse = route.dest_warehouse
		se_child.t_warehouse = target_warehouse
		# in stock uom
		se_child.transfer_qty = milk_collected
		se_child.cost_center = cost_center
		se_child.expense_account = expense_account if perpetual_inventory else None