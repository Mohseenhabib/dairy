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
			lst.append(itm.route + "," + itm.shift + "," + itm.date +","+ itm.customer)
		for customer in set(lst):
			doc = frappe.new_doc("Gate Pass")
			doc.total_qty = 0
			doc.total_free_qty = 0
			doc.date = self.date
			doc.transporter = self.transporter
			doc.shift = self.shift
			doc.route = self.route
			total_supp_qty = 0
			total_free_qty = 0
			for itm in self.items:
				if customer == (itm.route + "," + itm.shift + "," + itm.date +","+ itm.customer):
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

	# def create_delivery_note(self):
	# 	lst = []
	# 	for itm in self.items:
	# 		lst.append(itm.delivery_note)
	# 	print("lst   ",lst)
	# 	for delivery_note in set(lst):
	# 		print("******* delivery Note ********",delivery_note)
	# 		doc = frappe.new_doc("Gate Pass")
	# 		doc.total_qty = 0
	# 		doc.total_free_qty = 0
	# 		doc.date = self.date
	# 		doc.transporter = self.transporter
	# 		doc.shift = self.shift
	# 		doc.route = self.route
	# 		total_supp_qty = 0
	# 		total_free_qty = 0
	# 		lst2 = []
	# 		for itm in self.items:
	# 			if itm.delivery_note == delivery_note:
	# 				lst2.append(itm.item_code)
	# 		for item in set(lst2):
	# 			print("items ***************88",item)
	# 			item_obj = frappe.get_doc("Item", item)
	# 			has_batch_no = item_obj.has_batch_no
	# 			if has_batch_no == 1:
	# 				lst3 = []
	# 				for itm in self.items:
	# 					if itm.delivery_note == delivery_note and itm.item_code == item:
	# 						lst3.append(itm.warehouse)
	# 				for warehouse in set(lst3):
	# 					print("warehouse ********",warehouse)
	# 					lst4 = []
	# 					for itm in self.items:
	# 						if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse:
	# 							lst4.append(itm.batch_no)
	# 					for batch_no in set(lst4):
	# 						free_qty = 0
	# 						total_qty = 0
	# 						for itm in self.items:
	# 							if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse and itm.batch_no == batch_no and itm.is_free_item == 1:
	# 								free_qty += itm.qty
	# 							if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse and itm.batch_no == batch_no and itm.is_free_item == 0:
	# 								total_qty += itm.qty
	# 							if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse and itm.batch_no == batch_no:
	# 								doc.append('merge_item', {
	# 											'item_code': item,
	# 											'qty': total_qty,
	# 											'item_name': item_obj.item_name,
	# 											'warehouse': warehouse,
	# 											'uom': item_obj.stock_uom,
	# 											'batch_no': batch_no,
	# 											'free_qty': free_qty,
	# 											# 'in_crate': total_qty[0][1]
	# 										})
	# 								total_supp_qty += total_qty
	# 								total_free_qty += free_qty
	# 			elif has_batch_no == 0:
	# 				lst3 = []
	# 				for itm in self.items:
	# 					if itm.delivery_note == delivery_note and itm.item_code == item:
	# 						lst3.append(itm.warehouse)
	# 				for warehouse in set(lst3):
	# 					print("warehouse ********", warehouse)
	# 					lst4 = []
	# 					free_qty = 0
	# 					total_qty = 0
	# 					for itm in self.items:
	# 						if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse  and itm.is_free_item == 1:
	# 							free_qty += itm.qty
	# 						if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse  and itm.is_free_item == 0:
	# 							total_qty += itm.qty
	# 						if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse:
	# 							doc.append('merge_item', {
	# 								'item_code': item,
	# 								'qty': total_qty,
	# 								'item_name': item_obj.item_name,
	# 								'warehouse': warehouse,
	# 								'uom': item_obj.stock_uom,
	# 								'free_qty': free_qty,
	# 								# 'in_crate': total_qty[0][1]
	# 							})
	# 							total_supp_qty += total_qty
	# 							total_free_qty += free_qty
	# 		doc.save()
	# doc.set_missing_values()
	# 	doc.insert()


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
	# print("********",doclist)
	return doclist
