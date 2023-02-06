# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RMRDLines(Document):
	@frappe.whitelist()
	def calculate_total_cans_wt(self):
		g_cow_milk = self.g_cow_milk if self.g_cow_milk else 0
		g_buf_milk = self.g_buf_milk if self.g_buf_milk else 0
		g_mix_milk = self.g_mix_milk if self.g_mix_milk else 0
		g_total_m = g_cow_milk + g_buf_milk + g_mix_milk

		g_cow_milk_can = self.g_cow_milk_can if self.g_cow_milk_can else 0
		g_buf_milk_can = self.g_buf_milk_can if self.g_buf_milk_can else 0
		g_mix_milk_can = self.g_mix_milk_can if self.g_mix_milk_can else 0
		g_total_c = g_cow_milk_can + g_buf_milk_can + g_mix_milk_can

		s_cow_milk = self.s_cow_milk if self.s_cow_milk else 0
		s_buf_milk = self.s_buf_milk if self.s_buf_milk else 0
		s_mix_milk = self.s_mix_milk if self.s_mix_milk else 0
		s_total_m = s_cow_milk + s_buf_milk + s_mix_milk

		s_cow_milk_can = self.s_cow_milk_can if self.s_cow_milk_can else 0
		s_buf_milk_can = self.s_buf_milk_can if self.s_buf_milk_can else 0
		s_mix_milk_can = self.s_mix_milk_can if self.s_mix_milk_can else 0
		s_total_c = s_cow_milk_can + s_buf_milk_can + s_mix_milk_can

		c_cow_milk = self.c_cow_milk if self.c_cow_milk else 0
		c_buf_milk = self.c_buf_milk if self.c_buf_milk else 0
		c_mix_milk = self.c_mix_milk if self.c_mix_milk else 0
		c_total_m =c_cow_milk + c_buf_milk + c_mix_milk

		c_cow_milk_can = self.c_cow_milk_can if self.c_cow_milk_can else 0
		c_buf_milk_can = self.c_buf_milk_can if self.c_buf_milk_can else 0
		c_mix_milk_can = self.c_mix_milk_can if self.c_mix_milk_can else 0
		c_total_c = c_cow_milk_can + c_buf_milk_can + c_mix_milk_can

		self.total_milk_can = g_total_c - s_total_c - c_total_c
		self.total_milk_wt = g_total_m - s_total_m - c_total_m
		self.db_update()


	def on_submit(self):
		self.make_stock_entry()
		self.create_materail_receipt()

	@frappe.whitelist()
	def make_stock_entry(self):
		rmrd = frappe.get_doc("RMRD", self.rmrd)
		# if rmrd.t_g_cow_wt > 0 or rmrd.t_g_buf_wt > 0 or rmrd.t_g_mix_wt > 0:
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.purpose = "Material Transfer"
		stock_entry.stock_entry_type = "Material Transfer"
		stock_entry.company = rmrd.company
		stock_entry.rmrd = rmrd.name

		route = frappe.get_doc("Route Master", self.route)

		cost_center = frappe.get_cached_value('Company', rmrd.company, 'cost_center')
		perpetual_inventory = frappe.get_cached_value('Company', rmrd.company, 'enable_perpetual_inventory')
		expense_account = frappe.get_cached_value('Company', rmrd.company, 'stock_adjustment_account')

		g_cow_item = frappe.db.get_single_value("Dairy Settings", "cow_pro")
		g_buf_item = frappe.db.get_single_value("Dairy Settings", "buf_pro")
		g_mix_item = frappe.db.get_single_value("Dairy Settings", "mix_pro")

		# if rmrd.t_g_cow_wt > 0:
		# 	rmrd.set_value_depend_milk_type(g_cow_item, stock_entry, self.t_g_cow_wt, self.cow_milk_fat,
		# 									rmrd.t_cow_m_clr, route, rmrd.target_warehouse, cost_center, expense_account, perpetual_inventory)

		# if self.t_g_buf_wt > 0:
		# 	self.set_value_depend_milk_type(g_buf_item, stock_entry, self.t_g_buf_wt, self.t_buf_m_fat,
		# 									self.t_buf_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

		# if self.t_g_mix_wt > 0:
		# 	self.set_value_depend_milk_type(g_mix_item, stock_entry, self.t_g_mix_wt, self.t_mix_m_fat,
		# 									self.t_mix_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

		stock_entry.insert()
		if not self.inspection_required:
			stock_entry.submit()

		return stock_entry

	def create_materail_receipt(self):
		rmrd = frappe.get_doc("RMRD", self.rmrd)
		# if rmrd.t_s_cow_wt > 0 or rmrd.t_s_buf_wt > 0 or rmrd.t_s_mix_wt > 0 or rmrd.t_c_cow_wt > 0 or rmrd.t_c_buf_wt > 0 or rmrd.t_c_mix_wt > 0:
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

		# if self.t_s_cow_wt > 0:
		# 	self.set_value_depend_milk_type(s_cow_item, stock_entry, self.t_s_cow_wt, self.t_cow_m_fat,
		# 									self.t_cow_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

		# if self.t_s_buf_wt > 0:
		# 	self.set_value_depend_milk_type(s_buf_item, stock_entry, self.t_s_buf_wt, self.t_buf_m_fat,
		# 									self.t_buf_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

		# if self.t_s_mix_wt > 0:
		# 	self.set_value_depend_milk_type(s_mix_item, stock_entry, self.t_s_mix_wt, self.t_mix_m_fat,
		# 									self.t_mix_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

		# if self.t_c_cow_wt > 0:
		# 	self.set_value_depend_milk_type(c_cow_item, stock_entry, self.t_c_cow_wt, self.t_cow_m_fat,
		# 									self.t_cow_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

		# if self.t_c_buf_wt > 0:
		# 	self.set_value_depend_milk_type(c_buf_item, stock_entry, self.t_c_buf_wt, self.t_buf_m_fat,
		# 									self.t_buf_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

		# if self.t_c_mix_wt > 0:
		# 	self.set_value_depend_milk_type(c_mix_item, stock_entry, self.t_c_mix_wt, self.t_mix_m_fat,
		# 									self.t_mix_m_clr, route, self.target_warehouse, cost_center, expense_account, perpetual_inventory)

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