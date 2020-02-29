# from __future__ import unicode_literals
# import frappe
# import json
# import copy
# from frappe import throw, _
# from frappe.utils import flt, cint, getdate

# from frappe.model.document import Document

# from six import string_types

# @frappe.whitelist()
# def apply_pricing_rule(args, doc=None):
# 	"""
# 		args = {
# 			"items": [{"doctype": "", "name": "", "item_code": "", "brand": "", "item_group": ""}, ...],
# 			"customer": "something",
# 			"customer_group": "something",
# 			"territory": "something",
# 			"supplier": "something",
# 			"supplier_group": "something",
#             "address": "something",
# 			"currency": "something",
# 			"conversion_rate": "something",
# 			"price_list": "something",
# 			"plc_conversion_rate": "something",
# 			"company": "something",
# 			"transaction_date": "something",
# 			"campaign": "something",
# 			"sales_partner": "something",
# 			"ignore_pricing_rule": "something"
# 		}
# 	"""
#     if