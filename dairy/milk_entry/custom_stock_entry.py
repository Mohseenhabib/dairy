from __future__ import unicode_literals
import json
from dairy.milk_entry.report.milk_ledger.milk_ledger import get_columns, get_item_details, get_items, get_opening_balance, get_stock_ledger_entries
from erpnext.stock.utils import update_included_uom_in_report
import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt,cint, cstr, getdate
from frappe.utils.data import today

def milk_ledger_stock_entry(self,method):
    if not self.get("__islocal"):
        if not self.van_collection and not self.van_collection_item:

            good_cow_milk = frappe.db.get_single_value("Dairy Settings", "cow_pro")
            good_buff_milk = frappe.db.get_single_value("Dairy Settings", "buf_pro")
            good_mix_milk = frappe.db.get_single_value("Dairy Settings", "mix_pro")
            milk_type = ""
            for itm in self.items:
                if itm.s_warehouse:
                    itm_obj = frappe.get_doc("Item",itm.item_code)
                    itm_weight = float(itm_obj.weight_per_unit)
                    weight_uom = itm_obj.weight_uom
                    maintain_snf_fat = itm_obj.maintain_fat_snf_clr
                    itm_milk_type = itm_obj.milk_type
                
                    if itm.item_code == good_cow_milk or itm.item_code == good_buff_milk or itm.item_code == good_mix_milk or maintain_snf_fat == 1:
                        if itm.item_code == good_cow_milk:
                            milk_type = "Cow"
                        elif itm.item_code == good_buff_milk:
                            milk_type = "Buffalo"
                        elif itm.item_code == good_mix_milk:
                            milk_type = "Mix"
                        elif maintain_snf_fat == 1:
                            milk_type = itm_milk_type
                            
                        query = """ select name from `tabMilk Ledger Entry` where item_code = %(item_code)s 
                        and warehouse = %(warehouse)s """
                        if itm.batch_no:
                            query += """ and batch_no = %(batch_no)s """
                        if itm.serial_no:
                            query += """ and serial_no = %(serial_no)s """

                        query += """ order by modified desc limit 1 """
                        mle = frappe.db.sql(query,
                                            {'warehouse': itm.s_warehouse, 'item_code': itm.item_code, 'batch_no': itm.batch_no,
                                            'serial_no': itm.serial_no}, as_dict=True)
       
                        # if mle:
                        #     mle_obj = frappe.get_doc("Milk Ledger Entry",mle[0]['name'])
                        #     print('mle_obj*************************',mle_obj)
                        #     itm.fat = (mle_obj.fat_per / 100) * (itm.transfer_qty * itm_weight)
                        #     itm.fat_per = mle_obj.fat_per
                        #     itm.snf_clr = (mle_obj.snf_per / 100) * (itm.transfer_qty * itm_weight)
                        #     itm.snf_clr_per = mle_obj.snf_per

                        # rate
                        # if milk_type != "":
                        #     print('milk type**********************')
                        #     query2 = frappe.db.sql(""" select bmpl.name, bmpl.rate, bmpl.snf_clr_rate 
                        #                             from `tabBulk Milk Price List` bmpl, `tabBulk Milk Price List Warehouse` bmplw
                        #                             where bmplw.warehouse = %(warehouse)s and bmpl.active = 1 and bmpl.milk_type = %(milk_type)s 
                        #                             and bmpl.name = bmplw.parent
                        #                             and bmpl.docstatus =1 
                        #                             order by bmpl.modified desc limit 1 """,
                        #                         {'warehouse':itm.s_warehouse,'milk_type':milk_type},
                        #                             as_dict=True)
                        #     if not query2:
                        #         query3 = frappe.db.sql(""" select bmpl.name, bmpl.rate, bmpl.snf_clr_rate 
                        #                                                     from `tabBulk Milk Price List` bmpl, `tabBulk Milk Price List Warehouse` bmplw
                        #                                                     where bmplw.warehouse = %(warehouse)s and bmpl.active = 1 and bmpl.milk_type = %(milk_type)s 
                        #                                                     and bmpl.name = bmplw.parent and bmpl.docstatus =1 order by bmpl.modified desc limit 1 """,
                        #                             {'warehouse': itm.s_warehouse, 'milk_type': milk_type},
                        #                             as_dict=True)
                        #         if not query3:
                        #             frappe.throw("No Rate Specified in Bulk Milk Price List")
                        #         else:
                        #             itm.rate = (((itm.fat_per * query3[0]['rate']) + (
                        #                         itm.snf_clr_per * query3[0]['snf_clr_rate'])) /  (itm.transfer_qty * itm_weight))
                        #     else:
                        #         itm.rate = (((itm.fat_per * query2[0]['rate']) + (itm.snf_clr_per * query2[0]['snf_clr_rate'])) /  (itm.transfer_qty * itm_weight))



    # create milk ledger entry
