# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import frappe
from frappe import _
from datetime import datetime
from frappe.model.mapper import get_mapped_doc
from frappe.utils.data import flt
# from dairy.milk_entry.custom_purchase_receipt import change_milk_entry_status
# from dairy.milk_entry.custom_purchase_receipt import change_milk_status

class MilkEntry(Document):
    def before_save(self):
        self.get_pricelist()




    @frappe.whitelist()
    def get_pricelist(self):
        pricelist_name = frappe.db.sql("""
                        select milk_rate.name from `tabMilk Rate` as milk_rate 
                        inner join `tabWarehouse Child` as ware on ware.parent = milk_rate.name 
                        where milk_rate.milk_type = '{0}' and ware.warehouse_id = '{1}' 
                        and milk_rate.docstatus = 1 and milk_rate.effective_date <= '{2}' order by milk_rate.creation desc limit 1 """.format(self.milk_type,self.dcs_id,self.date))
        if not pricelist_name:
            frappe.throw(_("Milk Rate not found."))

        self.db_set('milk_rate', pricelist_name[0][0])

        
        milk_rate = frappe.db.get_value('Milk Rate',{'name':pricelist_name[0][0]},['name'])


        milk = frappe.get_doc('Milk Rate',milk_rate)

        if milk.simplified_milk_rate == 1:
            if milk_rate:  
                new_rate = (flt(milk.fat_rate_in_kg) * flt(self.fat)+flt(milk.snf_rate_in_kg) * flt(self.snf))/100
                if new_rate:
                    self.db_set('unit_price', new_rate)
                    self.db_set('unit_price_with_incentive',flt(new_rate))
                    final_rate = self.volume * new_rate
                    self.db_set('total',final_rate)
                    if milk.enable_deduction == 1:
                        doc=frappe.get_doc("Dairy Settings")
                        item=0.0
                        if self.get("milk_type")=="Cow":
                            item = frappe.db.get_value('Item',{"name":doc.cow_pro},['weight_per_unit'])
                        if self.get("milk_type")=="Buffalo":
                            item = frappe.db.get_value('Item',{"name":doc.buf_pro},['weight_per_unit'])
                        if self.get("milk_type")=="Mix":
                            item = frappe.db.get_value('Item',{"name":doc.mix_pro},['weight_per_unit'])



                        fat_min_cow_milk = flt(frappe.db.get_single_value("Dairy Settings", "fat_min_cow_milk"))
                        fat_min_buf_milk = flt(frappe.db.get_single_value("Dairy Settings", "fat_min_buf_milk"))
                        fat_min_mix_milk = flt(frappe.db.get_single_value("Dairy Settings", "fat_min_mix_milk"))
                        
                        snf_min_cow_milk = flt(frappe.db.get_single_value("Dairy Settings", "snf_min_cow_milk"))
                        snf_min_buf_milk = flt(frappe.db.get_single_value("Dairy Settings", "snf_min_buf_milk"))
                        snf_min_mix_milk = flt(frappe.db.get_single_value("Dairy Settings", "snf_min_mix_milk"))
                        
                    
                        # for mrc in milk.milk_rate_chart:
                        
                        if self.get("milk_type")=="Cow":
                            w = ((self.volume * item) * self.fat) 
                            for fd in milk.fat_deduction:
                                if self.fat >= fd.from_fat and self.fat <= fd.to_fat:
                                    deduction_rate = (self.volume) * fd.per_kg_deduction 
                                    final_rate = final_rate - deduction_rate
                                    # self.db_set('unit_price', new_rate)
                                    self.db_set('fat_deduction',deduction_rate)
                                    self.db_set('total',final_rate)
                                    self.db_set('fat_deduction_per',fd.per_kg_deduction)
                                    new_rate=flt(new_rate) - flt(fd.per_kg_deduction)
                                    self.db_set('unit_price_with_incentive',flt(new_rate))
                                    # self.db_set('status','Submitted')


                           
                            # w = ((self.volume * item) * self.snf)
                            for sd in milk.snf_deduction:   
                                if self.snf >= sd.from_snf and self.snf <= sd.to_snf:
                                    deduction_rate = (self.volume) * sd.per_kg_deduction 
                                    final_rate = final_rate - deduction_rate
                                    # self.db_set('unit_price', new_rate)
                                    self.db_set('snf_deduction',deduction_rate)
                                    self.db_set('total',final_rate)
                                    new_rate=flt(new_rate) - flt(sd.per_kg_deduction)
                                    self.db_set('snf_deduction_per',sd.per_kg_deduction)
                                    self.db_set('unit_price_with_incentive',flt(new_rate))
                                    print('snf---------------------((((((((((((((((((((((((((')
                                        # self.db_set('status','Submitted')
                    

                        if self.get("milk_type")=="Buffalo":
                            w = ((self.volume * item) * self.fat)
                            for fd in milk.fat_deduction:
                                if self.fat >= fd.from_fat and self.fat <= fd.to_fat:
                                    deduction_rate = (self.volume) * fd.per_kg_deduction 
                                    final_rate = final_rate - deduction_rate
                                    # self.db_set('unit_price', new_rate)
                                    self.db_set('fat_deduction',deduction_rate)
                                    self.db_set('total',final_rate)
                                    new_rate=flt(new_rate) - flt(fd.per_kg_deduction)
                                    self.db_set('fat_deduction_per',fd.per_kg_deduction)
                                    self.db_set('unit_price_with_incentive',flt(new_rate))
                                    # self.db_set('status','Submitted')


                            w = ((self.volume * item) * self.snf)
                            for sd in milk.snf_deduction:   
                                if self.snf >= sd.from_snf and self.snf <= sd.to_snf:
                                    deduction_rate = (self.volume) * sd.per_kg_deduction 
                                    final_rate = final_rate - deduction_rate
                                    # self.db_set('unit_price', new_rate)
                                    self.db_set('snf_deduction',deduction_rate)
                                    self.db_set('total',final_rate)
                                    new_rate=flt(new_rate) - flt(sd.per_kg_deduction)
                                    self.db_set('snf_deduction_per',sd.per_kg_deduction)
                                    self.db_set('unit_price_with_incentive',flt(new_rate))
                                    # self.db_set('status','Submitted')
                    
                        
                        if self.get("milk_type")=="Mix":
                            w = ((self.volume * item) * self.fat)
                            for fd in milk.fat_deduction:
                                if self.fat >= fd.from_fat and self.fat <= fd.to_fat:
                                    deduction_rate = (self.volume) * fd.per_kg_deduction 
                                    final_rate = final_rate - deduction_rate
                                    # self.db_set('unit_price', new_rate)
                                    self.db_set('fat_deduction',deduction_rate)
                                    self.db_set('total',final_rate)
                                    new_rate=flt(new_rate) - flt(fd.per_kg_deduction)
                                    self.db_set('fat_deduction_per',fd.per_kg_deduction)
                                    self.db_set('unit_price_with_incentive',flt(new_rate))
                                    # self.db_set('status','Submitted')


                            w = ((self.volume * item) * self.snf)
                            for sd in milk.snf_deduction:   
                                if self.snf >= sd.from_snf and self.snf <= sd.to_snf:
                                    deduction_rate = (self.volume) * sd.per_kg_deduction 
                                    final_rate = final_rate - deduction_rate
                                    # self.db_set('unit_price', new_rate)
                                    self.db_set('snf_deduction',deduction_rate)
                                    self.db_set('total',final_rate)
                                    new_rate=flt(new_rate) - flt(sd.per_kg_deduction)
                                    self.db_set('snf_deduction_per',sd.per_kg_deduction)
                                    self.db_set('unit_price_with_incentive',flt(new_rate))
                                    # self.db_set('status','Submitted')
                # self.db_set('unit_price_with_deduction',deduction_rate)
                    

                    if milk.enable_volume_incentive == 1:
                        ct = frappe.db.get_value('Supplier',{'name':self.member},['commission_type'])
                        if self.get("milk_type")=="Cow":
                            for incentive in milk.incentive:
                                if self.volume >= int(incentive.from_volume) and self.volume <= int(incentive.to_volume) and incentive.commission_type==ct:
                                    final_rate = final_rate + (incentive.incentive_per_volume * self.volume)
                                    ivolume =  incentive.incentive_per_volume * self.volume
                                    print('volume^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',ivolume)
                                    # final_rate = final_rate + ivolume
                                    self.db_set('incentive',ivolume)
                                    # self.db_set('unit_price', new_rate)
                                    self.db_set('total',final_rate)
                                    self.db_set('incentive_per',incentive.incentive_per_volume)
                                    new_rate=flt(new_rate) + flt(incentive.incentive_per_volume)
                                    self.db_set('unit_price_with_incentive',flt(new_rate))
                                    
                                    # self.db_set('status','Submitted')

                        if self.get("milk_type")=="Buffalo":
                            for incentive in milk.incentive: 
                                if self.volume >= int(incentive.from_volume) and self.volume <= int(incentive.to_volume) and incentive.commission_type==ct:
                                    final_rate = final_rate + (incentive.incentive_per_volume * self.volume)
                                    ivolume =  incentive.incentive_per_volume * self.volume
                                    # final_rate = final_rate + ivolume
                                    self.db_set('unit_price', new_rate)
                                    self.db_set('total',final_rate)
                                    self.db_set('incentive',ivolume)
                                    self.db_set('incentive_per',incentive.incentive_per_volume)
                                    new_rate=flt(new_rate) + flt(incentive.incentive_per_volume)
                                    self.db_set('unit_price_with_incentive',flt(new_rate))
                                    # self.db_set('status','Submitted')

                        if self.get("milk_type")=="Mix":
                            for incentive in milk.incentive: 
                                if self.volume >= int(incentive.from_volume) and self.volume <= int(incentive.to_volume) and incentive.commission_type==ct:
                                    final_rate = final_rate + (incentive.incentive_per_volume * self.volume)
                                    ivolume =  incentive.incentive_per_volume * self.volume
                                    # final_rate = final_rate + (incentive.incentive_per_volume*self.volume)
                                    self.db_set('unit_price', new_rate)
                                    self.db_set('total',final_rate)
                                    self.db_set('incentive',ivolume)
                                    self.db_set('incentive_per',incentive.incentive_per_volume)
                                    new_rate=flt(new_rate) + flt(incentive.incentive_per_volume)
                                    self.db_set('unit_price_with_incentive',flt(new_rate))


                    if  milk.enable_deduction == 0 and milk.enable_volume_incentive == 0:
                        self.db_set('unit_price', new_rate)
                        self.db_set('total',new_rate * self.volume)
                        self.db_set('unit_price_with_incentive',new_rate)
                else:                   
                        frappe.throw(_("No Rate Found For Provide Combination."))               
            
            
        
        else:                        
            if milk_rate:  
                # milk = frappe.get_doc('Milk Rate',milk_rate)
                rate = frappe.db.sql(""" select rate from `tabMilk Rate Chart` where fat BETWEEN {0} and {1} 
                        and parent = '{2}' order by fat,snf_clr asc limit 1 """.format(self.fat,self.snf,pricelist_name[0][0]))
                print('rate****************************************',rate)
                    
                if rate:
                    pr=rate[0][0]
                    final_rate = self.volume *rate[0][0]
                    self.db_set('unit_price_with_incentive',rate[0][0])
                    self.db_set('total',final_rate)

                    if milk.enable_deduction == 1:
                        doc=frappe.get_doc("Dairy Settings")
                        item=0.0
                        if self.get("milk_type")=="Cow":
                            item = frappe.db.get_value('Item',{"name":doc.cow_pro},['weight_per_unit'])
                        if self.get("milk_type")=="Buffalo":
                            item = frappe.db.get_value('Item',{"name":doc.buf_pro},['weight_per_unit'])
                        if self.get("milk_type")=="Mix":
                            item = frappe.db.get_value('Item',{"name":doc.mix_pro},['weight_per_unit'])



                        fat_min_cow_milk = flt(frappe.db.get_single_value("Dairy Settings", "fat_min_cow_milk"))
                        fat_min_buf_milk = flt(frappe.db.get_single_value("Dairy Settings", "fat_min_buf_milk"))
                        fat_min_mix_milk = flt(frappe.db.get_single_value("Dairy Settings", "fat_min_mix_milk"))
                        
                        snf_min_cow_milk = flt(frappe.db.get_single_value("Dairy Settings", "snf_min_cow_milk"))
                        snf_min_buf_milk = flt(frappe.db.get_single_value("Dairy Settings", "snf_min_buf_milk"))
                        snf_min_mix_milk = flt(frappe.db.get_single_value("Dairy Settings", "snf_min_mix_milk"))
                        
                    
                        # for mrc in milk.milk_rate_chart:
                       
                        if self.get("milk_type")=="Cow":
                            if self.fat < fat_min_cow_milk:
                                w = (self.volume * item* fat_min_cow_milk)
                                print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',w)
                                b = self.volume* item * self.fat
                                # if self.fat not in milk.milk_rate_chart:
                                for fd in milk.fat_deduction:
                                    if self.fat >= fd.from_fat and self.fat <= fd.to_fat:
                                        deduction_rate = (w-b ) * fd.per_kg_deduction 
                                        final_rate = final_rate - deduction_rate
                                        self.db_set('unit_price', rate[0][0])
                                        self.db_set('fat_deduction',deduction_rate)
                                        self.db_set('total',final_rate)
                                        self.db_set('fat_deduction_per',fd.per_kg_deduction)
                                        pr = flt(pr)-flt(fd.per_kg_deduction)
                                        self.db_set('unit_price_with_incentive',pr)
                                        print('fat deduction**********************************',rate[0][0] - fd.per_kg_deduction)
                                        # self.db_set('status','Submitted')
                            else:
                                self.db_set('unit_price', rate[0][0])
                                self.db_set('total',final_rate)

                            if self.snf < snf_min_cow_milk:
                                    w = (self.volume * item* snf_min_cow_milk)
                                    b = self.volume* item * self.snf
                                    # if self.snf not in milk.milk_rate_chart:
                                    for sd in milk.snf_deduction:   
                                        if self.snf >= sd.from_snf and self.snf <= sd.to_snf:
                                            deduction_rate = (w-b ) * sd.per_kg_deduction 
                                            final_rate = final_rate - deduction_rate
                                            self.db_set('unit_price', rate[0][0])
                                            self.db_set('total',final_rate)
                                            self.db_set('snf_deduction',deduction_rate)
                                            self.db_set('total',final_rate)
                                            self.db_set('snf_deduction_per',sd.per_kg_deduction)
                                            pr = flt(pr)-flt(sd.per_kg_deduction)
                                            self.db_set('unit_price_with_incentive',pr)
                                            print('snf deduction**********************************',rate[0][0] - sd.per_kg_deduction)
                                            # self.db_set('status','Submitted')
                            else:
                                self.db_set('unit_price', rate[0][0])
                                self.db_set('total',final_rate)

                        
                        if self.get("milk_type")=="Buffalo":
                            if self.fat < fat_min_buf_milk:
                                w = (self.volume * item* fat_min_buf_milk)
                                b = self.volume* item * self.fat
                                for fd in milk.fat_deduction:
                                    if self.fat >= fd.from_fat and self.fat <= fd.to_fat:
                                        deduction_rate = (w-b ) * fd.per_kg_deduction 
                                        final_rate = final_rate - deduction_rate
                                        self.db_set('unit_price', rate[0][0])
                                        self.db_set('fat_deduction',deduction_rate)
                                        self.db_set('total',final_rate)
                                        self.db_set('fat_deduction_per',fd.per_kg_deduction)
                                        pr = flt(pr)-flt(fd.per_kg_deduction)
                                        self.db_set('unit_price_with_incentive',pr)
                                        # self.db_set('status','Submitted')
                            else:
                                self.db_set('unit_price', rate[0][0])
                                self.db_set('total',final_rate)


                            if self.snf < snf_min_buf_milk:
                                w = (self.volume * item* snf_min_buf_milk)
                                b = self.volume* item * self.snf
                                for sd in milk.snf_deduction:   
                                    if self.snf >= sd.from_snf and self.snf <= sd.to_snf:
                                        deduction_rate = (w-b ) * sd.per_kg_deduction 
                                        final_rate = final_rate - deduction_rate
                                        self.db_set('unit_price', rate[0][0])
                                        self.db_set('snf_deduction',deduction_rate)
                                        self.db_set('total',final_rate)
                                        self.db_set('snf_deduction_per',sd.per_kg_deduction)
                                        pr = flt(pr) - flt(sd.per_kg_deduction)
                                        self.db_set('unit_price_with_incentive',pr)
                                        # self.db_set('status','Submitted')
                            else:
                                self.db_set('unit_price', rate[0][0])
                                self.db_set('total',final_rate)

                        
                        
                        if self.get("milk_type")=="Mix":
                            if self.fat < fat_min_mix_milk:
                                w = (self.volume * item* fat_min_mix_milk)
                                b = self.volume* item * self.fat
                                for fd in milk.fat_deduction:
                                    if self.fat >= fd.from_fat and self.fat <= fd.to_fat:
                                        deduction_rate = (w-b ) * fd.per_kg_deduction 
                                        final_rate = final_rate - deduction_rate
                                        self.db_set('unit_price', rate[0][0])
                                        self.db_set('fat_deduction',deduction_rate)
                                        self.db_set('total',final_rate)
                                        self.db_set('fat_deduction_per',fd.per_kg_deduction)
                                        pr = flt(pr) - flt(fd.per_kg_deduction)
                                        self.db_set('unit_price_with_incentive',pr)
                                        
                                        # self.db_set('status','Submitted')
                            else:
                                self.db_set('unit_price', rate[0][0])
                                self.db_set('total',final_rate)


                            if self.snf < snf_min_mix_milk:
                                    w = (self.volume * item* snf_min_mix_milk)
                                    b = self.volume* item * self.snf
                                    for sd in milk.snf_deduction:   
                                        if self.snf >= sd.from_snf and self.snf <= sd.to_snf:
                                            deduction_rate = (w-b ) * sd.per_kg_deduction 
                                            final_rate = final_rate - deduction_rate
                                            self.db_set('unit_price', rate[0][0])
                                            self.db_set('snf_deduction',deduction_rate)
                                            self.db_set('total',final_rate)
                                            self.db_set('snf_deduction_per',sd.per_kg_deduction)
                                            pr = flt(pr) - flt(sd.per_kg_deduction)
                                            self.db_set('unit_price_with_incentive',pr)
                                            # self.db_set('status','Submitted')
                            else:
                                self.db_set('unit_price', rate[0][0])
                                self.db_set('total',final_rate)

                        
                    
                    if milk.enable_volume_incentive == 1:
                        ct = frappe.db.get_value('Supplier',{'name':self.member},['commission_type'])
                        if self.get("milk_type")=="Cow":
                            for incentive in milk.incentive:
                                if self.volume >= int(incentive.from_volume) and self.volume <= int(incentive.to_volume) and incentive.commission_type==ct:
                                    final_rate = final_rate + (incentive.incentive_per_volume * self.volume)
                                    ivolume =  incentive.incentive_per_volume * self.volume
                                    print('volume^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',ivolume)
                                    # final_rate = final_rate + ivolume
                                    self.db_set('incentive',ivolume)
                                    self.db_set('unit_price', rate[0][0])
                                    self.db_set('total',final_rate)
                                    self.db_set('incentive_per',incentive.incentive_per_volume)
                                    pr = flt(pr) + flt(incentive.incentive_per_volume)
                                    self.db_set('unit_price_with_incentive',pr)
                                    # self.db_set('status','Submitted')

                        if self.get("milk_type")=="Buffalo":
                            for incentive in milk.incentive: 
                                if self.volume >= int(incentive.from_volume) and self.volume <= int(incentive.to_volume) and incentive.commission_type==ct:
                                    final_rate = final_rate + (incentive.incentive_per_volume * self.volume)
                                    ivolume =  incentive.incentive_per_volume * self.volume
                                    # final_rate = final_rate + ivolume
                                    self.db_set('unit_price', rate[0][0])
                                    self.db_set('total',final_rate)
                                    self.db_set('incentive',ivolume)
                                    self.db_set('incentive_per',incentive.incentive_per_volume)
                                    pr = flt(pr) + flt(incentive.incentive_per_volume)
                                    self.db_set('unit_price_with_incentive',pr)
                                    # self.db_set('status','Submitted')

                        if self.get("milk_type")=="Mix":
                            for incentive in milk.incentive: 
                                if self.volume >= int(incentive.from_volume) and self.volume <= int(incentive.to_volume) and incentive.commission_type==ct:
                                    final_rate = final_rate + (incentive.incentive_per_volume * self.volume)
                                    ivolume =  incentive.incentive_per_volume * self.volume
                                    # final_rate = final_rate + (incentive.incentive_per_volume*self.volume)
                                    self.db_set('unit_price', rate[0][0])
                                    self.db_set('total',final_rate)
                                    self.db_set('incentive',ivolume)
                                    self.db_set('incentive_per',incentive.incentive_per_volume)
                                    pr = flt(pr) + flt(incentive.incentive_per_volume)
                                    self.db_set('unit_price_with_incentive',pr)

                    if  milk.enable_deduction == 0 and milk.enable_volume_incentive == 0:
                        self.db_set('unit_price', rate[0][0])
                        self.db_set('total',rate[0][0] * self.volume)
                        self.db_set('unit_price_with_incentive',rate[0][0])
                    
                else:                   
                    frappe.throw(_("No Rate Found For Provide Combination."))               
                                    
            # self.db_set('status','Submitted')


        state_climatic_factor,state_factor = frappe.db.get_value('Warehouse',{'is_dcs':1},['state_climatic_factor','state_factor'])
        if self.clr != 0 or self.snf !=0:
            if self.snf == 0 or not self.snf:
                snf =  ((self.clr/4)+(self.fat*(state_climatic_factor)+(state_factor)))
                self.db_set('snf', snf)
                print('snfffffffffffffffffff',self.snf)

            if self.clr == 0 or not self.clr:
                clr = (self.snf - (state_factor) - ((state_climatic_factor)*self.fat)) * 4
                self.db_set('clr', clr)
                print('clrrrrrrrrrrrrrrrrrrrr',clr)
            
            doc=frappe.get_doc("Dairy Settings")
            item=0.0
            if self.get("milk_type")=="Cow":
                item = frappe.db.get_value('Item',{"name":doc.cow_pro},['weight_per_unit'])
            if self.get("milk_type")=="Buffalo":
                item = frappe.db.get_value('Item',{"name":doc.buf_pro},['weight_per_unit'])
            if self.get("milk_type")=="Mix":
                item = frappe.db.get_value('Item',{"name":doc.mix_pro},['weight_per_unit'])


            fat_kg =  ((self.volume * (item)) * (self.fat/100))
            self.db_set('fat_kg', fat_kg)
            print('fat_kg**************',fat_kg,item)
            
        
            snf_kg =  ((self.volume * (item)) * (self.snf/100))
            self.db_set('snf_kg', snf_kg)
            print('snfYYYYYYYYYYYYYYYYY',snf_kg)

            clr_kg =  ((self.volume * (item)) * (self.clr/100))
            self.db_set('clr_kg', clr_kg)
            print('clr%%%%%%%%%%%%%%%%%%',clr_kg)

            litre = ((self.volume * (item)))
            self.db_set('litre', litre)
    

            pricelist_name = frappe.db.sql("""
                        select milk_rate.name from `tabMilk Rate` as milk_rate 
                        inner join `tabWarehouse Child` as ware on ware.parent = milk_rate.name 
                        where milk_rate.milk_type = '{0}' and ware.warehouse_id = '{1}' 
                        and milk_rate.docstatus = 1 and milk_rate.effective_date <= '{2}' order by milk_rate.creation desc limit 1  """.format(self.milk_type,self.dcs_id,self.date))
            
            print('pricelist name____________________________-',pricelist_name)
            if not pricelist_name:
                frappe.throw(_("Milk Rate not found."))
            milk_rate = frappe.db.get_value('Milk Rate',{'name':pricelist_name[0][0]},['name'])
            if milk_rate:
                milk = frappe.get_doc('Milk Rate',milk_rate)
                if milk.enable_deduction == 0:
                    self.db_set('milk_rate', pricelist_name[0][0])
                    rate = frappe.db.sql(""" select rate from `tabMilk Rate Chart` where fat >= {0} and snf_clr >= {1} 
                            and parent = '{2}' order by fat,snf_clr asc limit 1 """.format(self.fat,self.snf,pricelist_name[0][0]))

                    print('rateEEEEEEEEEEEEEEEEEEEEEEEEEE',rate,pricelist_name[0][0])
                    print('milk rate^^^^^^^^^^^^^^^^1111111111111111111',pricelist_name)
                    
                    
                    # self.db_set('unit_price', rate[0][0])
                    # self.db_set('total',(self.volume *self.unit_price))
                    self.db_set('status','Submitted')



    @frappe.whitelist()
    def stock_data(self):
        doc=frappe.get_doc("Dairy Settings")
        if self.get("milk_type")=="Cow":
            itm = frappe.db.get_value('Item',{"name":doc.cow_pro},['stock_uom'])
        if self.get("milk_type")=="Buffalo":
            itm = frappe.db.get_value('Item',{"name":doc.buf_pro},['stock_uom'])
        if self.get("milk_type")=="Mix":
            itm = frappe.db.get_value('Item',{"name":doc.mix_pro},['stock_uom'])
        
        self.db_set('stock_uom',itm)    

    @frappe.whitelist()
    def before_submit(self):
        self.create_purchase_receipt()
        
        
    @frappe.whitelist()
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

        doc.set_posting_time = 1
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
            'rate': self.unit_price_with_incentive,
            'warehouse': self.dcs_id,
            'fat': self.fat_kg,
            'clr': self.snf_kg,
            'snf':self.clr_kg,
            'snf_clr_per' : self.snf,
            'clr_per' : self.clr,
            'fat_per_' : self.fat
        })
        doc.insert(ignore_permissions=True)
        doc.submit()
        # self.db_set("status" ,"To Sample and Bill")
        return doc

def _get_product(milk_type):
    if milk_type == 'Cow':
        item_code = frappe.db.get_single_value("Dairy Settings", "cow_pro")
    elif milk_type == 'Buffalo':
        item_code = frappe.db.get_single_value("Dairy Settings", "buf_pro")
    elif milk_type == 'Mix':
        item_code = frappe.db.get_single_value("Dairy Settings", "mix_pro")

    item = frappe.get_doc('Item', item_code)
    return item

@frappe.whitelist()
def create_raw_sample(source_name, target_doc=None):
    doc=frappe.db.get_value("Sample lines",{'milk_entry':source_name},'name')
    if not doc:
        def update_item(obj, target, source_parent):
            print('target&&&&&&&&&&&&&&&&&&&&&',source_name,obj.name,target)
            raw_sample = frappe.get_all('Raw Milk Sample',['name'])
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

        
        print('doclist$$$$$$$$$$$$$$$$$$$$$$$$$$$$',doclist,source_name)

        return doclist

    else:
        frappe.throw('Raw sample {0} already exist against milk entry {1}'.format(doc,source_name))

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

    print('doclist*********************88888',doclist)

    return doclist


