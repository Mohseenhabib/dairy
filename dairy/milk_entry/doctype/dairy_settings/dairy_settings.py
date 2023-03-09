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
	pass

@frappe.whitelist()
def purchase_invoice():
	tdate = str(date.today())
	p_inv = frappe.get_doc('Dairy Settings')
	if p_inv.default_payment_type == 'Daily':
		ware = frappe.get_all('Warehouse',{'is_dcs':1},['supplier','name','is_third_party_dcs'])
		

		for wh in ware:
			query =frappe.db.sql("""select dcs_id,member,milk_type,name,volume
										from `tabMilk Entry` 
										where docstatus =1  and dcs_id = '{0}' and date = '{1}' 
										""".format(wh.name,tdate), as_dict =True)

			

			
			for k in query:
				print('query^^^^^^^^^^^^^^^^^^^^^^^^^',k.name)
				pr =  frappe.db.get_all('Purchase Receipt',{'milk_entry':k.name,"docstatus":1},['*'])
				
				for j in pr:
					pr =  frappe.get_doc('Purchase Receipt',j.name)
					pur_inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':j.name},["parent"])
					if not pur_inv:
						
						pi = frappe.new_doc("Purchase Invoice")
						for itm in pr.items:
							pi.supplier = k.get('member') if  wh.is_third_party_dcs == 0 else wh.get("supplier")
							pi.name = k.get('name')
							pi.append(
								"items",
								{
									'item_code': itm.item_code,
									'item_name': itm.item_name,
									'description': itm.description,
									'received_qty': k.volume,
									'qty': k.volume,
									'uom': itm.stock_uom,
									'stock_uom': itm.stock_uom,
									'rate': itm.rate,
									'warehouse': k.dcs_id,
									'purchase_receipt':j.name
								}
							)
						pi.save(ignore_permissions = True)
						pi.submit()
						if (pi.docstatus == 1):
							k.db_set('status','Billed')



	if p_inv.default_payment_type == 'Days':
		
		delta=getdate(date.today()) - getdate(p_inv.previous_sync_date)
		
		if delta.days >= p_inv.days:

			d2 = getdate(date.today())
			
			ware = frappe.get_all('Warehouse',{'is_dcs':1},['supplier','name','is_third_party_dcs'])
			
			for wh in ware:
				query =frappe.db.sql("""select dcs_id,member,milk_type,name,volume,date
											from `tabMilk Entry` 
											where docstatus =1 and dcs_id = '{0}' and date BETWEEN  '{1}' and '{2}'
											""".format(wh.name,p_inv.previous_sync_date,d2), as_dict =True)

				
			
			
			
				for k in query:
					
					pr =  frappe.db.get_all('Purchase Receipt',{'milk_entry':k.name,"docstatus":1},['*'])
					
					for j in pr:
						pr =  frappe.get_doc('Purchase Receipt',j.name)

						
						pur_inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':j.name,"docstatus":1},["parent"])
						print('pur inv in days$$$$$$$$$$$$$$$',pur_inv )
						if not pur_inv:
							
							pi = frappe.new_doc("Purchase Invoice")
							
							for itm in pr.items:
								
								pi.supplier = k.get('member') if  wh.is_third_party_dcs == 0 else wh.get("supplier")
								pi.name = k.get('name')
								pi.append(
									"items",
									{
										'item_code': itm.item_code,
										'item_name': itm.item_name,
										'description': itm.description,
										'received_qty': k.volume,
										'qty': k.volume,
										'uom': itm.stock_uom,
										'stock_uom': itm.stock_uom,
										'rate': itm.rate,
										'warehouse': k.dcs_id,
										'purchase_receipt': j.name
									}
								)

							pi.save(ignore_permissions = True)
							pi.submit()
							if (pi.docstatus == 1):
								k.db_set('status','Billed')
							p_inv.db_set('previous_sync_date',str(date.today()))




	if p_inv.default_payment_type == 'Weekly':
		delta=getdate(date.today()) - getdate(p_inv.previous_sync_date)
		
		if delta.days >= 7:
			d2 = getdate(date.today())

			ware = frappe.get_all('Warehouse',{'is_dcs':1},['supplier','name','is_third_party_dcs'])
			

			for wh in ware:
				query =frappe.db.sql("""select dcs_id,member,milk_type,name,volume,date
											from `tabMilk Entry` 
											where docstatus =1 and dcs_id = '{0}' and date BETWEEN  '{1}' and '{2}'
											""".format(wh.name,p_inv.previous_sync_date,d2), as_dict =True)

				
			
			
			
				for k in query:
					
					pr =  frappe.db.get_all('Purchase Receipt',{'milk_entry':k.name,"docstatus":1},['*'])
					for j in pr:
						pr =  frappe.get_doc('Purchase Receipt',j.name)
					
						pur_inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':j.name},["parent"])
						if not pur_inv:
							pi = frappe.new_doc("Purchase Invoice")
							for itm in pr.items:
								pi.supplier = k.get('member') if  wh.is_third_party_dcs == 0 else wh.get("supplier")
								pi.name = k.get('name')
								pi.append(
									"items",
									{
										'item_code': itm.item_code,
										'item_name': itm.item_name,
										'description': itm.description,
										'received_qty': k.volume,
										'qty': k.volume,
										'uom': itm.stock_uom,
										'stock_uom': itm.stock_uom,
										'rate': itm.rate,
										'warehouse': k.dcs_id,
										'purchase_receipt': j.name
									}
								)

							pi.save(ignore_permissions = True)
							pi.submit()
							if (pi.docstatus == 1):
								k.db_set('status','Billed')
							p_inv.db_set('previous_sync_date',str(date.today()))