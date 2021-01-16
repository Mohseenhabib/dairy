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
    def get_pricelist(self):
        pricelist_name = frappe.db.sql("""
                    select milk_rate.name from `tabMilk Rate` as milk_rate 
                    inner join `tabWarehouse Child` as ware on ware.parent = milk_rate.name 
                    where milk_rate.milk_type = '{0}' and ware.warehouse_id = '{1}' 
                    and milk_rate.docstatus = 1 and milk_rate.effective_date <= '{2}' limit 1  """.format(self.milk_type,self.dcs_id,self.date))
        if not pricelist_name:
            frappe.throw(_("Milk Rate not found."))

        frappe.db.set(self,'milk_rate', pricelist_name[0][0])
        rate = frappe.db.sql(""" select rate from `tabMilk Rate Chart` where fat >= {0} and snf_clr >= {1} 
                    and parent = '{2}' order by fat,snf_clr asc limit 1 """.format(self.fat,self.clr,pricelist_name[0][0]))
        if not rate:
            frappe.throw(_("Milk price not found."))
        frappe.db.set(self, 'unit_price', rate[0][0])
        frappe.db.set(self, 'total',(self.volume *self.unit_price))
        frappe.db.set(self, 'status','Submitted')

        fat_kg = (self.volume * self.fat)/100
        frappe.db.set(self, 'fat_kg', fat_kg)

        snf_kg = self.clr/4 + 0.21*(self.fat/100) + 0.36
        frappe.db.set(self, 'snf_kg', snf_kg)

    def create_purchase_receipt(self):
        purchase_receipts = frappe.db.sql("""select count(name) from `tabPurchase Receipt` 
                                            where status not in ('Cancelled') and milk_entry= %s""",(self.name))[0][0]

        if purchase_receipts >= 1:
            frappe.throw(_("Purchase Receipt already Created."))

        warehouse = frappe.get_doc('Warehouse', self.dcs_id)
        item_code = _get_product(self.milk_type)

        doc = frappe.new_doc('Purchase Receipt')
        doc.supplier = self.member

        if warehouse.is_dcs and warehouse.is_third_party_dcs:
            doc.supplier = warehouse.supplier

        doc.posting_date = self.date
        doc.posting_time = self.time
        doc.company = warehouse.company
        doc.milk_entry = self.name

        doc.append('items', {
            'item_code': item_code.item_code,
            'item_name': item_code.item_name,
            'description': item_code.description,
            'received_qty': self.volume,
            'qty': self.volume,
            'uom': item_code.stock_uom,
            'stock_uom': item_code.stock_uom,
            'rate': self.unit_price,
            'warehouse': self.dcs_id,
            'fat': self.fat_kg,
            'clr': self.snf_kg
        })
        doc.insert(ignore_permissions=True)
        # doc.submit()
        return doc

def _get_product(milk_type):
    if milk_type == 'Cow':
        item_code = frappe.db.get_single_value("Dairy Settings", "cow_pro")
    elif milk_type == 'Buffalow':
        item_code = frappe.db.get_single_value("Dairy Settings", "buf_pro")
    elif milk_type == 'Mix':
        item_code = frappe.db.get_single_value("Dairy Settings", "mix_pro")

    item = frappe.get_doc('Item', item_code)
    return item

@frappe.whitelist()
def create_raw_sample(source_name, target_doc=None):
    def update_item(obj, target, source_parent):
        obj.sample_created = True
        nameing_series = frappe.db.sql(""" select options from `tabDocField` where fieldname='naming_series' and parent='Sample lines' """)
        target.append('sample_lines', {
            'naming_series':nameing_series[0][0],
            'milk_entry': obj.name,
            'member_id': obj.member,
            'milk_type': obj.milk_type,
            'fat': obj.fat_kg,
            'clr': obj.snf_kg})

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
    doclist = get_mapped_doc("Milk Entry", source_name,fields,	{
    }, target_doc)

    return doclist

@frappe.whitelist()
def make_sample(source_name, target_doc=None):
    def set_missing_values(source, target):
        dcs_id = frappe.get_doc('Warehouse', source.dcs_id)
        if dcs_id.sample_collector == False:
            frappe.throw(_("The given DCS is not setup to collect farmer-specific samples."))
        nameing_series = frappe.db.sql(""" select options from `tabDocField` where fieldname='naming_series' and parent='Sample lines' """)

        if source.dcs_id == target.dcs_id:
            if dcs_id.sample_collector == True:
                target.sample_created = True
                target.append('sample_lines', {
                    'member_id': source.member,
                    'milk_type': source.milk_type,
                    'fat': source.fat,
                    'clr': source.clr,
                    'milk_entry':source.name,
                    'naming_series': nameing_series[0][0],
                })

    doclist = get_mapped_doc("Milk Entry", source_name,	{
        "Milk Entry": {
            "doctype": "Sample lines",
        }
    }, target_doc, set_missing_values)

    return doclist

