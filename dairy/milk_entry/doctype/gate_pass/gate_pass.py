# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import json
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form
from frappe import _
from six import string_types
from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.controllers.selling_controller import SellingController
from frappe.automation.doctype.auto_repeat.auto_repeat import get_next_schedule_date
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.manufacturing.doctype.production_plan.production_plan import get_items_for_material_requests
from erpnext.accounts.doctype.sales_invoice.sales_invoice import validate_inter_company_party, update_linked_doc,\
	unlink_inter_company_doc
class GatePass(Document):
	def on_submit(self):
		for i in self.item:
			if i.delivery_note:
				del_note = frappe.get_doc("Delivery Note",i.delivery_note)
				del_note.crate_gate_pass_done = 1
				del_note.db_update()

	def on_cancel(self):
		for i in self.item:
			if i.delivery_note:
				del_note = frappe.get_doc("Delivery Note", i.delivery_note)
				del_note.crate_get_pass_done = 0
				del_note.db_update()


@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None, skip_item_mapping=False):
	doclist = get_mapped_doc("Delivery Note", source_name, {
		"Delivery Note": {
			"doctype": "Gate Pass",
			"validation": {
				"docstatus": ["=", 1]
				# "material_request_type": ["=", "Purchase"]
			}
		},
		"Delivery Note Item": {
			"doctype": "Gate Pass Item",
			"field_map": [
				["stock_qty", 'qty'],
				["item_code", "item_code"],
				["stock_uom", "uom"],
				["delivery_note_item","name"],
				["is_free_item", "is_free_item"],
			]
		}
	}, target_doc)
	# print("********",doclist)
	return doclist

# @frappe.whitelist()
# def make_delivery_note(source_name, target_doc=None, skip_item_mapping=False):
# 	def set_missing_values(source, target):
# 		target.ignore_pricing_rule = 1
# 		target.run_method("set_missing_values")
# 		target.run_method("set_po_nos")
# 		target.run_method("calculate_taxes_and_totals")
#
# 		if source.company_address:
# 			target.update({'company_address': source.company_address})
# 		else:
# 			# set company address
# 			target.update(get_company_address(target.company))
#
# 		if target.company_address:
# 			target.update(get_fetch_values("Delivery Note", 'company_address', target.company_address))
#
#
#
# 	mapper = {
# 		"Delivery Note": {
# 			"doctype": "Gate Pass",
# 			"validation": {
# 				"docstatus": ["=", 1]
# 				# "material_request_type": ["=", "Purchase"]
# 			}
# 		},
# 		"Delivery Note Item": {
# 			"doctype": "Gate Pass Item",
# 			"field_map": [
# 				["item_code", "item_code"],
# 				["uom", "uom"]
# 			]
# 		}
#
# 	}
#
# 	if not skip_item_mapping:
# 		mapper["Delivery Note Item"] = {
# 			"doctype": "Gate Pass Item",
# 			"field_map": {
# 				"item_code": "item_code",
# 				"uom": "uom"
# 			}
# 		}
#
# 	target_doc = get_mapped_doc("Delivery Note", source_name, mapper, target_doc, set_missing_values)
#
# 	return target_doc
# @frappe.whitelist()

