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
			lst.append(itm.delivery_note)
		print("lst   ",lst)
		for delivery_note in set(lst):
			print("******* delivery Note ********",delivery_note)
			doc = frappe.new_doc("Gate Pass")
			doc.total_qty = 0
			doc.total_free_qty = 0
			doc.date = self.date
			doc.transporter = self.transporter
			doc.shift = self.shift
			doc.route = self.route
			total_supp_qty = 0
			total_free_qty = 0
			lst2 = []
			for itm in self.items:
				if itm.delivery_note == delivery_note:
					lst2.append(itm.item_code)
			for item in set(lst2):
				print("items ***************88",item)
				item_obj = frappe.get_doc("Item", item)
				has_batch_no = item_obj.has_batch_no
				if has_batch_no == 1:
					lst3 = []
					for itm in self.items:
						if itm.delivery_note == delivery_note and itm.item_code == item:
							lst3.append(itm.warehouse)
						for warehouse in set(lst3):
							print("warehouse ********",warehouse)
							lst4 = []
							for itm in self.items:
								if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse:
									lst4.append(itm.batch_no)
								for batch_no in set(lst4):
									free_qty = 0
									total_qty = 0
									for itm in self.items:
										if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse and itm.batch_no == batch_no and itm.is_free_item == 1:
											free_qty += itm.qty
										if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse and itm.batch_no == batch_no and itm.is_free_item == 0:
											total_qty += itm.qty
										if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse and itm.batch_no == batch_no:
											doc.append('merge_item', {
														'item_code': item,
														'qty': total_qty,
														'item_name': item_obj.item_name,
														'warehouse': warehouse,
														'uom': item_obj.stock_uom,
														'batch_no': batch_no,
														'free_qty': free_qty,
														# 'in_crate': total_qty[0][1]
													})
											total_supp_qty += total_qty
											total_free_qty += free_qty
				elif has_batch_no == 0:
					lst3 = []
					for itm in self.items:
						if itm.delivery_note == delivery_note and itm.item_code == item:
							lst3.append(itm.warehouse)
						for warehouse in set(lst3):
							print("warehouse ********", warehouse)
							lst4 = []
							free_qty = 0
							total_qty = 0
							for itm in self.items:
								if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse  and itm.is_free_item == 1:
									free_qty += itm.qty
								if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse  and itm.is_free_item == 0:
									total_qty += itm.qty
								if itm.delivery_note == delivery_note and itm.item_code == item and itm.warehouse == warehouse:
									doc.append('merge_item', {
										'item_code': item,
										'qty': total_qty,
										'item_name': item_obj.item_name,
										'warehouse': warehouse,
										'uom': item_obj.stock_uom,
										'free_qty': free_qty,
										# 'in_crate': total_qty[0][1]
									})
									total_supp_qty += total_qty
									total_free_qty += free_qty
	# doc.save()
	# doc.set_missing_values()
		doc.insert()

