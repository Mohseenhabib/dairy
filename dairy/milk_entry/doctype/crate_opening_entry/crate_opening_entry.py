# Copyright (c) 2023, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CrateOpeningEntry(Document):
	@frappe.whitelist()
	def make_crate_log(self):

		if frappe.db.get_single_value("Dairy Settings", "crate_reconciliation_based_on") == "Gate Pass":
			for crate in self.party_crate_opening:

				log = frappe.new_doc("Crate Log")
				customer_route = frappe.get_doc('Customer',{'customer_name':crate.customer})
				print('customer&&&&&&&&&&&&&&&&&&&&&',customer_route)
				for j in customer_route.links:
					doc=frappe.get_doc("Route Master",j.link_name)
					print('customer route&&&&&&&&&&&&&&&&&&&&&7',doc)
					route = frappe.get_all('Route Master',{'name':j.link_name},['*'])
					for k in route:
						print('route^^^^^^^^^^^^^^^^^^',k)
						log.transporter = k.transporter
						log.vehicle = k.vehicle
						log.route = doc.name
						# log.shift = self.shift
						log.date = frappe.utils.nowdate()
						log.company = self.company
						# log.voucher_type = "Crate Opening Entry"
						# log.voucher = self.name
						# log.damaged = sums[0]['damaged_crate']
						# log.crate_issue = sums[0]['crate']
						# log.crate_return = sums[0]['crate_ret']
						log.crate_type = crate.crate_type
						log.source_warehouse = k.source_warehouse
						# log.note = "Entry Created From Gate pass"
						openning_cnt = frappe.db.sql(""" select count(*) from `tabCrate Log`  
														where company = %(company)s and docstatus = 1 	
															order by date desc """,
															{'company': self.company}, as_dict=1)
						if openning_cnt[0]['count(*)'] > 0:

							openning = frappe.db.sql(""" select crate_balance from `tabCrate Log`  
														where
														company = %(company)s and  docstatus = 1 order by date desc limit 1 """,
														{'company':self.company},as_dict=1)

						# 	log.crate_opening = int(openning[0]['crate_balance'])
						# 	log.crate_balance = openning[0]['crate_balance'] - (sums[0]['crate'] + sums[0]['crate_ret'])
						# 	self.append("crate_summary", {
						# 		"crate_opening": openning[0]['crate_balance'] - (sums[0]['crate'] + sums[0]['crate_ret']),
						# 		"crate_issue": sums[0]['crate'],
						# 		"crate_return": sums[0]['crate_ret'],
						# 		"crate_balance": openning[0]['crate_balance'] - (sums[0]['crate'] + sums[0]['crate_ret'])
						# 	})

						# else:
						# 	log.crate_opening = int(0)
						# 	log.crate_balance = int(0) - (sums[0]['crate'] + sums[0]['crate_ret'])
						# 	self.append("crate_summary", {
						# 		"crate_opening": int(0) - (sums[0]['crate'] + sums[0]['crate_ret']),
						# 		"crate_issue": sums[0]['crate'],
						# 		"crate_return": sums[0]['crate_ret'],
						# 		"crate_balance": int(0) - (sums[0]['crate'] + sums[0]['crate_ret'])
						# 	})
						log.save()
						log.submit()

