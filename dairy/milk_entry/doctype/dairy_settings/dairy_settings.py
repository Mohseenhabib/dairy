# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dexciss Technology by Sid and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date
from datetime import date, timedelta
from frappe.utils import (flt, getdate, get_url, now,
                          nowtime, get_time, today, get_datetime, add_days, datetime)

class DairySettings(Document):
	# def before_save(self):
	# 	purchase_invoice()
	pass

def purchase_invoice():
	
	# tdate = str(date.today())
	p_inv = frappe.get_doc('Dairy Settings')
	if p_inv.default_payment_type == 'Daily':
		purchase = frappe.db.sql("""select distinct(supplier) as name 
											from `tabPurchase Receipt` 
											where docstatus =1 and posting_date ='{0}'
											""".format(getdate(today())), as_dict =True)
					
		print('purchase********************************************',purchase)
		for i in purchase:
		# p_inv = frappe.get_doc('Dairy Settings')
		# if p_inv.default_payment_type == 'Daily':
			pi = frappe.new_doc("Purchase Invoice")
			
			
		
			me = frappe.db.sql("""select milk_entry
											from `tabPurchase Receipt` 
											where supplier = '{0}' and posting_date = '{1}' and docstatus = 1
											""".format(i.name,getdate(today())), as_dict =True)
			
			print('meeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',me)
			for m in me:
				milk = frappe.get_doc('Milk Entry',m.milk_entry)
				print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmm',m.milk_entry)
				ware = frappe.get_doc('Warehouse',{'name':milk.dcs_id})
				print('ware^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',ware)

				# for wh in ware:

					# entry = frappe.db.get_value('Milk Entry',{'name':m.milk_entry},['date'])
					# print('entryYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',entry)

					# query =frappe.db.sql("""select dcs_id,member,milk_type,name,volume
					# 							from `tabMilk Entry` 
					# 							where docstatus =1  and name = '{0}'
					# 							""".format(m.milk_entry), as_dict =True)

					

					# print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',query)
					# for k in query:
					# 	# if query[0]:
					# 		# print('query^^^^^^^^^^^^^^^^^^^^^^^^^',k.name)
						# milk = frappe.get_doc('Milk Entry',m.milk_entry)
						# print('query^^^^^^^^^^^^^^^^^^^^^^^^^',milk.name)

				pr =  frappe.db.get_value('Purchase Receipt',{'milk_entry':milk.name,"docstatus":1},['name'])

				# for j in pr:
				if pr:
					pri =  frappe.get_doc('Purchase Receipt',pr)
					pur_inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':pr},["parent"])
					if not pur_inv:
						
						# pi = frappe.new_doc("Purchase Invoice")
						for itm in pri.items:
							pi.supplier = milk.member if  ware.is_third_party_dcs == 0 else ware.supplier
							pi.name = milk.name
							pi.append(
								"items",
								{
									'item_code': itm.item_code,
									'item_name': itm.item_name,
									'description': itm.description,
									'received_qty': milk.volume,
									'qty': milk.volume,
									'uom': itm.stock_uom,
									'stock_uom': itm.stock_uom,
									'rate': itm.rate,
									'warehouse': milk.dcs_id,
									'purchase_receipt':pr
								}
							)
			pi.save(ignore_permissions = True)
			pi.submit()
			if (pi.docstatus == 1):
				milk.db_set('status','Billed')



	if p_inv.default_payment_type == 'Days':
		
		delta=getdate(date.today()) - getdate(p_inv.previous_sync_date)
		if delta.days >= p_inv.days:
			# pi = frappe.new_doc("Purchase Invoice")
			purchase = frappe.db.sql("""select distinct(supplier) as name 
											from `tabPurchase Receipt` 
											where docstatus =1 and posting_date BETWEEN '{0}' and '{1}'
											""".format(p_inv.previous_sync_date,getdate(today())), as_dict =True)
					
			for i in purchase:
				
				me = frappe.db.sql("""select milk_entry , status , supplier
											from `tabPurchase Receipt` 
											where docstatus= 1 and supplier = '{0}' and posting_date BETWEEN '{1}' and '{2}' and per_billed<100 and milk_entry is not null
											""".format(i.name,p_inv.previous_sync_date,getdate(today())), as_dict =True)
				if me:
					pi = frappe.new_doc("Purchase Invoice")
					print('meeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',me)
					for m in me:
						if m.milk_entry:
							milk = frappe.get_doc('Milk Entry',m.milk_entry)
							ware = frappe.get_doc('Warehouse',{'name':milk.dcs_id})

							pr =  frappe.db.get_value('Purchase Receipt',{'milk_entry':milk.name,"docstatus":1},['name'])
							if pr:
								pri =  frappe.get_doc('Purchase Receipt',pr)

							# if pr:
								# pur_inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':pr},["parent"])
								# print('pur_inv***************************************',pur_inv)
								# inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':pr},["pr_detail"])
								# print('inv^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',inv)
								# if not inv:
								
								# pi = frappe.new_doc("Purchase Invoice")
								pi.supplier = milk.member
								pi.milk_entry = milk.name
								for itm in pri.items:
									# pi.supplier = milk.member if  ware.is_third_party_dcs == 0 else ware.supplier
									pi.append(
										"items",
										{
											'item_code': itm.item_code,
											'item_name': itm.item_name,
											'description': itm.description,
											'received_qty': milk.volume,
											'qty': milk.volume,
											'uom': itm.stock_uom,
											'stock_uom': itm.stock_uom,
											'rate': itm.rate,
											'warehouse': milk.dcs_id,
											'purchase_receipt':pr,
											'pr_detail':itm.name
										}
									)
					pi.save(ignore_permissions = True)
					pi.submit()
					if (pi.docstatus == 1):
						milk.db_set('status','Billed')
					frappe.db.commit()
			p_inv.db_set('previous_sync_date',getdate(today()))




		if p_inv.default_payment_type == 'Weekly':
			delta=getdate(date.today()) - getdate(p_inv.previous_sync_date)
			
			if delta.days >= 7:
				# d2 = getdate(date.today())

				purchase = frappe.db.sql("""select distinct(supplier) as name 
											from `tabPurchase Receipt` 
											where docstatus =1 and posting_date BETWEEN '{0}' and '{1}'
											""".format(p_inv.previous_sync_date,getdate(today())), as_dict =True)
					
			for i in purchase:
				
				me = frappe.db.sql("""select milk_entry , status , supplier
											from `tabPurchase Receipt` 
											where docstatus= 1 and supplier = '{0}' and posting_date BETWEEN '{1}' and '{2}' and per_billed<100
											""".format(i.name,p_inv.previous_sync_date,getdate(today())), as_dict =True)
				if me:
					pi = frappe.new_doc("Purchase Invoice")
					print('meeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',me)
					for m in me:
						milk = frappe.get_doc('Milk Entry',m.milk_entry)
						ware = frappe.get_doc('Warehouse',{'name':milk.dcs_id})

						pr =  frappe.db.get_value('Purchase Receipt',{'milk_entry':milk.name,"docstatus":1},['name'])
						if pr:
							pri =  frappe.get_doc('Purchase Receipt',pr)

						# if pr:
							# pur_inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':pr},["parent"])
							# print('pur_inv***************************************',pur_inv)
							# inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':pr},["pr_detail"])
							# print('inv^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',inv)
							# if not inv:
							
							# pi = frappe.new_doc("Purchase Invoice")
							pi.supplier = milk.member
							pi.milk_entry = milk.name
							for itm in pri.items:
								# pi.supplier = milk.member if  ware.is_third_party_dcs == 0 else ware.supplier
								pi.append(
									"items",
									{
										'item_code': itm.item_code,
										'item_name': itm.item_name,
										'description': itm.description,
										'received_qty': milk.volume,
										'qty': milk.volume,
										'uom': itm.stock_uom,
										'stock_uom': itm.stock_uom,
										'rate': itm.rate,
										'warehouse': milk.dcs_id,
										'purchase_receipt':pr,
										'pr_detail':itm.name
									}
								)
					pi.save(ignore_permissions = True)
					pi.submit()
					if (pi.docstatus == 1):
						milk.db_set('status','Billed')
			p_inv.db_set('previous_sync_date',getdate(today()))

