# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
import frappe.utils
from frappe.model.mapper import get_mapped_doc

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
				frappe.db.sql(""" update `tabDelivery Note` set crate_gate_pass_done = 0 where name = %(name)s """,{'name': i.delivery_note})
				frappe.db.commit()
				frappe.db.sql(""" update `tabGate Pass` set gate_crate_cal_done = " " where name = %(name)s """,
							  {'name': self.name})
				frappe.db.commit()


	def before_submit(sales):
		frappe.db.sql("delete from `tabLeakage Item` where parent = %(name)s",{'name':sales.name})
		frappe.db.commit()

		frappe.db.sql("delete from `tabCrate Summary` where parent = %(name)s", {'name': sales.name})
		frappe.db.commit()

		if frappe.db.get_single_value("Dairy Settings", "leakage_calculated_on") == "Gate Pass":
			if frappe.db.get_single_value("Dairy Settings", "leakage_percentage") and frappe.db.get_single_value("Dairy Settings", "leakage_qty"):
				leakage_perc = float(frappe.db.get_single_value("Dairy Settings", "leakage_percentage"))
				leakage_qty = float(frappe.db.get_single_value("Dairy Settings", "leakage_qty"))
				applicable_on = (frappe.db.get_single_value("Dairy Settings", "applicable_on"))
				if not sales.customer:
					frappe.throw("Select Customer For leakage Items")

				# del_note = frappe.new_doc("Delivery Note")
				# del_note.customer = sales.customer
				# del_note.route = sales.route
				lst = []
				for line in sales.merge_item:
					lst.append(line)
				total_leakage = 0

				for line in lst:
					item = frappe.get_doc("Item", line.item_code)
					if item.leakage_applicable and applicable_on == "Stock UOM" and line.qty > leakage_qty:
						qty = (line.qty * leakage_perc) / 100
						uom = frappe.get_doc("UOM", line.uom)
						if uom.must_be_whole_number:
							qty = round((line.qty * leakage_perc) / 100)
						if qty == 0:
							qty = 1
						sales.append("leakage_item", {
							"item": line.item_code,
							"item_name": line.item_name,
							"leakage_qty": qty,
							"uom": item.stock_uom
						})
						# del_note.append("items",{
						# 	"item_code": line.item_code,
						# 	"item_name": line.item_name,
						# 	"qty": qty,
						# 	"uom": item.stock_uom,
						# 	"stock_uom": item.stock_uom
						# })
						total_leakage += qty


					if item.leakage_applicable and applicable_on == "Order UOM" and line.qty > leakage_qty:
						qty = (line.qty * leakage_perc) / 100
						uom1 = frappe.get_doc("UOM", line.uom)
						if uom1.must_be_whole_number:
							qty = round((line.qty * leakage_perc) / 100)
						if qty == 0:
							qty = 1
						sales.append("leakage_item", {
							"item": line.item_code,
							"item_name": line.item_name,
							"leakage_qty": qty,
							"uom": line.uom
						})
						# del_note.append("items", {
						# 	"item_code": line.item_code,
						# 	"item_name": line.item_name,
						# 	"qty": qty,
						# 	"uom": line.uom,
						# 	"stock_uom": item.stock_uom
						# })
						total_leakage += qty
				# del_note.save(ignore_permissions=True)
				frappe.db.set(sales, 'total_leakage', total_leakage)



		# for creating crate Log
		if frappe.db.get_single_value("Dairy Settings", "crate_reconciliation_based_on") == "Gate Pass":
			dist_cratetype = frappe.db.sql(""" select distinct(crate_type) 
												from `tabMerge Gate Pass Item` 
												where parent = %(name)s""",{'name':sales.name})
			for crate in dist_cratetype:
				dist_warehouse = frappe.db.sql(""" select distinct(warehouse) 
													from `tabMerge Gate Pass Item` 
													where parent = %(name)s and crate_type = %(crate_type)s """,
													{'name': sales.name,'crate_type':crate})
				for warehouse in dist_warehouse:
					sums = frappe.db.sql(""" select 
												 sum(out_crate) as crate, sum(in_crate) as crate_ret, sum(damaged_crate) as damaged_crate
					 						  from 
					 							`tabMerge Gate Pass Item` 
					 						  where 
					 							 crate_type = %(crate)s and parent = %(name)s and warehouse = %(warehouse)s""",
										 		 {'crate':crate,'name':sales.name,'warehouse':warehouse},as_dict=1)

					log = frappe.new_doc("Crate Log")
					log.transporter = sales.transporter
					log.vehicle = sales.vehicle
					log.route = sales.route
					log.date = frappe.utils.nowdate()
					log.company = sales.company
					log.voucher_type = "Gate Pass"
					log.voucher = sales.name
					log.damaged = sums[0]['damaged_crate']
					log.crate_issue = sums[0]['crate']
					log.crate_return = sums[0]['crate_ret']
					log.crate_type = crate[0]
					log.source_warehouse = warehouse[0]
					log.note = "Entry Created From Gate pass"
					openning_cnt = frappe.db.sql(""" select count(*) from `tabCrate Log`  
													where 
														crate_type = %(crate)s and source_warehouse = %(warehouse)s 
														and company = %(company)s and docstatus = 1	order by date desc """,
												 		{'crate': crate, 'warehouse': warehouse,'company': sales.company}, as_dict=1)
					print("opening_cnt = ",openning_cnt)
					if openning_cnt[0]['count(*)'] > 0:

						openning = frappe.db.sql(""" select crate_balance from `tabCrate Log`  
													where 
													crate_type = %(crate)s and source_warehouse = %(warehouse)s and
													company = %(company)s and  docstatus = 1 order by date desc limit 1 """,
												 	{'crate':crate,'warehouse':warehouse,'company':sales.company},as_dict=1)

						log.crate_opening = int(openning[0]['crate_balance'])
						log.crate_balance = openning[0]['crate_balance'] - (sums[0]['crate'] + sums[0]['crate_ret'])
						sales.append("crate_summary", {
							"crate_opening": openning[0]['crate_balance'] - (sums[0]['crate'] + sums[0]['crate_ret']),
							"crate_issue": sums[0]['crate'],
							"crate_return": sums[0]['crate_ret'],
							"crate_balance": openning[0]['crate_balance'] - (sums[0]['crate'] + sums[0]['crate_ret'])
						})

					else:
						log.crate_opening = int(0)
						log.crate_balance = int(0) - (sums[0]['crate'] + sums[0]['crate_ret'])
						sales.append("crate_summary", {
							"crate_opening": int(0) - (sums[0]['crate'] + sums[0]['crate_ret']),
							"crate_issue": sums[0]['crate'],
							"crate_return": sums[0]['crate_ret'],
							"crate_balance": int(0) - (sums[0]['crate'] + sums[0]['crate_ret'])
						})
					log.save()
					log.submit()



	def after_insert(self):
		self.merge_items(self.name)
		calculate_crate(self.name)
		self.reload()


	def merge_items(self,doc_name):
		doc = frappe.get_doc("Gate Pass", doc_name)
		frappe.db.sql("delete from `tabMerge Gate Pass Item` where parent = %(name)s",{'name':self.name})
		frappe.db.commit()
		doc.total_qty = 0
		doc.total_free_qty = 0
		total_supp_qty = 0
		total_free_qty = 0
		dist_item = frappe.db.sql(""" select distinct(item_code) 
									  from `tabGate Pass Item` 
									  where parent = %(parent)s """,{'parent': doc_name})

		for i in range(0, len(dist_item)):
			item_obj = frappe.get_doc("Item", dist_item[i][0])
			has_batch_no = item_obj.has_batch_no
			if has_batch_no == 1:
				warehouse = frappe.db.sql(""" select distinct(warehouse) 
											  from `tabGate Pass Item` 
											  where parent = %(parent)s and item_code = %(item_code)s """,
											  {'parent': doc_name, 'item_code': dist_item[i][0]})

				if len(warehouse) > 0:
					for j in range(0, len(warehouse)):
						dist_batch_no = frappe.db.sql(""" select distinct(batch_no) 
														   from `tabGate Pass Item` 
														   where parent = %(parent)s and item_code = %(item_code)s""",
														   {'parent': doc_name, 'item_code': dist_item[i][0]})
						for k in range(0, len(dist_batch_no)):
							free_qty = 0
							free_qty_list = frappe.db.sql(""" select sum(qty) 
																from `tabGate Pass Item` 
																where parent = %(parent)s and item_code = %(item_code)s and 
																is_free_item = 1 and batch_no = %(batch_no)s """,
																{'parent': doc_name, 'item_code': dist_item[i][0], 'batch_no': dist_batch_no[k][0]})
							if free_qty_list:
								free_qty = free_qty_list[0][0]

							total_qty = frappe.db.sql(
								""" select sum(qty) from `tabGate Pass Item` 
								    where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 0 and batch_no = %(batch_no)s""",
												{'parent': doc_name, 'item_code': dist_item[i][0], 'batch_no': dist_batch_no[k][0]})

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

								total_supp_qty += total_qty[0][0]
								str_free_qty = str(free_qty)

								if (str_free_qty != "None"):
									total_free_qty += int(free_qty)

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
									# 'in_crate': total_qty[0][1]
								})
								total_free_qty += free_qty

			elif has_batch_no == 0:
				warehouse = frappe.db.sql(
					""" select distinct(warehouse) from `tabGate Pass Item` 
						where parent = %(parent)s and item_code = %(item_code)s """,
						{'parent': doc_name, 'item_code': dist_item[i][0]})

				if len(warehouse) > 0:
					for j in range(0, len(warehouse)):
						free_qty = 0
						free_qty_list = frappe.db.sql(
							""" select sum(qty) from `tabGate Pass Item` 
								where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 1 """,
								{'parent': doc_name, 'item_code': dist_item[i][0]})

						if free_qty_list:
							free_qty = free_qty_list[0][0]

						total_qty = frappe.db.sql(
							""" select sum(qty) from `tabGate Pass Item` 
								where parent = %(parent)s and item_code = %(item_code)s and is_free_item = 0 """,
								{'parent': doc_name, 'item_code': dist_item[i][0]})

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
								'free_qty': free_qty,
								# 'in_crate': total_qty[0][1]
							})
							total_supp_qty += total_qty[0][0]
							# total_crate_return += total_qty[0][1]
							str_free_qty = str(free_qty)
							if (str_free_qty != "None"):
								total_free_qty += int(free_qty)

						elif ttl_qty == "None" and free_qty != 0:
							item_doc = frappe.get_doc("Item", dist_item[i][0])
							itm_name = item_doc.item_name
							stock_uom = item_doc.stock_uom
							doc.append('merge_item', {
								'item_code': dist_item[i][0],
								'item_name': itm_name,
								'warehouse': warehouse[0][0],
								'uom': stock_uom,
								'free_qty': free_qty,
							})
							total_free_qty += free_qty
		doc.total_qty = total_supp_qty
		doc.total_free_qty = total_free_qty
		doc.save()

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
				["is_free_item", "is_free_item"]
			]
		}
	}, target_doc)

	return doclist