# def on_submit(self, method):
#     for itm in self.items:
      
#         if itm.s_warehouse:
#             itm_obj = frappe.get_doc("Item", itm.item_code)
#             itm_weight = float(itm_obj.weight_per_unit)
#             weight_uom = itm_obj.weight_uom
#             maintain_snf_fat = itm_obj.maintain_fat_snf_clr
#             good_cow_milk = frappe.db.get_single_value("Dairy Settings", "cow_pro")
#             good_buff_milk = frappe.db.get_single_value("Dairy Settings", "buf_pro")
#             good_mix_milk = frappe.db.get_single_value("Dairy Settings", "mix_pro")
#             if itm.item_code == good_cow_milk or itm.item_code == good_buff_milk or itm.item_code == good_mix_milk or maintain_snf_fat == 1:
#                 query = """ select count(*) from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
#                             """
#                 if itm.batch_no:
#                     query += """ and batch_no = %(batch_no)s """
#                 if itm.serial_no:
#                     query += """ and serial_no = %(serial_no)s """

#                 query += """ order by modified desc"""

#                 total_count = frappe.db.sql(query,{'warehouse':itm.s_warehouse,'item_code':itm.item_code,'batch_no':itm.batch_no,
#                                                    'serial_no':itm.serial_no})

#                 if total_count[0][0] != 0:
#                     query = """ select name from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
#                                                         """
#                     if itm.batch_no:
#                         query += """ and batch_no = %(batch_no)s """
#                     if itm.serial_no:
#                         query += """ and serial_no = %(serial_no)s """

#                     query += """ order by modified desc limit 1 """
#                     mle = frappe.db.sql(query,
#                                         {'warehouse': itm.s_warehouse, 'item_code': itm.item_code, 'batch_no': itm.batch_no,
#                                          'serial_no': itm.serial_no}, as_dict=True)
#                     if len(mle) > 0:
#                         if mle[0]['name']:
#                             mle_obj = frappe.get_doc("Milk Ledger Entry", mle[0]['name'])

#                             new_mle = frappe.new_doc("Milk Ledger Entry")
#                             new_mle.item_code = mle_obj.item_code
#                             new_mle.serial_no = cstr(mle_obj.serial_no).strip()
#                             new_mle.batch_no = mle_obj.batch_no
#                             new_mle.warehouse = mle_obj.warehouse
#                             new_mle.posting_date = self.posting_date
#                             new_mle.posting_time = self.posting_time
#                             new_mle.voucher_type = "Stock Entry"
#                             new_mle.voucher_no = self.name
#                             new_mle.voucher_detail_no = itm.name
#                             new_mle.actual_qty = -1 *  (itm.transfer_qty * itm_weight)
#                             new_mle.fat = -1 * float(itm.fat)
#                             new_mle.snf = -1 * float(itm.snf_clr)
#                             new_mle.fat_per =  float(itm.fat_per)
#                             new_mle.snf_per =  float(itm.snf_clr_per)
#                             new_mle.stock_uom = weight_uom
#                             new_mle.qty_after_transaction = mle_obj.qty_after_transaction - (itm.transfer_qty * itm_weight)
#                             new_mle.fat_after_transaction = mle_obj.fat_after_transaction - itm.fat
#                             new_mle.snf_after_transaction = mle_obj.snf_after_transaction - itm.snf_clr


#                             new_mle.save(ignore_permissions=True)
#                             # new_mle.submit()

#     for itm in self.items:
#         if itm.t_warehouse:
#             itm_obj = frappe.get_doc("Item", itm.item_code)
#             itm_weight = float(itm_obj.weight_per_unit)
#             weight_uom = itm_obj.weight_uom
#             maintain_snf_fat = itm_obj.maintain_fat_snf_clr
#             good_cow_milk = frappe.db.get_single_value("Dairy Settings", "cow_pro")
#             good_buff_milk = frappe.db.get_single_value("Dairy Settings", "buf_pro")
#             good_mix_milk = frappe.db.get_single_value("Dairy Settings", "mix_pro")
#             if itm.item_code == good_cow_milk or itm.item_code == good_buff_milk or itm.item_code == good_mix_milk or maintain_snf_fat == 1:
#                 query = """ select count(*) from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
#                             """
#                 if itm.batch_no:
#                     query += """ and batch_no = %(batch_no)s """
#                 if itm.serial_no:
#                     query += """ and serial_no = %(serial_no)s """

