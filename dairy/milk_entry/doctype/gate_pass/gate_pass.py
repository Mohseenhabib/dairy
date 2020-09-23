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
		frappe.db.sql("delete from `tabMerge Gate Pass Item` where parent = %(name)s", {'name': self.name})
		frappe.db.commit()
		frappe.db.sql("delete from `tabLeakage Item` where parent = %(name)s", {'name': self.name})
		frappe.db.commit()

		for i in self.item:
			if i.delivery_note:
				frappe.db.sql(""" update `tabDelivery Note` set crate_gate_pass_done = 0 where name = %(name)s """,{'name': i.delivery_note})
				frappe.db.commit()
				frappe.db.sql(""" update `tabGate Pass` set gate_crate_cal_done = " " where name = %(name)s """,
							  {'name': self.name})
				frappe.db.commit()

		self.reload()
	def before_submit(sales):
		frappe.db.sql("delete from `tabLeakage Item` where parent = %(name)s",{'name':sales.name})
		frappe.db.commit()

		frappe.db.sql("delete from `tabCrate Summary` where parent = %(name)s", {'name': sales.name})
		frappe.db.commit()


		# ******************************************************************************************************
		# if frappe.db.get_single_value("Dairy Settings", "leakage_calculated_on") == "Gate Pass":
		# 	if frappe.db.get_single_value("Dairy Settings","leakage_percentage") and frappe.db.get_single_value("Dairy Settings","leakage_qty"):
		# 		leakage_perc = float(frappe.db.get_single_value("Dairy Settings", "leakage_percentage"))
		# 		leakage_qty = float(frappe.db.get_single_value("Dairy Settings", "leakage_qty"))
		# 		applicable_on = (frappe.db.get_single_value("Dairy Settings", "applicable_on"))
		#
		# 		if not sales.customer:
		# 			frappe.throw("Select Customer For leakage Items")
		# 		doc = frappe.get_doc("Gate Pass", sales.name)
		# 		lst = []
		# 		for line in doc.merge_item:
		# 			item = frappe.get_doc("Item", line.item_code)
		# 			if item.variant_of and item.leakage_applicable:
		# 				line.variant_of = item.variant_of
		# 				line.leakage_applicable = 1
		# 				line.leakage_variant = item.leakage_variant
		# 				# line.total_weight = (line.qty * item.weight_per_unit)
		# 				# lst.append(item.variant_of)
		# 			if not item.variant_of:
		# 				print("**",item.item_code)
		#
		# 				if item.leakage_applicable and applicable_on == "Stock UOM" and line.qty > leakage_qty:
		# 					qty = (line.qty * leakage_perc) / 100
		# 					uom = frappe.get_doc("UOM", line.uom)
		# 					if uom.must_be_whole_number:
		# 						qty = round((line.qty * leakage_perc) / 100)
		# 					if qty == 0:
		# 						qty = 1
		# 					doc.append("leakage_item", {
		# 						"item": line.item_code,
		# 						"item_name": line.item_name,
		# 						"leakage_qty": qty,
		# 						"uom": item.stock_uom
		# 					})
		#
		# 				if item.leakage_applicable and applicable_on == "Order UOM" and line.qty > leakage_qty:
		# 					qty = (line.qty * leakage_perc) / 100
		# 					uom1 = frappe.get_doc("UOM", line.uom)
		# 					if uom1.must_be_whole_number:
		# 						qty = round((line.qty * leakage_perc) / 100)
		# 					if qty == 0:
		# 						qty = 1
		# 					doc.append("leakage_item", {
		# 						"item": line.item_code,
		# 						"item_name": line.item_name,
		# 						"leakage_qty": qty,
		# 						"uom": line.uom
		# 					})
		# 		doc.save(ignore_permissions=True)
		# 		# obj = frappe.get_doc("Gate Pass", sales.name)
		# 		dist_var = frappe.db.sql(""" select distinct(variant_of) from `tabMerge Gate Pass Item` where parent = %(name)s and
		# 		 		leakage_applicable = 1 """,
		# 							{'name':sales.name})
		# 		print("****************************dsit var***************************",dist_var)
		# 		for varant in dist_var:
		# 			dist_leak_var = frappe.db.sql(""" select distinct(leakage_variant) from `tabMerge Gate Pass Item` where parent = %(name)s and
		# 		 		leakage_applicable = 1 and variant_of = %(variant_of)s """,{'name':sales.name,'variant_of':varant[0]})
		# 			print("varant",varant)
		# 			print("dist_leak_var",)
		# 			item = frappe.get_doc("Item", varant[0])
		# 			sum_qty = frappe.db.sql(
		# 				""" select sum(total_weight),uom from `tabMerge Gate Pass Item`  where variant_of = %(variant)s and parent = %(name)s """,
		# 				{'variant': varant[0], 'name': sales.name})
		# 			print("sum qty",sum_qty)
		#
		# 			chek_lakge_var_for_itms = frappe.db.sql(
		# 				""" select item_code from `tabMerge Gate Pass Item`  where variant_of = %(variant)s and parent = %(name)s """,
		# 				{'variant': varant[0], 'name': sales.name})
		#
		# 			var_itm_code = ""
		# 			var_itm_name = ""
		# 			var_itm_uom = ""
		#
		# 			for itms in chek_lakge_var_for_itms:
		# 				leakage_varnt = frappe.db.sql(""" select leakage_variant from `tabItem`
		# 											where name = %(variant)s and leakage_variant  IS NOT NULL """,
		# 												{'variant': itms})
		# 				if leakage_varnt:
		# 					print("------------------____________________---------------",leakage_varnt[0][0])
		# 					leak_var_item = frappe.get_doc("Item",leakage_varnt[0][0])
		# 					var_itm_code = leak_var_item.item_code
		# 					var_itm_name = leak_var_item.item_name
		# 					var_itm_uom = leak_var_item.stock_uom
		#
		# 			# if item.leakage_variant:
		# 			# 	var_itm = frappe.get_doc("Item",item.leakage_variant)
		# 			# 	var_itm_code = var_itm.item_code
		# 			# 	var_itm_name = var_itm.item_name
		# 			# 	var_itm_uom = var_itm.stock_uom
		#
		# 			if applicable_on == "Stock UOM" and sum_qty[0][0] > leakage_qty:
		# 				print("***1",sum_qty[0][0])
		# 				qty = (sum_qty[0][0] * leakage_perc) / 100
		# 				uom = frappe.get_doc("UOM", sum_qty[0][1])
		# 				if uom.must_be_whole_number:
		# 					qty = round((sum_qty[0][0] * leakage_perc) / 100)
		# 				if qty == 0:
		# 					qty = 1
		# 				print("*************sum_qty",sum_qty[0][0])
		# 				if sum_qty[0][0] > 0:
		# 					if var_itm_code != "":
		# 						sales.append("leakage_item", {
		# 							"item": var_itm_code,
		# 							"item_name": var_itm_name,
		# 							"leakage_qty": qty,
		# 							"uom": var_itm_uom
		# 						})
		# 					else:
		# 						sales.append("leakage_item", {
		# 							"item": item.item_code,
		# 							"item_name": item.item_name,
		# 							"leakage_qty": qty,
		# 							"uom": item.stock_uom
		# 						})
		# 			if applicable_on == "Order UOM" and sum_qty[0][0] > leakage_qty:
		#
		# 				print("***2", sum_qty[0][0])
		# 				qty = (sum_qty[0][0] * leakage_perc) / 100
		# 				uom = frappe.get_doc("UOM", sum_qty[0][1])
		# 				if uom.must_be_whole_number:
		# 					qty = round((sum_qty[0][0] * leakage_perc) / 100)
		# 				if qty == 0:
		# 					qty = 1
		# 				print("*************sum_qty", sum_qty[0][0])
		# 				if sum_qty[0][0] > 0:
		# 					if var_itm_code != "":
		# 						sales.append("leakage_item", {
		# 							"item": var_itm_code,
		# 							"item_name": var_itm_name,
		# 							"leakage_qty": qty,
		# 							"uom": sum_qty[0][1]
		# 						})
		# 					else:
		# 						sales.append("leakage_item", {
		# 							"item": item.item_code,
		# 							"item_name": item.item_name,
		# 							"leakage_qty": qty,
		# 							"uom": sum_qty[0][1]
		# 						})
		# 						************************  New  **************************
		if frappe.db.get_single_value("Dairy Settings", "leakage_calculated_on") == "Gate Pass":
			if frappe.db.get_single_value("Dairy Settings","leakage_percentage") and frappe.db.get_single_value("Dairy Settings","leakage_qty"):
				leakage_perc = float(frappe.db.get_single_value("Dairy Settings", "leakage_percentage"))
				leakage_qty = float(frappe.db.get_single_value("Dairy Settings", "leakage_qty"))
				applicable_on = (frappe.db.get_single_value("Dairy Settings", "applicable_on"))

				if not sales.customer:
					frappe.throw("Select Customer For leakage Items")
				lst = []
				for line in sales.merge_item:
					item = frappe.get_doc("Item", line.item_code)
					if item.variant_of and item.leakage_applicable:
						line.variant_of = item.variant_of
						line.leakage_applicable = 1
						line.leakage_variant = item.leakage_variant
					# line.total_weight = (line.qty * item.weight_per_unit)
					# lst.append(item.variant_of)
					else:
						print("**", item.item_code)
						if item.leakage_applicable and applicable_on == "Stock UOM" and line.qty > leakage_qty:
							qty = (line.qty * leakage_perc) / 100
							print("******************8uoms  ",line.uom)
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

						if item.leakage_applicable and applicable_on == "Order UOM" and line.qty > leakage_qty:
							qty = (line.qty * leakage_perc) / 100
							print("******************8uoms  ", line.uom)
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

				dist_variant_itm = []
				for itm in sales.merge_item:
					if itm.variant_of:
						dist_variant_itm.append(itm.variant_of)

				print("************************** variant items******************************",dist_variant_itm)

				for dis_itm in set(dist_variant_itm):
					dist_leakge_variant = []
					item_obj = frappe.get_doc("Item",dis_itm)
					for itm in sales.merge_item:
						if itm.variant_of == dis_itm:
							dist_leakge_variant.append(itm.leakage_variant)
					print("****************************dist_leakge_variant************************",dist_leakge_variant)
					total_weight = 0
					line_uom = ""
					for leakge_variant in set(dist_leakge_variant):
						leakage_variant_itm_obj = frappe.get_doc("Item",leakge_variant)

						for itm in sales.merge_item:
							if itm.variant_of == dis_itm and itm.leakage_variant == leakge_variant:
								total_weight += itm.total_weight
								line_uom = itm.uom
						print("****************************",total_weight)
						if applicable_on == "Stock UOM" and total_weight > leakage_qty:
							qty = (total_weight * leakage_perc) / 100
							print("uoms  ",item_obj.stock_uom)
							uom = frappe.get_doc("UOM", item_obj.stock_uom)
							if uom.must_be_whole_number:
								qty = round((total_weight * leakage_perc) / 100)
							if qty == 0:
								qty = 1
							if total_weight > 0:
								sales.append("leakage_item", {
									"item": leakage_variant_itm_obj.item_code,
									"item_name": leakage_variant_itm_obj.item_name,
									"leakage_qty": qty,
									"uom": uom.name
								})

						if applicable_on == "Order UOM" and total_weight > leakage_qty:
							qty = (total_weight * leakage_perc) / 100
							uom1 = frappe.get_doc("UOM", line_uom)
							if uom1.must_be_whole_number:
								qty = round((total_weight * leakage_perc) / 100)
							if qty == 0:
								qty = 1
							sales.append("leakage_item", {
								"item": leakage_variant_itm_obj.item_code,
								"item_name": leakage_variant_itm_obj.item_name,
								"leakage_qty": qty,
								"uom": uom1.name
							})


		# ***********************************************************************************************************
		if len(sales.get("leakage_item")) > 0:
			dn = frappe.new_doc("Delivery Note")
			dn.posting_date =  frappe.utils.nowdate()
			dn.posting_time =  frappe.utils.nowtime()
			dn.set_posting_time = 1
			dn.route = sales.route
			dn.company = sales.company or "_Test Company"
			dn.customer = sales.customer or "_Test Customer"
			dn.currency = "INR"
			val = 0
			for itm in sales.leakage_item:
				if itm.leakage_qty > 0:
					val = 1
					dn.append("items", {
						"item_code":  itm.item,
						"description": "Leakage From Gate Pass",
						"warehouse":  sales.warehouse,
						"qty":  itm.leakage_qty,
						"rate": 0,
						"conversion_factor": 1.0,
						"allow_zero_valuation_rate":  1,
						"expense_account": frappe.get_cached_value('Company', sales.company, 'expense_account'),
						"cost_center":  frappe.get_cached_value('Company', sales.company, 'cost_center'),
						"is_free_item": 1,
						"uom":itm.uom
					})
			if val == 1:
				dn.save(ignore_permissions=True)
				obj = frappe.get_doc("Delivery Note",dn.name)
				obj.status = "Closed"
				obj.save()
				obj.submit()
				# doc.save(ignore_permissions=True)



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
								""" select sum(qty), sum(total_weight) from `tabGate Pass Item` 
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
									'total_weight': total_qty[0][1]
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
							""" select sum(qty),sum(total_weight) from `tabGate Pass Item` 
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
								'total_weight': total_qty[0][1]
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

def set_delivery_note_missing_values(target):
	target.run_method('set_missing_values')
	target.run_method('set_po_nos')
	target.run_method('calculate_taxes_and_totals')

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
				["weight_per_unit","weight_per_unit"],
				["total_weight","total_weight"]
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
