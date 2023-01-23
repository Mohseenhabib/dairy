# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dexciss Technology by Sid and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date

class DairySettings(Document):
	pass

@frappe.whitelist()
def purchase_invoice():
	tdate = date.today()
	doc = frappe.db.get_all('Milk Entry',{'date':tdate,'docstatus':1},['name','member','volume'])
	p_inv = frappe.get_doc('Dairy Settings')
	if p_inv.default_payment_type == 'Daily':
		ware = frappe.get_all('Warehouse',{'is_dcs':1},['supplier','name','is_third_party_dcs'])
		for wh in ware:
			for k in doc:
				item = frappe.get_all('Item',{'milk_type':k.milk_type},['*'])
				pr =  frappe.get_all('Purchase Receipt',{'milk_entry':k.name},['*'])
				for j in pr:
					pi = frappe.new_doc("Purchase Invoice")
					for itm in item:
						pi.supplier = wh.get('supplier') if  wh.is_third_party_dcs == 1 else k.get("member")
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
								# 'warehouse': self.dcs_id,
								# 'fat': self.fat_kg,
								# 'clr': self.snf_kg
							}
						)

					pi.save(ignore_permissions= True)
							
				