#                 query += """ order by modified desc"""

#                 total_count = frappe.db.sql(query, {'warehouse': itm.t_warehouse, 'item_code': itm.item_code,
#                                                     'batch_no': itm.batch_no,
#                                                     'serial_no': itm.serial_no})

#                 if total_count[0][0] == 0:
#                     pr_qty = flt(itm.qty) * flt(itm.conversion_factor)
#                     new_mle = frappe.new_doc("Milk Ledger Entry")
#                     new_mle.item_code = itm.item_code
#                     new_mle.serial_no = cstr(itm.serial_no).strip()
#                     new_mle.batch_no = itm.batch_no
#                     new_mle.warehouse = itm.t_warehouse
#                     new_mle.posting_date = self.posting_date
#                     new_mle.posting_time = self.posting_time
#                     new_mle.voucher_type = "Stock Entry"
#                     new_mle.voucher_no = self.name
#                     new_mle.voucher_detail_no = itm.name
#                     new_mle.actual_qty = (itm.transfer_qty * itm_weight)
#                     new_mle.fat = itm.fat
#                     new_mle.snf = itm.snf_clr
#                     new_mle.stock_uom = weight_uom
#                     new_mle.qty_after_transaction = (itm.transfer_qty * itm_weight)
#                     new_mle.fat_after_transaction = itm.fat
#                     new_mle.snf_after_transaction = itm.snf_clr
#                     new_mle.fat_per = (itm.fat / (itm.transfer_qty * itm_weight)) * 100
#                     new_mle.snf_per = (itm.snf_clr / (itm.transfer_qty * itm_weight)) * 100
#                     new_mle.save(ignore_permissions=True)
#                     # new_mle.submit()
#                 else:
#                     query = """ select name from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
#                                         """
#                     if itm.batch_no:
#                         query += """ and batch_no = %(batch_no)s """
#                     if itm.serial_no:
#                         query += """ and serial_no = %(serial_no)s """

#                     query += """ order by modified desc limit 1 """
#                     mle = frappe.db.sql(query, {'warehouse': itm.t_warehouse, 'item_code': itm.item_code,
#                                                 'batch_no': itm.batch_no,
#                                                 'serial_no': itm.serial_no}, as_dict=True)
#                     if len(mle) > 0:
#                         if mle[0]['name']:
#                             mle_obj = frappe.get_doc("Milk Ledger Entry", mle[0]['name'])
#                             new_mle = frappe.new_doc("Milk Ledger Entry")
#                             new_mle.item_code = mle_obj.item_code
#                             new_mle.serial_no = cstr(mle_obj.serial_no).strip()
#                             new_mle.batch_no = mle_obj.batch_no
#                             new_mle.warehouse = mle_obj.warehouse
#                             new_mle.posting_date = self.posting_date
#                             new_mle.posting_time = self.posting_time
#                             new_mle.voucher_type = "Stock Entry"
#                             new_mle.voucher_no = self.name
#                             new_mle.voucher_detail_no = itm.name
#                             new_mle.actual_qty = (itm.transfer_qty * itm_weight)
#                             new_mle.fat = itm.fat
#                             new_mle.snf = itm.snf_clr
#                             new_mle.stock_uom = weight_uom
#                             new_mle.qty_after_transaction = (itm.transfer_qty * itm_weight) + mle_obj.qty_after_transaction
#                             new_mle.fat_after_transaction = mle_obj.fat_after_transaction + itm.fat
#                             new_mle.snf_after_transaction = mle_obj.snf_after_transaction + itm.snf_clr
#                             new_mle.fat_per = ((mle_obj.fat_after_transaction + itm.fat) / (
#                                     (itm.transfer_qty * itm_weight) + mle_obj.qty_after_transaction)) * 100
#                             new_mle.snf_per = ((mle_obj.snf_after_transaction + itm.snf_clr) / (
#                                     (itm.transfer_qty * itm_weight) + mle_obj.qty_after_transaction)) * 100
#                             new_mle.save(ignore_permissions=True)
#
#                              # new_mle.submit()

