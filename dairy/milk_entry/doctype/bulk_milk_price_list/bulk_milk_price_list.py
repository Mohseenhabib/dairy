# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BulkMilkPriceList(Document):
	pass

@frappe.whitelist()
def fetch_data(doctype, customer):
	all_doc = frappe.db.get_all(doctype,fields=['*'],filters = {"docstatus" :1})
	for doc in all_doc:
		query = """ select customer from `tabBulk Milk Price List Customer` where parent = '{0}'""".format(doc.get("name"))
		customer_name = frappe.db.sql(query, as_dict = True)
		if(customer == customer_name[0].get("customer")):
			return {
				'rate': doc.get("rate"),
				'snf' : doc.get('snf_clr_rate')
			}