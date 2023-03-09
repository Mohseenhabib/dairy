# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import date

from frappe.utils.data import flt

class VanCollection(Document):
    @frappe.whitelist()
    def submit_van_collection(self):
        self.db_set('status','Submitted')

    def on_cancel(self):
        milk_entry = frappe.get_all('Milk Entry',{'date':self.date},['name','van_collection_completed','date'])
        for me in milk_entry:
            if self.date == me.date:
                vcc = frappe.get_doc('Milk Entry',me.name) 
                vcc.db_set("van_collection_completed",0)
                vci = frappe.get_all('Van Collection Items',{'van_collection':self.name},['name'])
                for dl in vci:
                    dlt = frappe.delete_doc('Van Collection Items',dl.name)

        # stock_entry = frappe.get_all('Stock Entry',{'posting_date':self.date},['name','date'])
        # print('seeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',stock_entry)
        # for se in stock_entry:
            
        #     if self.date == se.posting_date:
        #         se_dlt = frappe.delete_doc('Stock Entry',se.name)
        #         print('delete stock entry&&&&&&&&&&&&&&&&&&&&&')

        
    @frappe.whitelist()
    def change_status_complete(self):
        self.db_set('status', 'Completed')
        self.flags.ignore_validate_update_after_submit = True  # ignore after submit permission
        milk_entry = frappe.get_all('Milk Entry',{'date':self.date},['name','van_collection_completed','date'])
        for me in milk_entry:
            if self.date == me.date:
                vcc = frappe.get_doc('Milk Entry',me.name)
                if self.status == "Completed":
                    vcc.db_set("van_collection_completed", 1)
        
        self.save(ignore_permissions=True)

    @frappe.whitelist()
    def van_start_collection(self):
        state_climatic_factor,state_factor = frappe.db.get_value('Warehouse',{'is_dcs':1},['state_climatic_factor','state_factor'])
        seq =[]
        sequence = frappe.db.get_all('Warehouse',{'is_dcs':1},['sequence'])
        for i in sequence:
            seq.append(i.get('sequence'))
        print('sequence******************',seq,sorted(seq))
        tdate = date.today()

        if self:
            warehouse = frappe.db.get_all("Warehouse",{
                                            "route": self.route,
                                            "is_dcs": 1
                                        })
            if not warehouse:
                frappe.throw(_("No Warehouse present in this Route"))
            for res in warehouse:
                result = frappe.db.sql("""select dcs_id,milk_type,sum(volume) as total_volume,sum(fat) as fat,sum(clr) as clr ,
                                    sum(fat_kg) as fat_kg , sum(snf_kg) as snf_kg , sum(clr_kg) as clr_kg
                                    from `tabMilk Entry` 
                                    where docstatus =1 and dcs_id = %s and shift = %s and date = %s 
                                    group by milk_type""",(res.name,self.shift,self.date), as_dict =True)

                print('result***************************',result,res)
                cow_volume = 0.0
                buffalo_volume = 0.0
                mix_volume = 0.0
                cow_milk_fat = buf_milk_fat = mix_milk_fat = 0.0
                cow_milk_clr = buf_milk_clr = mix_milk_clr = 0.0
                cow_milk_snf = buffalow_milk_snf = mix_milk_snf = 0.0
                buffalo_milk_snfin_kg = 0.0
                buffalo_milk_fatin_kg = 0.0
                mix_milk_snfin_kg = 0.0
                mix_milk_fatin_kg = 0.0
                cow_milk_snfin_kg=0.0
                cow_milk_fatin_kg=0.0
                cow_milk_clrin_kg=0.0
                mix_milk_clrin_kg = 0.0
                buffalo_milk_clrin_kg = 0.0

                for i in result:
                    if i.get('milk_type') == 'Cow':
                        cow_volume = i.get('total_volume')
                        cow_milk_fat = i.get('fat')
                        cow_milk_clr = i.get('clr')
                        cow_milk_snf = i.get('snf')
                        cow_milk_snfin_kg = i.get('snf_kg')
                        cow_milk_fatin_kg = i.get('fat_kg')
                        cow_milk_clrin_kg = i.get('clr_kg')

                    if i.get('milk_type') == 'Buffalo':
                        buffalo_volume = i.get('total_volume')
                        buf_milk_fat = i.get('fat')
                        buf_milk_clr = i.get('clr')
                        buffalo_milk_snf = i.get('snf')
                        buffalo_milk_snfin_kg = i.get('snf_kg')
                        buffalo_milk_fatin_kg = i.get('fat_kg')
                        buffalo_milk_clrin_kg = i.get('clr_kg')
                
                    if i.get('milk_type') == 'Mix':
                        mix_volume =i.get('total_volume')
                        mix_milk_fat = i.get('fat')
                        mix_milk_clr = i.get('clr')
                        mix_milk_snf = i.get('snf')
                        mix_milk_snfin_kg = i.get('snf_kg')
                        mix_milk_fatin_kg = i.get('fat_kg')
                        mix_milk_clrin_kg = i.get('clr_kg')
                   

                if cow_volume > 0 or buffalo_volume > 0 or mix_volume > 0:
                    van_collection = frappe.new_doc("Van Collection Items")
                    van_collection.dcs = res.name
                    van_collection.cow_milk_vol = cow_volume
                    van_collection.buf_milk_vol = buffalo_volume
                    van_collection.mix_milk_vol = mix_volume
                    van_collection.van_collection = self.name

                    van_collection.cow_milk_fat = cow_milk_fat
                    van_collection.cow_milk_clr = cow_milk_clr
                    van_collection.cow_milk_snf = cow_milk_snf
                    van_collection.cow_milk_snfin_kg = cow_milk_snfin_kg
                    van_collection.cow_milk_fatin_kg = cow_milk_fatin_kg
                    van_collection.cow_milk_clrin_kg = cow_milk_clrin_kg
                    van_collection.buffalo_milk_snfin_kg = buffalo_milk_snfin_kg
                    van_collection.buffalo_milk_fatin_kg = buffalo_milk_fatin_kg
                    van_collection.buffalo_milk_clrin_kg = buffalo_milk_clrin_kg
                    van_collection.buf_milk_fat = buf_milk_fat
                    van_collection.buf_milk_clr = buf_milk_clr
                    van_collection.mix_milk_snfin_kg = mix_milk_snfin_kg
                    van_collection.mix_milk_fatin_kg = mix_milk_fatin_kg
                    van_collection.mix_milk_clrin_kg = mix_milk_clrin_kg
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
                      
                        if res.get('milk_type') == 'Buffalo':
                            van_collection.append("buf_milk_sam", {
                                'sample_lines': res.get('name')
                            })

                        if res.get('milk_type') == 'Mix':
                            van_collection.append("mix_milk_sam", {
                                'sample_lines': res.get('name')
                            })     
                    
                    doc=frappe.get_doc("Dairy Settings")
                    item=0.0
                    if i.get("milk_type")=="Cow":
                        item = frappe.db.get_value('Item',{"name":doc.cow_pro},['weight_per_unit'])
                    if i.get("milk_type")=="Buffalo":
                        item = frappe.db.get_value('Item',{"name":doc.buf_pro},['weight_per_unit'])
                    if i.get("milk_type")=="Mix":
                        item = frappe.db.get_value('Item',{"name":doc.mix_pro},['weight_per_unit'])

                    print('buffalo volume8*****************',buffalo_volume)
                    if flt(cow_volume) > 0:
                        van_collection.cow_milk_fat = (cow_milk_fatin_kg /(cow_volume * item)) * 100 
                        van_collection.cow_milk_clr = (cow_milk_clrin_kg /(cow_volume * item)) * 100 
                        van_collection.cow_milk_snf = (cow_milk_snfin_kg /(cow_volume * item)) * 100
                    if flt(buffalo_volume) > 0:
                        van_collection.buf_milk_fat = (buffalo_milk_fatin_kg /(buffalo_volume  * item)) * 100 
                        van_collection.buf_milk_clr = (buffalo_milk_clrin_kg /(buffalo_volume  * item)) * 100
                        van_collection.buffalow_milk_snf = (buffalo_milk_snfin_kg /(buffalo_volume  * item)) * 100
                    
                    if flt(mix_volume) > 0:
                        van_collection.mix_milk_fat = (mix_milk_fatin_kg /(mix_volume * item)) * 100 
                        van_collection.mix_milk_snf = (mix_milk_snfin_kg /(mix_volume * item)) * 100
                        van_collection.cow_milk_clr = (mix_milk_clrin_kg /(mix_volume * item)) * 100 
                    van_collection.insert(ignore_permissions = True)
                    

            self.db_set('status', 'In-Progress')
            self.flags.ignore_validate_update_after_submit = True  # ignore after submit permission
            self.save(ignore_permissions=True)
        return True



#---------------------stock entry method---------------

def change_van_collection_status(st,method):
    if st.van_collection_item:
        doc = frappe.get_doc("Van Collection Items", st.van_collection_item)
        doc.gate_pass =st.name
        doc.db_update()
    print('st******************************8', st.rmrd_lines)
    if st.rmrd_lines:
        doc = frappe.get_doc("RMRD Lines", st.rmrd_lines)
        doc.stock_entry = st.name
        doc.db_update()