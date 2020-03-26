# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VanCollectionItems(Document):
	def calculate_milk_cans(self):
		allow_max_capacity = frappe.db.get_single_value("Dairy Settings", "max_allowed")

		if self.cow_milk_vol < self.cow_milk_collected:
			frappe.throw("Can not allow Cow Milk Collected greater then the Cow Milk Entry")

		if self.buf_milk_vol < self.buffalow_milk_collected:
			frappe.throw("Can not allow Buffalow Milk Collected greater then the Buffalow Milk Entry")

		if self.mix_milk_vol < self.mix_milk_collected:
			frappe.throw("Can not allow Mix Milk Collected greater then the Mix Milk Entry")

		if allow_max_capacity > 0:
			self.cow_milk_cans = self.cow_milk_collected / allow_max_capacity
			self.buf_milk_cans = self.buffalow_milk_collected / allow_max_capacity
			self.mix_milk_cans = self.mix_milk_collected / allow_max_capacity
			self.db_update()
		return True
