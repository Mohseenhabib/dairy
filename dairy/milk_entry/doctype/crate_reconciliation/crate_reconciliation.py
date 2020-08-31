# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from erpnext.assets.doctype.asset.depreciation \
	import get_disposal_account_and_cost_center, get_depreciation_accounts
from datetime import datetime

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

	def on_submit(self):
		for i in self.delivery_info:
			if i.delivery_note:
				del_note = frappe.get_doc("Delivery Note",i.delivery_note)
				del_note.crate_reconcilation_done =1
				del_note.db_update()
			if i.gate_pass:
				del_note = frappe.get_doc("Gate Pass", i.gate_pass)
				del_note.crate_reconcilation_done = 1
				del_note.db_update()

	def on_cancel(self):
		for i in self.delivery_info:
			if i.delivery_note:
				del_note = frappe.get_doc("Delivery Note",i.delivery_note)
				del_note.crate_reconcilation_done =0
				del_note.db_update()
			if i.gate_pass:
				del_note = frappe.get_doc("Gate Pass",i.gate_pass)
				del_note.crate_reconcilation_done =0
				del_note.db_update()

	def calculate_crate_type_summary(self):
		if self:
			frappe.db.sql("delete from `tabCrate Type Summary Child` where parent = %s", (self.name))
			result = frappe.db.sql("""select crate_type,sum(difference) as diff from `tabCrate Reconciliation Child`
									where crate_type is not null and parent =%s
									group by crate_type""", (self.name), as_dict=True)
			for i in result:
				self.append("crate_type_summary", {
					"crate_type": i.get('crate_type'),
					"difference": i.get('diff')
				})
			self.flags.ignore_validate_update_after_submit = True   #ignore after submit permission
			self.save(ignore_permissions=True)
		return True

	def make_sales_invoice(self):
		si = frappe.new_doc("Sales Invoice")
		si.company = self.company
		si.customer = self.customer
		si.crate_reconciliation = self.name
		si.route = self.route
		si.due_date = datetime.now().date()
		si.currency = frappe.get_cached_value('Company', self.company, "default_currency")
		disposal_account, depreciation_cost_center = get_disposal_account_and_cost_center(self.company)
		result = frappe.db.sql("""select crate_type,sum(difference) as diff from `tabCrate Reconciliation Child`
											where crate_type is not null and parent =%s
											group by crate_type""", (self.name), as_dict=True)
		for i in result:
			crate_type_doc = frappe.get_doc("Crate Type",i.get('crate_type'))
			si.append("items", {
				"item_code": crate_type_doc.item,
				"income_account": disposal_account,
				"cost_center": depreciation_cost_center,
				"qty": i.get('diff'),
				"rate":crate_type_doc.price
			})
		si.set_missing_values()
		return si


@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None, ignore_permissions=False):
	def set_item_in_sales_invoice(source, target):
		del_note = frappe.get_doc(source)
		crate_recl = frappe.get_doc(target)
		for i in del_note.crate_count:
			out_count = i.outgoing_count if i.outgoing_count else 0
			in_count = i.incoming_count if i.incoming_count else 0
			dam_count = i.damaged_count if i.damaged_count else 0
			vehicle_name = None
			if del_note.route:
				route_doc = frappe.get_doc("Route Master",del_note.route)
				vehicle_name = route_doc.vehicle
			crate_recl.append("delivery_info",{
				"delivery_date": del_note.posting_date,
				"delivery_note": del_note.name,
				"customer": del_note.customer,
				"route": del_note.route,
				"crate_type": i.crate_type,
				"vehicle": vehicle_name,
				"outgoing": out_count,
				"incoming": in_count,
				"damaged": dam_count,
				"difference": out_count - in_count
			})

	doclist = get_mapped_doc("Delivery Note", source_name, {
		"Delivery Note": {
			"doctype": "Crate Reconciliation",
		}
	}, target_doc,set_item_in_sales_invoice)
	return doclist

@frappe.whitelist()
def make_gate_pass(source_name, target_doc=None, ignore_permissions=False):
	def set_item_in_sales_invoice(source, target):
		del_note = frappe.get_doc(source)
		crate_recl = frappe.get_doc(target)
		for i in del_note.crate	:
			out_count = i.outgoing_count if i.outgoing_count else 0
			in_count = i.incoming_count if i.incoming_count else 0
			dam_count = i.damaged_count if i.damaged_count else 0
			vehicle_name = None
			if del_note.route:
				route_doc = frappe.get_doc("Route Master",del_note.route)
				vehicle_name = route_doc.vehicle
			crate_recl.append("delivery_info",{
				"delivery_date": del_note.date,
				"gate_pass": del_note.name,
				"transporter": del_note.transporter,
				"route": del_note.route,
				"crate_type": i.crate_type,
				"vehicle": vehicle_name,
				"outgoing": out_count,
				"incoming": in_count,
				"damaged": dam_count,
				"difference": out_count - in_count
			})

	doclist = get_mapped_doc("Gate Pass", source_name, {
		"Gate Pass": {
			"doctype": "Crate Reconciliation",
		}
	}, target_doc,set_item_in_sales_invoice)
	return doclist