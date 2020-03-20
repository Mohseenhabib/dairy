# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class CrateReconciliation(Document):
	def validate(self):
		if not self.get("__islocal"):
			self.calculate_total_count()

	def after_insert(self):
		self.calculate_total_count()

	def calculate_total_count(self):
		total_outgoing = 0.0
		total_incoming = 0.0
		total_damage = 0.0
		for i in self.delivery_info:
			if i.outgoing:
				total_outgoing += i.outgoing
			if i.incoming:
				total_incoming += i.incoming
			if i.damaged:
				total_damage += i.damaged
		self.total_outgoing =total_outgoing
		self.total_incoming =total_incoming
		self.total_damaged =total_damage
		self.difference = total_outgoing - total_incoming
		self.db_update()
		# self.save(ignore_permissions=True)


@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None, ignore_permissions=False):
	def set_item_in_sales_invoice(source, target):
		sale_inv = frappe.get_doc(target)

	doclist = get_mapped_doc("Delivery Note", source_name, {
		"Delivery Note": {
			"doctype": "Crate Reconciliation",
		}
	}, target_doc,set_item_in_sales_invoice)
	return doclist