def before_save(self,method):
    if self.stock_entry_type in ["Material Transfer","Material Issue","Material Transfer for Manufacture","Repack"]:
        for s in self.items:
            item = frappe.get_doc('Item',s.item_code)
            filters={'from_date':getdate(self.posting_date),'to_date':getdate(self.posting_date),'warehouse':s.s_warehouse,'item_code':s.item_code,'company':self.company}
            filters=frappe._dict(filters)
            ml=exec(filters)
            # print('mllllllllllllllllllllllllllllll',filters,ml)
            if (len(ml)) > 1:
                ml = ml[-1]
                if flt(ml.get("qty_after_transaction"))>0:
                    s.fat_per = (ml.get("fat_after_transaction")/ml.get("qty_after_transaction"))*100
                    s.snf_per = (ml.get("fat_after_transaction")/ml.get("qty_after_transaction"))*100
                    s.fat = ((s.qty*flt(s.fat_per))/100) * flt(item.weight_per_unit)
                    s.snf = ((s.qty*flt(s.snf_per))/100) * flt(item.weight_per_unit)
            else:
                ml = ml[0]
                if flt(ml.get("qty_after_transaction"))>0:
                    s.fat_per = (ml.get("fat_after_transaction")/ml.get("qty_after_transaction"))*100
                    s.snf_per = (ml.get("fat_after_transaction")/ml.get("qty_after_transaction"))*100
                    s.fat = ((s.qty*flt(s.fat_per))/100) * flt(item.weight_per_unit)
                    s.snf = ((s.qty*flt(s.snf_per))/100) * flt(item.weight_per_unit)

    if self.stock_entry_type=="Material Receipt":
        for j in self.items:
            if flt(j.fat_per)>0 or flt(j.snf_per)>0:
                frappe.throw("Fat and Snf Not defined")
    if self.stock_entry_type in ["Manufacture","Material Consumption for Manufacture"]:
        for s in self.items:
            item = frappe.get_doc('Item',s.item_code)
            filters={'from_date':getdate(self.posting_date),'to_date':getdate(self.posting_date),'warehouse':s.t_warehouse,'item_code':s.item_code,'company':self.company}
            filters=frappe._dict(filters)
            ml=exec(filters)
            # print('mllllllllllllllllllllllllllllll',filters,ml)
            if (len(ml)) > 1:
                ml = ml[-1]
                if flt(ml.get("qty_after_transaction"))>0:
                    s.fat_per = (ml.get("fat_after_transaction")/ml.get("qty_after_transaction"))*100
                    s.snf_per = (ml.get("fat_after_transaction")/ml.get("qty_after_transaction"))*100
                    s.fat = ((s.qty*flt(s.fat_per))/100) * flt(item.weight_per_unit)
                    s.snf = ((s.qty*flt(s.snf_per))/100) * flt(item.weight_per_unit)
            else:
                if ml:
                    ml = ml[0]
                    if flt(ml.get("qty_after_transaction"))>0:
                        s.fat_per = (ml.get("fat_after_transaction")/ml.get("qty_after_transaction"))*100
                        s.snf_per = (ml.get("fat_after_transaction")/ml.get("qty_after_transaction"))*100
                        s.fat = ((s.qty*flt(s.fat_per))/100) * flt(item.weight_per_unit)
                        s.snf = ((s.qty*flt(s.snf_per))/100) * flt(item.weight_per_unit)





def cancel_create_milk_stock_ledger(self,method):
    if self.van_collection or self.van_collection_item:
        vci = frappe.get_doc('Van Collection Items',self.van_collection_item)
        if vci.van_collection == self.van_collection:
            vc = frappe.get_doc('Van Collection',self.van_collection)
            vc.db_set('status','In-Progress')
            vc.db_update()
            # print('van collection satus *************************')

    if self.rmrd or self.rmrd_lines:
        r_lines = frappe.get_doc('RMRD Lines',self.rmrd_lines)
        if r_lines.rmrd == self.rmrd:
            rmrd = frappe.get_doc('RMRD',self.rmrd)
            rmrd.db_set('status','In-Progress')
            rmrd.db_update()
