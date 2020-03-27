# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class VanCollection(Document):
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
                    van_collection.van_collection = self.name
                    van_collection.insert(ignore_permissions = True)

            frappe.db.set(self, 'status', 'In-Progress')
            self.flags.ignore_validate_update_after_submit = True  # ignore after submit permission
            self.save(ignore_permissions=True)
        return True

    def make_stock_entry(self):
        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.purpose = "Material Transfer"
        stock_entry.stock_entry_type = "Material Transfer"
        stock_entry.company = self.company
        stock_entry.van_collection = self.name

        route = frappe.get_doc("Route Master",self.route)
        coll_items = frappe.db.get_all("Van Collection Items", {"van_collection": self.name})

        cost_center = frappe.get_cached_value('Company', self.company, 'cost_center')
        perpetual_inventory = frappe.get_cached_value('Company', self.company, 'enable_perpetual_inventory')
        expense_account = frappe.get_cached_value('Company', self.company, 'stock_adjustment_account')

        cow_item = frappe.db.get_single_value("Dairy Settings", "cow_pro")
        buf_item = frappe.db.get_single_value("Dairy Settings", "buf_pro")
        mix_item = frappe.db.get_single_value("Dairy Settings", "mix_pro")

        for res in coll_items:
            doc = frappe.get_doc("Van Collection Items",res.name)
            if doc.cow_milk_collected > 0:
                item = frappe.get_doc("Item",cow_item)
                se_child = stock_entry.append('items')
                se_child.item_code = item.item_code
                se_child.item_name = item.item_name
                se_child.uom = item.stock_uom
                se_child.stock_uom = item.stock_uom
                se_child.qty = doc.cow_milk_collected
                se_child.s_warehouse = doc.dcs
                se_child.t_warehouse = route.dest_warehouse
                # in stock uom
                se_child.transfer_qty = doc.cow_milk_collected
                se_child.cost_center = cost_center
                se_child.expense_account = expense_account if perpetual_inventory else None

            if doc.buffalow_milk_collected > 0:
                item = frappe.get_doc("Item",buf_item)
                se_child = stock_entry.append('items')
                se_child.item_code = item.item_code
                se_child.item_name = item.item_name
                se_child.uom = item.stock_uom
                se_child.stock_uom = item.stock_uom
                se_child.qty = doc.buffalow_milk_collected
                se_child.s_warehouse = doc.dcs
                se_child.t_warehouse = route.dest_warehouse
                # in stock uom
                se_child.transfer_qty = doc.buffalow_milk_collected
                se_child.cost_center = cost_center
                se_child.expense_account = expense_account if perpetual_inventory else None

            if doc.mix_milk_collected > 0:
                item = frappe.get_doc("Item",mix_item)
                se_child = stock_entry.append('items')
                se_child.item_code = item.item_code
                se_child.item_name = item.item_name
                se_child.uom = item.stock_uom
                se_child.stock_uom = item.stock_uom
                se_child.qty = doc.mix_milk_collected
                se_child.s_warehouse = doc.dcs
                se_child.t_warehouse = route.dest_warehouse
                # in stock uom
                se_child.transfer_qty = doc.mix_milk_collected
                se_child.cost_center = cost_center
                se_child.expense_account = expense_account if perpetual_inventory else None

        return stock_entry

#---------------------stock entry method---------------

def change_van_collection_status(st,method):
    if st.van_collection:
        doc = frappe.get_doc("Van Collection", st.van_collection)
        doc.status ="Completed"
        doc.db_update()