# def create_delivery_note(self):
	# 	print("****************************")
	#
	# 	# total_crate_return = 0
	# 	dist_del_note = frappe.db.sql(
	# 		""" select distinct(delivery_note) from `tabBulk Gate Pass Item` where parent = %(parent)s """,
	# 		{'parent': self.name})
	# 	for l in range(0, len(dist_del_note)):
	# 		print("-----------")
	# 		doc = frappe.new_doc("Gate Pass")
	# 		# frappe.db.sql("delete from `tabMerge Gate Pass Item` where parent = %s", (doc.name))
	# 		# frappe.db.commit()
	# 		doc.total_qty = 0
	# 		doc.total_free_qty = 0
	# 		doc.date = self.date
	# 		doc.transporter = self.transporter
	# 		doc.shift = self.shift
	# 		doc.route = self.route
	# 		total_supp_qty = 0
	# 		total_free_qty = 0
	# 		dist_item = frappe.db.sql(
	# 			""" select distinct(item_code) from `tabBulk Gate Pass Item` where parent = %(parent)s and delivery_note = %(delivery_note)s""",
	# 			{'parent': self.name, 'delivery_note': dist_del_note[l][0]})
	# 		print("##################", dist_item)
	# 		for i in range(0, len(dist_item)):
	# 			item_obj = frappe.get_doc("Item", dist_item[i][0])
	# 			has_batch_no = item_obj.has_batch_no
	# 			if has_batch_no == 1:
	# 				warehouse = frappe.db.sql(
	# 					""" select distinct(warehouse) from `tabBulk Gate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and delivery_note = %(delivery_note)s """,
	# 					{'parent': self.name, 'item_code': dist_item[i][0], 'delivery_note': dist_del_note[l][0]})
	# 				print("len********************", len(warehouse))
	# 				if len(warehouse) > 0:
	# 					for j in range(0, len(warehouse)):
	# 						dist_batch_no = frappe.db.sql(
	# 							""" select distinct(batch_no) from `tabBulk Gate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and delivery_note = %(delivery_note)s""",
	# 							{'parent': self.name, 'item_code': dist_item[i][0],
	# 							 'delivery_note': dist_del_note[l][0]})
	# 						for k in range(0, len(dist_batch_no)):
	# 							free_qty = 0
	# 							free_qty_list = frappe.db.sql(
	# 								""" select sum(qty) from `tabBulk Gate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 1
    #                                 and batch_no = %(batch_no)s and delivery_note = %(delivery_note)s """,
	# 								{'parent': self.name, 'item_code': dist_item[i][0], 'batch_no': dist_batch_no[k][0],
	# 								 'delivery_note': dist_del_note[l][0]})
	# 							if free_qty_list:
	# 								free_qty = free_qty_list[0][0]
	#
	# 							total_qty = frappe.db.sql(
	# 								""" select sum(qty) from `tabBulk Gate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 0
    #                                 and batch_no = %(batch_no)s and delivery_note = %(delivery_note)s """,
	# 								{'parent': self.name, 'item_code': dist_item[i][0], 'batch_no': dist_batch_no[k][0],
	# 								 'delivery_note': dist_del_note[l][0]})
	# 							print("*************************", total_qty)
	# 							ttl_qty = str(total_qty[0][0])
	#
	# 							if ttl_qty != "None":
	# 								item_doc = frappe.get_doc("Item", dist_item[i][0])
	# 								itm_name = item_doc.item_name
	# 								stock_uom = item_doc.stock_uom
	# 								doc.append('merge_item', {
	# 									'item_code': dist_item[i][0],
	# 									'qty': total_qty[0][0],
	# 									'item_name': itm_name,
	# 									'warehouse': warehouse[0][0],
	# 									'uom': stock_uom,
	# 									'batch_no': dist_batch_no[k][0],
	# 									'free_qty': free_qty,
	# 									# 'in_crate': total_qty[0][1]
	# 								})
	# 								total_supp_qty += total_qty[0][0]
	# 								# total_crate_return += total_qty[0][1]
	# 								str_free_qty = str(free_qty)
	# 								if (str_free_qty != "None"):
	# 									total_free_qty += int(free_qty)
	# 							elif ttl_qty == "None" and free_qty != 0:
	# 								item_doc = frappe.get_doc("Item", dist_item[i][0])
	# 								itm_name = item_doc.item_name
	# 								stock_uom = item_doc.stock_uom
	# 								doc.append('merge_item', {
	# 									'item_code': dist_item[i][0],
	# 									'item_name': itm_name,
	# 									'warehouse': warehouse[0][0],
	# 									'uom': stock_uom,
	# 									'batch_no': dist_batch_no[k][0],
	# 									'free_qty': free_qty,
	# 									# 'in_crate': total_qty[0][1]
	# 								})
	# 								total_free_qty += free_qty
	#
	# 			elif has_batch_no == 0:
	# 				warehouse = frappe.db.sql(
	# 					""" select distinct(warehouse) from `tabBulk Gate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and delivery_note = %(delivery_note)s """,
	# 					{'parent': self.name, 'item_code': dist_item[i][0], 'delivery_note': dist_del_note[l][0]})
	# 				print("len********************", len(warehouse))
	# 				if len(warehouse) > 0:
	# 					for j in range(0, len(warehouse)):
	# 						free_qty = 0
	# 						free_qty_list = frappe.db.sql(
	# 							""" select sum(qty) from `tabBulk Gate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 1 and delivery_note = %(delivery_note)s""",
	# 							{'parent': self.name, 'item_code': dist_item[i][0],
	# 							 'delivery_note': dist_del_note[l][0]})
	# 						if free_qty_list:
	# 							free_qty = free_qty_list[0][0]
	#
	# 						total_qty = frappe.db.sql(
	# 							""" select sum(qty) from `tabBulk Gate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 0 and delivery_note = %(delivery_note)s""",
	# 							{'parent': self.name, 'item_code': dist_item[i][0],
	# 							 'delivery_note': dist_del_note[l][0]})
	# 						print("*************************", total_qty)
	# 						ttl_qty = str(total_qty[0][0])
	#
	# 						if ttl_qty != "None":
	# 							item_doc = frappe.get_doc("Item", dist_item[i][0])
	# 							itm_name = item_doc.item_name
	# 							stock_uom = item_doc.stock_uom
	# 							doc.append('merge_item', {
	# 								'item_code': dist_item[i][0],
	# 								'qty': total_qty[0][0],
	# 								'item_name': itm_name,
	# 								'warehouse': warehouse[0][0],
	# 								'uom': stock_uom,
	# 								'free_qty': free_qty,
	# 								# 'in_crate': total_qty[0][1]
	# 							})
	# 							total_supp_qty += total_qty[0][0]
	# 							# total_crate_return += total_qty[0][1]
	# 							str_free_qty = str(free_qty)
	# 							if (str_free_qty != "None"):
	# 								total_free_qty += int(free_qty)
	# 						elif ttl_qty == "None" and free_qty != 0:
	# 							item_doc = frappe.get_doc("Item", dist_item[i][0])
	# 							itm_name = item_doc.item_name
	# 							stock_uom = item_doc.stock_uom
	# 							doc.append('merge_item', {
	# 								'item_code': dist_item[i][0],
	# 								'item_name': itm_name,
	# 								'warehouse': warehouse[0][0],
	# 								'uom': stock_uom,
	# 								'free_qty': free_qty,
	# 							})
	# 							total_free_qty += free_qty
	# 		doc.total_qty = total_supp_qty
	# 		doc.total_free_qty = total_free_qty
	# 		doc.save()
			# frappe.db.sql("delete from `tabBulk Gate Pass Creation Tools`")
			# frappe.db.commit()

@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None, skip_item_mapping=False):
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
			]
		}
	}, target_doc)
	# print("********",doclist)
	return doclist