@frappe.whitelist()
def merge_items(doc_name):
	doc = frappe.get_doc("Gate Pass", doc_name)
	frappe.db.sql("delete from `tabMerge Gate Pass Item` where parent = %s", (doc.name))

	dist_item = frappe.db.sql(""" select distinct(item_code) from `tabGate Pass Item` where parent = %(parent)s """,
							  {'parent': doc_name})
	print("##################", dist_item)
	for i in range(0, len(dist_item)):
		item_obj = frappe.get_doc("Item",dist_item[i][0])
		has_batch_no = item_obj.has_batch_no
		if has_batch_no == 1:
			warehouse = frappe.db.sql(
				""" select distinct(warehouse) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s """,
				{'parent': doc_name, 'item_code': dist_item[i][0]})
			print("len********************", len(warehouse))
			if len(warehouse) > 0:
				for j in range(0, len(warehouse)):
					dist_batch_no = frappe.db.sql(
						""" select distinct(batch_no) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s""",
						{'parent': doc_name, 'item_code': dist_item[i][0]})
					for k in range(0, len(dist_batch_no)):
						free_qty = 0
						free_qty_list = frappe.db.sql(
							""" select sum(qty) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 1 
                            and batch_no = %(batch_no)s """,{'parent': doc_name, 'item_code': dist_item[i][0], 'batch_no': dist_batch_no[k][0]})
						if free_qty_list:
							free_qty = free_qty_list[0][0]

						total_qty = frappe.db.sql(
							""" select sum(qty) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 0 
							and batch_no = %(batch_no)s""",
							{'parent': doc_name, 'item_code': dist_item[i][0], 'batch_no': dist_batch_no[k][0]})
						print("*************************", total_qty)
						ttl_qty = str(total_qty[0][0])

						if ttl_qty != "None":
							item_doc = frappe.get_doc("Item", dist_item[i][0])
							itm_name = item_doc.item_name
							stock_uom = item_doc.stock_uom
							doc.append('merge_item', {
								'item_code': dist_item[i][0],
								'qty': total_qty[0][0],
								'item_name': itm_name,
								'warehouse': warehouse[0][0],
								'uom': stock_uom,
								'batch_no': dist_batch_no[k][0],
								'free_qty': free_qty,
							})

						elif ttl_qty == "None" and free_qty != 0:
							item_doc = frappe.get_doc("Item", dist_item[i][0])
							itm_name = item_doc.item_name
							stock_uom = item_doc.stock_uom
							doc.append('merge_item', {
								'item_code': dist_item[i][0],
								'item_name': itm_name,
								'warehouse': warehouse[0][0],
								'uom': stock_uom,
								'batch_no': dist_batch_no[k][0],
								'free_qty': free_qty,
							})

		elif has_batch_no == 0:
			warehouse = frappe.db.sql(
				""" select distinct(warehouse) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s """,
				{'parent': doc_name, 'item_code': dist_item[i][0]})
			print("len********************", len(warehouse))
			if len(warehouse) > 0:
				for j in range(0, len(warehouse)):
					free_qty = 0
					free_qty_list = frappe.db.sql(
						""" select sum(qty) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 1 """,
						{'parent': doc_name, 'item_code': dist_item[i][0]})
					if free_qty_list:
						free_qty = free_qty_list[0][0]

					total_qty = frappe.db.sql(
						""" select sum(qty) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 0 """,
						{'parent': doc_name, 'item_code': dist_item[i][0]})
					print("*************************", total_qty)
					ttl_qty = str(total_qty[0][0])

					if ttl_qty != "None":
						item_doc = frappe.get_doc("Item", dist_item[i][0])
						itm_name = item_doc.item_name
						stock_uom = item_doc.stock_uom
						doc.append('merge_item', {
							'item_code': dist_item[i][0],
							'qty': total_qty[0][0],
							'item_name': itm_name,
							'warehouse': warehouse[0][0],
							'uom': stock_uom,
							'batch_no': dist_batch_no[k][0],
							'free_qty': free_qty,
						})

					elif ttl_qty == "None" and free_qty != 0:
						item_doc = frappe.get_doc("Item", dist_item[i][0])
						itm_name = item_doc.item_name
						stock_uom = item_doc.stock_uom
						doc.append('merge_item', {
							'item_code': dist_item[i][0],
							'item_name': itm_name,
							'warehouse': warehouse[0][0],
							'uom': stock_uom,
							'batch_no': dist_batch_no[k][0],
							'free_qty': free_qty,
						})


				# dist_batch_no = frappe.db.sql(
				# 	""" select distinct(batch_no) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 0 """,
				# 	{'parent': doc_name, 'item_code': dist_item[i][0]})
				# for k in range(0,len(dist_batch_no)):
				# 	total_qty = frappe.db.sql(
				# 		""" select sum(qty) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 0
				# 		and batch_no = %(batch_no)s""",
				# 		{'parent': doc_name, 'item_code': dist_item[i][0],'batch_no':dist_batch_no[k][0]})
				# 	print("*************************", total_qty)
				# 	ttl_qty = str(total_qty[0][0])
				# 	if ttl_qty != "None":
				# 		item_doc = frappe.get_doc("Item", dist_item[i][0])
				# 		itm_name = item_doc.item_name
				# 		stock_uom = item_doc.stock_uom
				# 		doc.append('merge_item', {
				# 			'item_code': dist_item[i][0],
				# 			'qty': total_qty[0][0],
				# 			'item_name': itm_name,
				# 			'warehouse': warehouse[0][0],
				# 			'uom': stock_uom,
				# 			'batch_no': dist_batch_no[k][0]
				# 		})
				# 	# free item
				# 	total_qty = frappe.db.sql(
				# 		""" select sum(qty) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 1
				# 		and batch_no = %(batch_no)s """,
				# 		{'parent': doc_name, 'item_code': dist_item[i][0],'batch_no':dist_batch_no[k][0]})
				# 	print("*************************", total_qty)
				# 	ttl_qty = str(total_qty[0][0])
				# 	if ttl_qty != "None":
				# 		item_doc = frappe.get_doc("Item", dist_item[i][0])
				# 		itm_name = item_doc.item_name
				# 		stock_uom = item_doc.stock_uom
				# 		doc.append('merge_item', {
				# 			'item_code': dist_item[i][0],
				# 			'free_qty': total_qty[0][0],
				# 			'item_name': itm_name,
				# 			'warehouse': warehouse[0][0],
				# 			'uom': stock_uom,
				# 			'batch_no': dist_batch_no[k][0]
				# 		})

		# elif len(warehouse) > 1:
		# 	for j in range(0,len(warehouse)):
		# 		dist_batch_no = frappe.db.sql(
		# 			""" select distinct(batch_no) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 0 """,
		# 			{'parent': doc_name, 'item_code': dist_item[i][0]})
		# 		for k in range(0, len(dist_batch_no)):
		# 			total_qty = frappe.db.sql(
		# 				""" select sum(qty) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and warehouse = %(warehouse)s
		# 				and is_free_item = 0 and batch_no = %(batch_no)s""",{'parent': doc_name, 'item_code': dist_item[i][0],'warehouse':warehouse[j][0],'batch_no':dist_batch_no[k][0]})
		# 			ttl_qty = str(total_qty[0][0])
		# 			if ttl_qty != "None":
		# 				item_doc = frappe.get_doc("Item", dist_item[i][0])
		# 				itm_name = item_doc.item_name
		# 				doc.append('merge_item', {
		# 					'item_code': dist_item[i][0],
		# 					'qty': total_qty[0][0],
		# 					'item_name': itm_name,
		# 					'warehouse': warehouse[j][0],
		# 					'batch_no': dist_batch_no[k][0]
		# 				})

				# free item quantity
				# 	total_qty = frappe.db.sql(
				# 		""" select sum(qty) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and warehouse = %(warehouse)s
				# 		and is_free_item = 1 and batch_no = %(batch_no)s """,
				# 		{'parent': doc_name, 'item_code': dist_item[i][0], 'warehouse': warehouse[j][0],'batch_no':dist_batch_no[k][0]})
				# 	ttl_qty = str(total_qty[0][0])
				# 	if ttl_qty != "None":
				# 		item_doc = frappe.get_doc("Item", dist_item[i][0])
				# 		itm_name = item_doc.item_name
				# 		doc.append('merge_item', {
				# 			'item_code': dist_item[i][0],
				# 			'free_qty': total_qty[0][0],
				# 			'item_name': itm_name,
				# 			'warehouse': warehouse[j][0],
				# 			'batch_no': dist_batch_no[k][0]
				# 		})
	doc.save()

@frappe.whitelist()
def calculate_crate(doc_name = None):
	doc = frappe.get_doc("Gate Pass",doc_name)
	frappe.db.sql("delete from `tabLoose Crate` where parent = %s", (doc.name))
	for itm in doc.merge_item:
		# warehouse = itm.warehouse
		if itm.qty:
			count = 0
			crate_count = frappe.get_doc("Item",itm.item_code)
			overage = crate_count.crate_overage
			for itms in crate_count.crate:
				if count == 0:
					if itms.crate_quantity and itms.crate_type and itm.warehouse == itms.warehouse:
						# doc.append('crate', {
						# 	'crate_type': itms.crate_type,
						# 	'outgoing_count': int(round((itm.qty / int((itms.crate_quantity) * (1 + overage/100))),2))
						#
						# })
						itm.crate_type = itms.crate_type
						itm.out_crate = int(round((itm.qty / int((itms.crate_quantity) * (1 + overage/100))),2))
						doc.append('loose_crates', {
							'crate_type': itms.crate_type,
							'qty': int(round((itm.qty) % int((itms.crate_quantity) * (1 + overage/100)),2))
						})
						count = 1

	doc.save(ignore_permissions=True)
