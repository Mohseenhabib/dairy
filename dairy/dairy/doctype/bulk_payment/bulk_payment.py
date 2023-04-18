# Copyright (c) 2023, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import csv
import io
import random

import frappe
import json

class BulkPayment(Document):
	@frappe.whitelist()
	def get_data(self):
		filters={}
		if self.from_date:
			filters.update({"posting_date":[">=",self.from_date]})
		if self.to_date:
			filters.update({"posting_date":["<=",self.to_date]})
		if self.mode_of_payment:
			filters.update({"mode_of_payment":self.mode_of_payment})
		if self.party_type:
			filters.update({"party_type":self.party_type})
		filters.update({"docstatus":1})
		f =frappe.get_all('Payment Entry',filters,["*"])
		self.items=[]
		for d in f:
			ifsc = frappe.get_value("Bank Account",{"bank_account_no":d.bank_account_no},["branch_code"])

			self.append("items",{
				"bank_account_no":d.bank_account_no,
				"paid_amount":d.paid_amount,
				"party_name":d.party_name,
				"posting_date":d.posting_date,
				"ifsc":ifsc,
				"bank":d.bank
			})
	@frappe.whitelist()
	def get_lines(self):
		a = 0
		l =[]
		for d in self.items:
			ifsc = frappe.get_value("Bank Account",{"bank_account_no":d.bank_account_no},["branch_code"])

			a = a+1
			x =[]
		
			x.append("N")
			x.append("           ")
			x.append(d.bank_account_no)
			x.append(d.paid_amount)
			x.append(d.party_name)
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append(str(d.posting_date) + "-"+ str("{:03d}".format(a)))
			x.append(str(d.posting_date) + "-"+ str("{:03d}".format(a)))
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append("           ")
			x.append(d.posting_date)
			x.append("           ")
			x.append(d.ifsc)
			x.append(d.bank)
			x.append("           ")
			x.append(frappe.session.user)
			l.append(x)


		doc=frappe.get_doc("Dairy Settings")
		path = doc.file_path_download_csv
		# ran = random.randint(0,9999999999)
		full_name = path + str(self.name) +".csv"


		with open(full_name, 'w') as file:
			field = ["name", "creation"]
			writer = csv.writer(file)
			# writer.writerow(field)
			for row in  l:
				writer.writerow(row)

    

@frappe.whitelist()
def get_download(name):
	doc=frappe.get_doc("Dairy Settings")
	with open(str(doc.file_path_download_csv)+str(name)+".csv",'rb') as f:
		file=f.read()
		frappe.local.response.filename = str(name)+".csv"
		frappe.local.response.filecontent = file
		frappe.local.response.type = "download"
		

            







    


























































