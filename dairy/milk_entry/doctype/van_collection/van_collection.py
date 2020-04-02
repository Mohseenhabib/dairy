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

    def change_status_complete(self):
        frappe.db.set(self, 'status', 'Completed')
        self.flags.ignore_validate_update_after_submit = True  # ignore after submit permission
        self.save(ignore_permissions=True)

    def van_start_collection(self):
        if self:
            warehouse = frappe.db.get_all("Warehouse",{
                                            "route": self.route,
                                            "is_dcs": 1
                                        })
            if not warehouse:
                frappe.throw(_("No Warehouse present in this Route"))
            for res in warehouse:
                result = frappe.db.sql("""select dcs_id,milk_type,sum(volume) as total_volume,sum(fat) as fat,sum(clr) as clr 
                                    from `tabMilk Entry` 
                                    where docstatus =1 and dcs_id = %s and shift = %s and date = %s 
                                    group by milk_type""",(res.name,self.shift,self.date), as_dict =True)

                cow_volume = 0.0
                buffalow_volume = 0.0
                mix_volume = 0.0
                cow_milk_fat = buf_milk_fat = mix_milk_fat = 0.0
                cow_milk_clr = buf_milk_clr = mix_milk_clr = 0.0

                for i in result:
                    if i.get('milk_type') == 'Cow':
                        cow_volume = i.get('total_volume')
                        cow_milk_fat = i.get('fat')
                        cow_milk_clr = i.get('clr')

                    if i.get('milk_type') == 'Buffalow':
                        buffalow_volume = i.get('total_volume')
                        buf_milk_fat = i.get('fat')
                        buf_milk_clr = i.get('clr')

                    if i.get('milk_type') == 'Mix':
                        mix_volume =i.get('total_volume')
                        mix_milk_fat = i.get('fat')
                        mix_milk_clr = i.get('clr')

                if cow_volume > 0 or buffalow_volume > 0 or mix_volume > 0:
                    van_collection = frappe.new_doc("Van Collection Items")
                    van_collection.dcs = res.name
                    van_collection.cow_milk_vol = cow_volume
                    van_collection.buf_milk_vol = buffalow_volume
                    van_collection.mix_milk_vol = mix_volume
                    van_collection.van_collection = self.name

                    van_collection.cow_milk_fat = cow_milk_fat
                    van_collection.cow_milk_clr = cow_milk_clr
                    van_collection.buf_milk_fat = buf_milk_fat
                    van_collection.buf_milk_clr = buf_milk_clr
                    van_collection.mix_milk_fat = mix_milk_fat
                    van_collection.mix_milk_clr = mix_milk_clr

                    result1 = frappe.db.sql("""Select name,milk_type from `tabSample lines` where milk_entry in
                                                           (select name from `tabMilk Entry` 
                                                           where docstatus =1 and dcs_id = %s and shift = %s and date = %s 
                                                           )""", (res.name, self.shift, self.date), as_dict=True)
                    for res in result1:
                        if res.get('milk_type') == 'Cow':
                            van_collection.append("cow_milk_sam", {
                                'sample_lines': res.get('name')
                            })

                        if res.get('milk_type') == 'Buffalow':
                            van_collection.append("buf_milk_sam", {
                                'sample_lines': res.get('name')
                            })

                        if res.get('milk_type') == 'Mix':
                            van_collection.append("mix_milk_sam", {
                                'sample_lines': res.get('name')
                            })

                    van_collection.insert(ignore_permissions = True)

            frappe.db.set(self, 'status', 'In-Progress')
            self.flags.ignore_validate_update_after_submit = True  # ignore after submit permission
            self.save(ignore_permissions=True)
        return True



#---------------------stock entry method---------------

def change_van_collection_status(st,method):
    if st.van_collection_item:
        doc = frappe.get_doc("Van Collection Items", st.van_collection_item)
        doc.gate_pass =st.name
        doc.db_update()