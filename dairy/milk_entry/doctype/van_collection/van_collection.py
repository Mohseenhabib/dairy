# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today


class VanCollection(Document):
	pass

	def submit_van_collection(self):
		frappe.db.set(self,'status','Submitted')

	def van_start_collection(self):
		if self:
			warehouse = frappe.db.get_all("Warehouse",{
											"route": self.route,
											"is_dcs": 1
										})
			if not warehouse:
				frappe.throw(_("No Warehouse present in this Route"))
			for res in warehouse:
				result = frappe.db.sql("""select dcs_id,milk_type,sum(volume) as total_volume from `tabMilk Entry` 
									where docstatus =1 and dcs_id = %s and shift = %s and date = %s 
									group by milk_type""",(res.name,self.shift,self.date), as_dict =True)

				cow_volume = 0.0
				buffalow_volume = 0.0
				mix_volume = 0.0
				for i in result:
					if i.get('milk_type') == 'Cow':
						cow_volume =i.get('total_volume')

					if i.get('milk_type') == 'Buffalow':
						buffalow_volume =i.get('total_volume')

					if i.get('milk_type') == 'Mix':
						mix_volume =i.get('total_volume')
				if cow_volume > 0 or buffalow_volume > 0 or mix_volume > 0:
					van_collection = frappe.new_doc("Van Collection Items")
					van_collection.dcs = res.name
					van_collection.cow_milk_vol = cow_volume
					van_collection.buf_milk_vol = buffalow_volume
					van_collection.mix_milk_vol = mix_volume
					van_collection.insert(ignore_permissions = True)

		return True
	