#             print('van collection satus *************************')
#     for itm in self.items:
#         if itm.t_warehouse:
#             itm_obj = frappe.get_doc("Item", itm.item_code)
#             itm_weight = float(itm_obj.weight_per_unit)
#             weight_uom = itm_obj.weight_uom
#             maintain_snf_fat = itm_obj.maintain_fat_snf_clr
#             good_cow_milk = frappe.db.get_single_value("Dairy Settings", "cow_pro")
#             good_buff_milk = frappe.db.get_single_value("Dairy Settings", "buf_pro")
#             good_mix_milk = frappe.db.get_single_value("Dairy Settings", "mix_pro")
#             if itm.item_code == good_cow_milk or itm.item_code == good_buff_milk or itm.item_code == good_mix_milk or maintain_snf_fat == 1:
#                 query = """ select name from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
#                                                 """
#                 if itm.batch_no:
#                     query += """ and batch_no = %(batch_no)s """
#                 if itm.serial_no:
#                     query += """ and serial_no = %(serial_no)s """
#                 query += """ and voucher_type = "Stock Entry" and voucher_no = %(voucher_no)s 
#                                                             and voucher_detail_no = %(voucher_detail_no)s """
#                 query += """ order by modified desc limit 1 """
#                 mle = frappe.db.sql(query, {'warehouse': itm.t_warehouse, 'item_code': itm.item_code, 'batch_no': itm.batch_no,
#                                             'serial_no': itm.serial_no,"voucher_detail_no":itm.name,"voucher_no":itm.parent}, as_dict=True)


#                 if len(mle) > 0:
#                     if mle[0]['name']:
#                         mle_obj = frappe.get_doc("Milk Ledger Entry", mle[0]['name'])
#                         new_mle = frappe.new_doc("Milk Ledger Entry")
#                         new_mle.item_code = mle_obj.item_code
#                         new_mle.serial_no = cstr(mle_obj.serial_no).strip()
#                         new_mle.batch_no = mle_obj.batch_no
#                         new_mle.warehouse = mle_obj.warehouse
#                         new_mle.posting_date = self.posting_date
#                         new_mle.posting_time = self.posting_time
#                         new_mle.voucher_type = "Stock Entry"
#                         new_mle.voucher_no = self.name
#                         new_mle.voucher_detail_no = itm.name
#                         new_mle.actual_qty = -1 * (itm.transfer_qty * itm_weight)
#                         new_mle.fat = -1 * itm.fat
#                         new_mle.snf = -1 * itm.snf_clr
#                         new_mle.stock_uom = weight_uom
#                         new_mle.qty_after_transaction = mle_obj.qty_after_transaction - (itm.transfer_qty * itm_weight)
#                         new_mle.fat_after_transaction = mle_obj.fat_after_transaction - itm.fat
#                         new_mle.snf_after_transaction = mle_obj.snf_after_transaction - itm.snf_clr
#                         if (mle_obj.qty_after_transaction - (itm.transfer_qty * itm_weight))>0:
#                             new_mle.fat_per = ((mle_obj.fat_after_transaction - itm.fat) / (mle_obj.qty_after_transaction - (itm.transfer_qty * itm_weight))) * 100
#                             new_mle.snf_per = ((mle_obj.snf_after_transaction - itm.snf_clr) / (mle_obj.qty_after_transaction - (itm.transfer_qty * itm_weight))) * 100

                       
#                         frappe.db.sql(""" update `tabMilk Ledger Entry` set is_cancelled = 1 where name = %(name)s """,
#                                       {'name': mle_obj.name})
#                         frappe.db.commit()

#                         new_mle.save(ignore_permissions=True)
#                         # new_mle.submit()
#                         frappe.db.sql(""" update `tabMilk Ledger Entry` set is_cancelled = 1 where name = %(name)s """,
#                                       {'name': new_mle.name})
#                         frappe.db.commit()
                        
        

#         if itm.s_warehouse:
#             itm_obj = frappe.get_doc("Item", itm.item_code)
#             itm_weight = float(itm_obj.weight_per_unit)
#             weight_uom = itm_obj.weight_uom
#             maintain_snf_fat = itm_obj.maintain_fat_snf_clr
#             good_cow_milk = frappe.db.get_single_value("Dairy Settings", "cow_pro")
#             good_buff_milk = frappe.db.get_single_value("Dairy Settings", "buf_pro")
#             good_mix_milk = frappe.db.get_single_value("Dairy Settings", "mix_pro")
#             if itm.item_code == good_cow_milk or itm.item_code == good_buff_milk or itm.item_code == good_mix_milk or maintain_snf_fat == 1:
#                 query = """ select name from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
#                                                         """
#                 if itm.batch_no:
#                     query += """ and batch_no = %(batch_no)s """
#                 if itm.serial_no:
#                     query += """ and serial_no = %(serial_no)s """

#                 query += """ and voucher_type = "Stock Entry" and voucher_no = %(voucher_no)s 
#                                                         and voucher_detail_no = %(voucher_detail_no)s """