@frappe.whitelist()
def calculate_crate(doc_name = None):
	doc = frappe.get_doc("Gate Pass",doc_name)
	frappe.db.sql("delete from `tabLoose Crate` where parent = %s", (doc.name))
	frappe.db.commit()
	doc.total_crate = 0
	total_crate = 0
	for itm in doc.merge_item:
		# warehouse = itm.warehouse
		if itm.qty:
			count = 0
			crate_count = frappe.get_doc("Item",itm.item_code)
			overage = crate_count.crate_overage
			for itms in crate_count.crate:
				if count == 0:
					if itms.crate_quantity and itms.crate_type and itm.warehouse == itms.warehouse:
						itm.crate_type = itms.crate_type
						itm.out_crate = int(round(((itm.qty + itm.free_qty) / int((itms.crate_quantity) * (1 + overage/100))),2))
						total_crate += int(round(((itm.qty + itm.free_qty) / int((itms.crate_quantity) * (1 + overage/100))),2))
						qty = int(round((itm.qty + itm.free_qty) % int((itms.crate_quantity) * (1 + overage / 100)), 2))
						if qty > 0:
							doc.append('loose_crates', {
								'crate_type': itms.crate_type,
								'qty': int(round((itm.qty + itm.free_qty) % int((itms.crate_quantity) * (1 + overage/100)),2)),
								'item_code': itm.item_code
							})
						count = 1
	doc.total_crate = total_crate
	doc.gate_crate_cal_done = "Done"
	doc.save(ignore_permissions=True)
