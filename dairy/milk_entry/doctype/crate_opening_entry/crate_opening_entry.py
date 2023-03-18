# Copyright (c) 2023, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CrateOpeningEntry(Document):
	@frappe.whitelist()
	def make_log(self,sales):

		if frappe.db.get_single_value("Dairy Settings", "crate_reconciliation_based_on") == "Gate Pass":
			dist_cratetype = frappe.db.sql(""" select distinct(crate_type) 
												from `tabMerge Gate Pass Item` 
												where parent = %(name)s""",{'name':self.name})
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
					log.shift = sales.shift
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
														and company = %(company)s and docstatus = 1 and vehicle = %(vehicle)s	
														and transporter = %(transporter)s and shift = %(shift)s order by date desc """,
												 		{'crate': crate, 'warehouse': warehouse,'company': sales.company,
														 'vehicle':sales.vehicle,'transporter':sales.transporter, 'shift':sales.shift}, as_dict=1)
					if openning_cnt[0]['count(*)'] > 0:

						openning = frappe.db.sql(""" select crate_balance from `tabCrate Log`  
													where 
													crate_type = %(crate)s and source_warehouse = %(warehouse)s and
													company = %(company)s and  docstatus = 1 and vehicle = %(vehicle)s
													and transporter = %(transporter)s and shift = %(shift)s order by date desc limit 1 """,
												 	{'crate':crate,'warehouse':warehouse,'company':sales.company,
													 'vehicle':sales.vehicle,'transporter':sales.transporter, 'shift':sales.shift},as_dict=1)

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