#                 query += """ order by modified desc limit 1 """

#                 mle = frappe.db.sql(query,
#                                     {'warehouse': itm.s_warehouse, 'item_code': itm.item_code, 'batch_no': itm.batch_no,
#                                      'serial_no': itm.serial_no, "voucher_detail_no": itm.name,
#                                      "voucher_no": itm.parent}, as_dict=True)

#                 if len(mle) > 0:
#                     if mle[0]['name']:
#                         mle_obj = frappe.get_doc("Milk Ledger Entry", mle[0]['name'])

#                         new_mle = frappe.new_doc("Milk Ledger Entry")
#                         new_mle.item_code = mle_obj.item_code
#                         new_mle.serial_no = cstr(mle_obj.serial_no).strip()
#                         new_mle.batch_no = mle_obj.batch_no
#                         new_mle.warehouse = mle_obj.warehouse
#                         new_mle.posting_date = self.posting_date
#                         new_mle.posting_time = self.posting_time
#                         new_mle.voucher_type = "Stock Entry"
#                         new_mle.voucher_no = self.name
#                         new_mle.voucher_detail_no = itm.name
#                         new_mle.actual_qty = (itm.transfer_qty * itm_weight)
#                         new_mle.fat = float(itm.fat)
#                         new_mle.snf = float(itm.snf_clr)
#                         new_mle.stock_uom = weight_uom
#                         new_mle.qty_after_transaction = mle_obj.qty_after_transaction + (itm.transfer_qty * itm_weight)
#                         new_mle.fat_after_transaction = mle_obj.fat_after_transaction + itm.fat
#                         new_mle.snf_after_transaction = mle_obj.snf_after_transaction + itm.snf_clr
#                         new_mle.fat_per = (float(itm.fat) / (itm.transfer_qty * itm_weight)) * 100
#                         new_mle.snf_per = (float(itm.snf_clr) / (itm.transfer_qty * itm_weight)) * 100

#                         frappe.db.sql(""" update `tabMilk Ledger Entry` set is_cancelled = 1 where name = %(name)s """,
#                                       {'name': mle_obj.name})
#                         frappe.db.commit()

#                         new_mle.save(ignore_permissions=True)
#                         # new_mle.submit()
#                         frappe.db.sql(""" update `tabMilk Ledger Entry` set is_cancelled = 1 where name = %(name)s """,
#                                       {'name': new_mle.name})
#                         frappe.db.commit()
                                      
    vci = frappe.get_all('Van Collection Items',{'gate_pass':self.name},['name'])
    # print('vciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    for i in vci:
        doc=frappe.get_doc("Van Collection Items",i.name)
        se_del = doc.gate_pass
        doc.db_set("gate_pass","")
        self.van_collection_item = ""
        # frappe.db.sql("""DELETE FROM `tabStock Entry` where name = '{0}' """.format(se_del))
        # print('se_del***********************************')

    r_lines = frappe.get_all('RMRD Lines',{'stock_entry':self.name},['name'])
    for rl in r_lines:
        doc1 = frappe.get_doc('RMRD Lines',rl.name)
        se_dlt = doc1.stock_entry
        doc1.db_set('stock_entry',"")
        self.rmrd = ""
        # print('se dlt*****************************************')
        # frappe.db.sql("""DELETE FROM `tabStock Entry` where name = '{0}' """.format(se_dlt))


    


@frappe.whitelist()
def get_item_weight(item_code):
    obj = frappe.get_doc("Item",item_code)
    return obj.weight_per_unit


def update_vc_status(self,method):
    if self.van_collection and self.van_collection_item:
        vci = frappe.get_doc('Van Collection Items',self.van_collection_item)
        if vci.van_collection == self.van_collection:
            vc = frappe.get_doc('Van Collection',self.van_collection)
            vc.db_set('status','Completed')
            vc.db_update()
            # print('van collection satus *************************')

    if self.rmrd and self.rmrd_lines:
        r_lines = frappe.get_doc('RMRD Lines',self.rmrd_lines)
        if r_lines.rmrd == self.rmrd:
            rmrd = frappe.get_doc('RMRD',self.rmrd)
            rmrd.db_set('status','Completed')
            rmrd.db_update()
            # print('van collection satus *************************')


# def calculate_wfs(self,method):
#     if self.stock_entry_type=="Manufacture":
#         tot_qty=[]
#         for i in self.items:
#             if i.is_finished_item==0:
#                 tot_qty.append(i.qty)
#         for i in self.items:
#             if i.is_finished_item==1:
#                i.qty="{:.3f}".format(sum(tot_qty))

