# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
class BulkGatePassCreationTool(Document):
	def create_delivery_note(self):

		lst = []
		for itm in self.items:
			lst.append(itm.shift + "," + itm.transporter)
		for customer in set(lst):
			doc = frappe.new_doc("Gate Pass")
			doc.naming_series = self.naming_series
			doc.total_qty = 0
			doc.total_free_qty = 0
			doc.date = self.date
			doc.transporter = self.transporter
			doc.shift = self.shift
			doc.route = self.route
			total_supp_qty = 0
			total_free_qty = 0
			for itm in self.items:
				if customer == (itm.shift + "," + itm.transporter):
					doc.append('item', {
								'item_code': itm.item_code,
								'item_name': itm.item_name,
								'batch_no': itm.batch_no,
								'qty': itm.qty,
								'uom': itm.uom,
								'out_crate': itm.out_crate,
								'free_qty': itm.free_qty,
								'in_crate': itm.in_crate,
								'warehouse': itm.warehouse,
								'delivery_note': itm.delivery_note,
								'is_free_item': itm.is_free_item
							})
			doc.save(ignore_permissions=True)


@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None, skip_item_mapping=False):
	def update_item(source, target, source_parent):
		if source_parent.route:
			target.update({'route': source_parent.route})
		if source_parent.shift:
			target.update({'shift': source_parent.shift})
		if source_parent.customer:
			target.update({'customer': source_parent.customer})
		if source_parent.posting_date:
			target.update({'date': source_parent.posting_date})
		if source_parent.transporter:
			target.update({'transporter': source_parent.transporter})

	doclist = get_mapped_doc("Delivery Note", source_name, {
		"Delivery Note": {
			"doctype": "Bulk Gate Pass Creation Tool",
			"validation": {
				"docstatus": ["=", 1]
				# "material_request_type": ["=", "Purchase"]
			}
		},
		"Delivery Note Item": {
			"doctype": "Bulk Gate Pass Item",
			"field_map": [
				["stock_qty", 'qty'],
				["item_code", "item_code"],
				["stock_uom", "uom"],
				["delivery_note_item", "name"],
				["is_free_item", "is_free_item"]
			],
			"postprocess": update_item,
		}
	}, target_doc)

	return doclist
