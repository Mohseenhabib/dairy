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
		query =frappe.db.sql("""select dcs_id,member,milk_type,name,volume
                                    from `tabMilk Entry` 
                                    where docstatus =1 and date = %s 
                                    """,(tdate), as_dict =True)

		ware = frappe.get_all('Warehouse',{'is_dcs':1},['supplier','name','is_third_party_dcs'])
		for wh in ware:
			for k in query:
				if k.get("milk_type")=="Cow":
					item = frappe.db.get_all('Item',{"name":p_inv.cow_pro},['*'])
				if k.get("milk_type")=="Buffalo":
					item = frappe.db.get_all('Item',{"name":p_inv.buf_pro},['*'])
				if k.get("milk_type")=="Mix":
					item = frappe.db.get_all('Item',{"name":p_inv.mix_pro},['*'])
				
				pr =  frappe.db.get_all('Purchase Receipt',{'milk_entry':k.name},['*'])
				
				for j in pr:
					pur_inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':j.name},["parent"])
					if not pur_inv:
						pi = frappe.new_doc("Purchase Invoice")
						for itm in item:
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
									'rate': itm.unit_price,
									'warehouse': k.dcs_id,
									'purchase_receipt':j.name
								}
							)

						pi.save(ignore_permissions= True)

	if p_inv.default_payment_type == 'Days':	
		days_after = ((getdate(frappe.utils.nowdate()))-timedelta(days=p_inv.days)).isoformat() 
		p_inv.db_set('previous_sync_date',days_after)
		dt = ((getdate(days_after)) + timedelta(days=p_inv.days)).isoformat()
		dts = (date.today()) - (getdate(dt))
		print('dts*******************',getdate(dt))
		if date.today() == getdate(dt):
			print('if condition ^^^^^^^^^^^^^^^^^^^^',(date.today()))
			d1 = getdate(days_after)
			d2 = getdate(date.today())
			# d = pd.date_range(d1, d2)
			print('dddddddddddddddddddddddddddddddddd',d2,p_inv.previous_sync_date)

			query =frappe.db.sql("""select dcs_id,member,milk_type,name,volume,date
										from `tabMilk Entry` 
										where docstatus =1 and date BETWEEN  '{0}' and '{1}'
										""".format(p_inv.previous_sync_date,d2), as_dict =True)

			print('query***********************',query)
			
			ware = frappe.get_all('Warehouse',{'is_dcs':1},['supplier','name','is_third_party_dcs'])
			for wh in ware:
				for k in query:
					if k.get("milk_type")=="Cow":
						item = frappe.db.get_all('Purchase Invoice Item',{"name":p_inv.cow_pro},['*'])
					if k.get("milk_type")=="Buffalo":
						item = frappe.db.get_all('Purchase Invoice Item',{"name":p_inv.buf_pro},['*'])
					if k.get("milk_type")=="Mix":
						item = frappe.db.get_all('Purchase Invoice Item',{"name":p_inv.mix_pro},['*'])
					pr =  frappe.db.get_all('Purchase Receipt',{'milk_entry':k.name},['*'])
					for j in pr:
						print('jjjjjjjjjjjjjjjjjjjj',j)
						pur_inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':j.name},["parent"])
						if not pur_inv:
							pi = frappe.new_doc("Purchase Invoice")
							for itm in item:
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
										'rate': itm.unit_price,
										'warehouse': k.dcs_id,
										'fat': k.fat_kg,
										'clr': k.snf_kg,
										'purchase_receipt': j.name
									}
								)

							pi.save(ignore_permissions= True)
							p_inv.db_set('previous_sync_date',str(dt))
						
	if p_inv.default_payment_type == 'Weekly':
		days_after = ((getdate(frappe.utils.nowdate()))-timedelta(days=7)).isoformat() 
		p_inv.db_set('previous_sync_date',days_after)
		dt = ((getdate(days_after)) + timedelta(days=7)).isoformat()
		dts = (date.today()) - (getdate(dt))
		print('dts*******************',getdate(dt))
		if date.today() == getdate(dt):
			print('if condition ^^^^^^^^^^^^^^^^^^^^',(date.today()))
			d1 = getdate(days_after)
			d2 = getdate(date.today())
			# d = pd.date_range(d1, d2)
			print('dddddddddddddddddddddddddddddddddd',d2,p_inv.previous_sync_date)

			query =frappe.db.sql("""select dcs_id,member,milk_type,name,volume,date
										from `tabMilk Entry` 
										where docstatus =1 and date BETWEEN  '{0}' and '{1}'
										""".format(p_inv.previous_sync_date,d2), as_dict =True)

			print('query***********************',query)
			
			ware = frappe.get_all('Warehouse',{'is_dcs':1},['supplier','name','is_third_party_dcs'])
			for wh in ware:
				for k in query:
					if k.get("milk_type")=="Cow":
						item = frappe.db.get_all('Purchase Invoice Item',{"name":p_inv.cow_pro},['*'])
					if k.get("milk_type")=="Buffalo":
						item = frappe.db.get_all('Purchase Invoice Item',{"name":p_inv.buf_pro},['*'])
					if k.get("milk_type")=="Mix":
						item = frappe.db.get_all('Purchase Invoice Item',{"name":p_inv.mix_pro},['*'])
					pr =  frappe.db.get_all('Purchase Receipt',{'milk_entry':k.name},['*'])
					for j in pr:
						print('jjjjjjjjjjjjjjjjjjjj',j)
						pur_inv = frappe.db.get_value('Purchase Invoice Item',{'purchase_receipt':j.name},["parent"])
						if not pur_inv:
							pi = frappe.new_doc("Purchase Invoice")
							for itm in item:
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
										'rate': itm.unit_price,
										'warehouse': k.dcs_id,
										'fat': k.fat_kg,
										'clr': k.snf_kg,
										'purchase_receipt': j.name
									}
								)

							pi.save(ignore_permissions= True)
							p_inv.db_set('previous_sync_date',str(dt))