#         self.fg_completed_qty="{:.3f}".format(sum(tot_qty))
#         wo=frappe.get_doc("Work Order",self.work_order)
#         wo.db_set("status","In Process")
#         if self.item:
#             doc=frappe.get_doc("Item",self.item)
#             if doc.maintain_fat_snf_clr:
#                 self.required_fat=doc.standard_fat
#                 self.required_snf=doc.standard_snf
#                 self.total_fat_in_kg=(flt(sum(tot_qty))*flt(doc.weight_per_unit))*doc.standard_fat/100
#                 self.total_snf_in_kg=(flt(sum(tot_qty))*flt(doc.weight_per_unit))*doc.standard_snf/100
            

#             total_rm_fat=[]
#             total_rm_snf=[]
#             total_fat_in_kg=[]
#             total_snf_in_kg=[]
#             for i in self.items:
#                 if i.is_finished_item==0:
#                     item=frappe.get_doc("Item",i.item_code)
#                     if doc.maintain_fat_snf_clr:
#                         i.fat_per=item.standard_fat
#                         i.snf_per=item.standard_snf
#                         i.fat=(i.qty*item.weight_per_unit)*item.standard_fat/100
#                         i.snf=(i.qty*item.weight_per_unit)*item.standard_snf/100
#                         total_rm_fat.append(item.standard_fat)
#                         total_rm_snf.append(item.standard_snf)
#                         total_fat_in_kg.append((i.qty*item.weight_per_unit)*item.standard_fat/100)
#                         total_snf_in_kg.append((i.qty*item.weight_per_unit)*item.standard_snf/100)
#             if len(total_rm_fat)>0:
#                 self.total_rm_fat=sum(total_rm_fat)/len(self.items)

#             if len(total_rm_snf)>0:
#                 self.total_rm_snf=sum(total_rm_snf)/len(self.items)
#             if len(total_fat_in_kg)>0:
#                 self.total_rm_fats_in_kg=sum(total_fat_in_kg)
#             if len(total_snf_in_kg)>0:
#                 self.total_rm_snfs_in_kg=sum(total_snf_in_kg)
            

#             self.total_diff_fat=self.required_fat- self.total_rm_fat
#             self.total_diff_snf=self.required_snf-self.total_rm_snf
#             self.total_diff_fat_in_kg=self.total_fat_in_kg-self.total_rm_fats_in_kg
#             self.total_diff_snf_in_kg=self.total_snf_in_kg-self.total_rm_snfs_in_kg


    


def exec(filters=None):
    include_uom = filters.get("include_uom")
    columns = get_columns()
    items = get_items(filters)
    sl_entries = get_stock_ledger_entries(filters, items)
    item_details = get_item_details(items, sl_entries, include_uom)
    opening_row = get_opening_balance(filters, columns)
    precision = cint(frappe.db.get_single_value("System Settings", "float_precision"))

    data = []
    conversion_factors = []
    if opening_row:                                     
        data.append(opening_row)


    for sle in sl_entries:
        
        item_detail = item_details[sle.item_code]

        sle.update(item_detail)

        if filters.get("batch_no"):
            actual_qty += flt(sle.actual_qty, precision)
            # stock_value += sle.stock_value_difference

            if sle.voucher_type == 'Stock Reconciliation' and not sle.actual_qty:
                actual_qty = sle.qty_after_transaction
                # stock_value = sle.stock_value

            sle.update({
                "qty_after_transaction": abs(actual_qty)
                # "stock_value": stock_value
            })
        a = max(sle.mle_act_qty, 0)
        b =  min(sle.mle_act_qty, 0)
        sle.update({
            "in_wt": abs(a),
            "out_wt": abs(b)
        })
        e = max(sle.fat, 0)
        f = min(sle.fat, 0)
        sle.update({
            "in_fat": abs(e),
            "out_fat": abs(f)
        })
        c =  max(sle.snf, 0)
        d = min(sle.snf, 0)
        sle.update({
            "in_snf": abs(c),
            "out_snf": abs(d)
        })
        
        h =  max(sle.sle_act_qty ,0)
        i = min(sle.sle_act_qty,0)
        sle.update({
            "in_qty": abs(h),
            "out_qty": abs(i)
        })
        

        data.append(sle)
        # print('data*************************8',data)

        if include_uom:
            conversion_factors.append(item_detail.conversion_factor)

    update_included_uom_in_report(columns, data, include_uom, conversion_factors)
    return data


