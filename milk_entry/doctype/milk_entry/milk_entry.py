# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import frappe
from frappe import _
from datetime import datetime
from frappe.model.mapper import get_mapped_doc

class MilkEntry(Document):

    # def on_update(self):
    #     if not self.dcs_id:
    #         if self.quick_dcs:
    #
    #             frappe.db.set(self, 'dcs_id',self.quick_dcs)
    #             frappe.db.set(self, 'member', self.quick_member)
    #             frappe.db.set(self, 'milk_type', self.quick_milk_type)
    #             frappe.db.set(self, 'volume', self.quick_vol)
    #             frappe.db.set(self, 'fat', self.quick_fat)
    #             frappe.db.set(self, 'clr', self.quick_clr)



    def get_pricelist(self):
        pricelist_name = frappe.db.sql("""
					select milk_rate.name from `tabMilk Rate` as milk_rate 
					inner join `tabWarehouse Child` as ware on ware.parent = milk_rate.name 
					where milk_rate.milk_type = '{0}' and ware.warehouse_id = '{1}' 
					and milk_rate.docstatus = 1 and milk_rate.effective_date <= '{2}' limit 1  """.format(self.milk_type,self.dcs_id,self.date))
        if not pricelist_name:
            frappe.throw(_("Pricelist not found."))
			
        frappe.db.set(self,'milk_rate', pricelist_name[0][0])
        print("======self==pricelist_name",self.milk_rate)
        rate =  frappe.db.sql(""" select rate from `tabMilk Rate Chart` where fat >= {0} and snf_clr >= {1} 
					and parent = '{2}' order by fat,snf_clr asc limit 1 """.format(self.fat,self.clr,pricelist_name[0][0]))
		
        frappe.db.set(self, 'unit_price', rate[0][0])
        frappe.db.set(self, 'total',(self.volume *self.unit_price))


@frappe.whitelist()
def create_raw_sample(source_name, target_doc=None):
    print("==source_name==",source_name,"=target_doc=",target_doc)

    def update_item(obj, target, source_parent):
        print("====obj",obj.sample_created,"===target",target)
        obj.sample_created = True

        # frappe.throw(_("Pricelist not found."))
        # print("===source_parent",source_parent)
        nameing_series = frappe.db.sql(""" select options from `tabDocField` where fieldname='naming_series' and parent='Sample lines' """)

        target.append('sample_lines', {
            'naming_series':nameing_series[0][0],
            'milk_entry': obj.name,
            'member_id': obj.member,
            'milk_type': obj.milk_type,
            'fat': obj.fat,
            'clr': obj.clr})

    fields = {
        "Milk Entry": {
            "doctype": "Sample lines"
        },
        "Milk Entry": {
            "doctype": "Raw Milk Sample",
            "field_map": {
                "name": "raw_milk_sample",
            },
            "postprocess": update_item,
        },
    }

	# def postprocess(source, doc):
	# 	print("=====source",source,"====doc",doc)



	# def set_missing_values(source, target):
	# 	print("=======target",target,"====source",source)
	# 	target.dcs_id = source.dcs_id
	# 	target.date	 = source.date
	# 	source.sample_created = True
	# 	frappe.throw(_("Purchase Receipt already Created."))
	# 	print("=====created",target.sample_created)
		# target.milk_entry =

    doclist = get_mapped_doc("Milk Entry", source_name,fields,	{
    }, target_doc)

    return doclist

def _get_product(milk_type):
    if milk_type=='Cow':
        item_code = frappe.db.get_single_value("Dairy Settings", "cow_pro")
    elif milk_type=='Buffalow':
        item_code = frappe.db.get_single_value("Dairy Settings", "buf_pro")
    elif milk_type == 'Mix':
        item_code = frappe.db.get_single_value("Dairy Settings", "mix_pro")

    # print("=====item_code",item_code)
    item = frappe.get_doc('Item', item_code)
    return item



@frappe.whitelist()
def create_purchase_receipt(source_name, target_doc=None):
    print("===src",source_name,"====target_doc",target_doc)

    purchase_receipts = frappe.db.sql("""
                select count(name) from `tabPurchase Receipt` where status not in ('Cancelled') and milk_entry= '{0}' """.format(source_name))[0][0]

    if purchase_receipts >= 1:
        frappe.throw(_("Purchase Receipt already Created."))

    src = frappe.get_doc('Milk Entry', source_name)
    warehouse = frappe.get_doc('Warehouse',src.dcs_id)
    item_code = _get_product(src.milk_type)

    doc = frappe.new_doc('Purchase Receipt')
    doc.supplier = src.member
    doc.posting_date = src.date
    doc.posting_time = src.time
    doc.company = warehouse.company
    doc.milk_entry = source_name

    doc.append('items', {
        'item_code': item_code.item_code,
        'item_name':item_code.item_name,
        'description':item_code.description,
        'received_qty':src.volume,
        'qty':src.volume,
        'uom':item_code.stock_uom,
        'stock_uom': item_code.stock_uom,
        'rate':src.unit_price,
        'warehouse':src.dcs_id,
        'fat':src.fat,
        'clr':src.clr
    })
    print("=======doc",doc,"====src",src)
    doc.save()
    doc.submit()
    src.db_set('status', "To Bill")
    frappe.db.set(src,'purchase_receipt',doc.name)
    # src.reload()




@frappe.whitelist()
def create_purchase_invoice(source_name, target_doc=None):
    def update_item(obj, target, source_parent):
        target.supplier = obj.member
        item_code = _get_product(obj.milk_type)
        target.append('items', {
            'item_code': item_code.item_code,
            'item_name':item_code.item_name,
            'description': item_code.description,
            'uom':item_code.stock_uom,
            'stock_uom': item_code.stock_uom,
            'rate': obj.unit_price,
            'qty':obj.volume
        })

    fields = {
        "Milk Entry": {
            "doctype": "Purchase Invoice Item",
        },
        "Milk Entry": {
            "doctype": "Purchase Invoice",
            "field_map": {
                "name": "purchase_invoice",
            },
            "postprocess": update_item,
        },
    }


    doclist = get_mapped_doc("Milk Entry", source_name, fields, {
    }, target_doc)

    return doclist



@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None):

    def set_missing_values(source, target):
        print("===target",target.dcs_id)
        dcs_id = frappe.get_doc('Warehouse', source.dcs_id)
        if dcs_id.sample_collector == False:
            frappe.throw(_("The given DCS is not setup to collect farmer-specific samples."))

        if source.dcs_id == target.dcs_id:

            if dcs_id.sample_collector == True:

                target.sample_created = True

                target.append('sample_lines', {
                    'member_id': source.member,
                    'milk_type': source.milk_type,
                    'fat': source.fat,
                    'clr': source.clr,
                    'milk_entry':source.name
                })


    doclist = get_mapped_doc("Milk Entry", source_name,	{
        "Milk Entry": {
            "doctype": "Sample lines",
        }
    }, target_doc, set_missing_values)

    return doclist



# @frappe.whitelist()
# def create_new_member(source_name, target_doc=None):
#     def set_missing_values(source, target):
#         print("=====sou")
#
#     doclist = get_mapped_doc("Milk Entry", source_name, {
#         "Milk Entry": {
#             "doctype": "",
#         }
#     }, target_doc, set_missing_values)
#     return doclist

# @frappe.whitelist()
# def filters_to_quick_entry():
# 	print("====test sid")