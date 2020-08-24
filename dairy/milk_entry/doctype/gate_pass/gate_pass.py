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
	pass

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
				["item_code", "item_code"]
			]
		}
	}, target_doc)
	# print("********",doclist)
	return doclist

@frappe.whitelist()
@frappe.whitelist()
def merge_items(doc_name):
	doc = frappe.get_doc("Gate Pass", doc_name)
	dist_item = frappe.db.sql(""" select distinct(item_code) from `tabGate Pass Item` where parent = %(parent)s """,
							  {'parent': doc_name})
	print("##################", dist_item)
	for i in range(0, len(dist_item)):
		warehouse = frappe.db.sql(
			""" select distinct(warehouse) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s """,
			{'parent': doc_name, 'item_code': dist_item[i][0]})
		print("len********************", len(warehouse))
		if len(warehouse) == 1:
			total_qty = frappe.db.sql(
				""" select sum(qty) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s """,
				{'parent': doc_name, 'item_code': dist_item[i][0]})
			print("*************************", total_qty)
			item_doc = frappe.get_doc("Item", dist_item[i][0])
			itm_name = item_doc.item_name
			doc.append('merge_item', {
				'item_code': dist_item[i][0],
				'qty': total_qty[0][0],
				'item_name': itm_name,
				'warehouse': warehouse[0][0]
			})
		elif len(warehouse) > 1:
			for j in range(0,len(warehouse)):
				total_qty = frappe.db.sql(
					""" select sum(qty) from `tabGate Pass Item` where parent = %(parent)s and item_code = %(item_code)s and warehouse = %(warehouse)s""",
					{'parent': doc_name, 'item_code': dist_item[i][0],'warehouse':warehouse[j][0]})
				item_doc = frappe.get_doc("Item", dist_item[i][0])
				itm_name = item_doc.item_name
				doc.append('merge_item', {
					'item_code': dist_item[i][0],
					'qty': total_qty[0][0],
					'item_name': itm_name,
					'warehouse': warehouse[j][0]
				})
	doc.save()

@frappe.whitelist()
def calculate_crate(doc_name = None):
	doc = frappe.get_doc("Gate Pass",doc_name)
	for itm in doc.merge_item:
		count = 0
		crate_count = frappe.get_doc("Item",itm.item_code)
		for itms in crate_count.crate:
			if count == 0:
				if itms.crate_quantity and itms.crate_type:
					doc.append('crate', {
						'crate_type': itms.crate_type,
						'outgoing_count': int(round((itm.qty / (itms.crate_quantity)),2))
					})
			count = 1
	doc.save(ignore_permissions=True)