# @frappe.whitelist()
# def get_add_fat(name):
#     filters={}
#     se=frappe.get_doc("Stock Entry",name)
#     import datetime

#     start_of_month = datetime.datetime(getdate(se.posting_date).year, getdate(se.posting_date).month, 1)
#     for i in se.items:
#         if i.idx==1:
#             filters.update({'warehouse':"Production Cold Room - BDF","from_date":getdate(start_of_month),"to_date":getdate(se.posting_date),"company":se.company})
#     doc=frappe.get_doc("Dairy Settings")
#     items={}
#     qty=0
#     for i in doc.items_to_add_fat:
#         doc=frappe.get_doc("Item",i.item)
#         filters.update({"item_code":doc.name})
#         items.update({"item_code":doc.name,"item_name":doc.item_name,"qty":0,"uom":doc.stock_uom,
#                       "fat":doc.standard_fat,"snf":doc.standard_snf,
#                       "total_fat_in_kg":0,"total_snf_in_kg":0,"weight":doc.weight_per_unit})
#         filters=frappe._dict(filters)
#         it=exec(filters)
#         if len(it)>1:
#             dx=it[-1]
            
#             if dx.get("qty_after_transaction")>0 and flt(doc.weight_per_unit)>0 and dx.get("fat_after_transaction")>0:
#                 qty=((dx.get("qty_after_transaction")/dx.get("fat_after_transaction"))*se.total_diff_fat_in_kg)/flt(doc.weight_per_unit)
#                 items.update({"qty":qty})
#                 break
#     print("&&&&&&&&&&&&&&&&&&",items)
#     if qty==0:
#         frappe.throw("Item Qty Not found")
#     return items
        
        
# @frappe.whitelist()
# def get_add_snf(name):
#     doc=frappe.get_doc("Dairy Settings")
#     se=frappe.get_doc("Stock Entry",name)
#     items={}
#     for i in doc.items_to_add_snf:
#         if i.idx==1:
#             doc=frappe.get_doc("Item",i.item)
#             qty=abs(se.total_diff_snf_in_kg)/flt(doc.weight_per_unit)
#             items.update({"item_code":doc.name,"item_name":doc.item_name,"qty":qty,"uom":doc.stock_uom,
#                         "fat":doc.standard_fat,"snf":doc.standard_snf,
#                         "total_fat_in_kg":0,
#                         "total_snf_in_kg":se.total_diff_snf_in_kg,"weight":doc.weight_per_unit})
#     for i in se.items:
#         if i.idx==1:
#             pass
#     return items
        
# @frappe.whitelist()
# def get_remove_snf(name):
#     doc=frappe.get_doc("Dairy Settings")
#     se=frappe.get_doc("Stock Entry",name)
#     items={}
#     for i in doc.items_to_remove_snf:
#         if i.idx==1:
#             doc=frappe.get_doc("Item",i.item)
#             qty=abs(se.total_diff_snf_in_kg)/flt(doc.weight_per_unit)
#             items.update({"item_code":doc.name,"item_name":doc.item_name,"qty":qty,"uom":doc.stock_uom,
#                         "fat":doc.standard_fat,"snf":doc.standard_snf,
#                         "total_fat_in_kg":0,
#                         "total_snf_in_kg":se.total_diff_snf_in_kg,"weight":doc.weight_per_unit})
#     return items
        

# @frappe.whitelist()
# def get_remove_fat(name):
#     doc=frappe.get_doc("Dairy Settings")
#     items={}
#     se=frappe.get_doc("Stock Entry",name)
#     for i in doc.items_to_remove_fat:
#         if i.idx==1:
#             doc=frappe.get_doc("Item",i.item)
#             qty=abs(se.total_diff_fat_in_kg)/flt(doc.weight_per_unit)
           
#             items.update({"item_code":doc.name,"item_name":doc.item_name,"qty":qty,"uom":doc.stock_uom,
#                         "fat":doc.standard_fat,"snf":doc.standard_snf,
#                         "total_fat_in_kg":se.total_diff_fat_in_kg,"total_snf_in_kg":0,"weight":doc.weight_per_unit})
#     return items
        
@frappe.whitelist()
def add_scrap_item(work_order,stock_entry_type):
    items=[]
    if stock_entry_type=="Manufacture":
        doc=frappe.get_doc("Work Order",work_order)
        for i in doc.fg_item_scrap:
            items.append({"item":i.item,"qty":i.qty})
    return items