from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt,cint, cstr, getdate

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
                        # if not mle:
                        #     frappe.throw("Milk Ledger Entry Not Found For This Item")
                        if mle:
                            mle_obj = frappe.get_doc("Milk Ledger Entry",mle[0]['name'])
                            print('mle_obj*************************',mle_obj)
                            itm.fat = (mle_obj.fat_per / 100) * (itm.transfer_qty * itm_weight)
                            itm.fat_per = mle_obj.fat_per
                            itm.snf_clr = (mle_obj.snf_per / 100) * (itm.transfer_qty * itm_weight)
                            itm.snf_clr_per = mle_obj.snf_per

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
def on_submit(self, method):
    for itm in self.items:
      
        if itm.s_warehouse:
            itm_obj = frappe.get_doc("Item", itm.item_code)
            itm_weight = float(itm_obj.weight_per_unit)
            weight_uom = itm_obj.weight_uom
            maintain_snf_fat = itm_obj.maintain_fat_snf_clr
            good_cow_milk = frappe.db.get_single_value("Dairy Settings", "cow_pro")
            good_buff_milk = frappe.db.get_single_value("Dairy Settings", "buf_pro")
            good_mix_milk = frappe.db.get_single_value("Dairy Settings", "mix_pro")
            if itm.item_code == good_cow_milk or itm.item_code == good_buff_milk or itm.item_code == good_mix_milk or maintain_snf_fat == 1:
                query = """ select count(*) from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
                            """
                if itm.batch_no:
                    query += """ and batch_no = %(batch_no)s """
                if itm.serial_no:
                    query += """ and serial_no = %(serial_no)s """

                query += """ order by modified desc"""

                total_count = frappe.db.sql(query,{'warehouse':itm.s_warehouse,'item_code':itm.item_code,'batch_no':itm.batch_no,
                                                   'serial_no':itm.serial_no})

                if total_count[0][0] != 0:
                    query = """ select name from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
                                                        """
                    if itm.batch_no:
                        query += """ and batch_no = %(batch_no)s """
                    if itm.serial_no:
                        query += """ and serial_no = %(serial_no)s """

                    query += """ order by modified desc limit 1 """
                    mle = frappe.db.sql(query,
                                        {'warehouse': itm.s_warehouse, 'item_code': itm.item_code, 'batch_no': itm.batch_no,
                                         'serial_no': itm.serial_no}, as_dict=True)
                    if len(mle) > 0:
                        if mle[0]['name']:
                            mle_obj = frappe.get_doc("Milk Ledger Entry", mle[0]['name'])

                            new_mle = frappe.new_doc("Milk Ledger Entry")
                            new_mle.item_code = mle_obj.item_code
                            new_mle.serial_no = cstr(mle_obj.serial_no).strip()
                            new_mle.batch_no = mle_obj.batch_no
                            new_mle.warehouse = mle_obj.warehouse
                            new_mle.posting_date = self.posting_date
                            new_mle.posting_time = self.posting_time
                            new_mle.voucher_type = "Stock Entry"
                            new_mle.voucher_no = self.name
                            new_mle.voucher_detail_no = itm.name
                            new_mle.actual_qty = -1 *  (itm.transfer_qty * itm_weight)
                            new_mle.fat = -1 * float(itm.fat)
                            new_mle.snf = -1 * float(itm.snf_clr)
                            new_mle.fat_per =  float(itm.fat_per)
                            new_mle.snf_per =  float(itm.snf_clr_per)
                            new_mle.stock_uom = weight_uom
                            new_mle.qty_after_transaction = mle_obj.qty_after_transaction - (itm.transfer_qty * itm_weight)
                            new_mle.fat_after_transaction = mle_obj.fat_after_transaction - itm.fat
                            new_mle.snf_after_transaction = mle_obj.snf_after_transaction - itm.snf_clr


                            new_mle.save(ignore_permissions=True)
                            # new_mle.submit()

    for itm in self.items:
        if itm.t_warehouse:
            itm_obj = frappe.get_doc("Item", itm.item_code)
            itm_weight = float(itm_obj.weight_per_unit)
            weight_uom = itm_obj.weight_uom
            maintain_snf_fat = itm_obj.maintain_fat_snf_clr
            good_cow_milk = frappe.db.get_single_value("Dairy Settings", "cow_pro")
            good_buff_milk = frappe.db.get_single_value("Dairy Settings", "buf_pro")
            good_mix_milk = frappe.db.get_single_value("Dairy Settings", "mix_pro")
            if itm.item_code == good_cow_milk or itm.item_code == good_buff_milk or itm.item_code == good_mix_milk or maintain_snf_fat == 1:
                query = """ select count(*) from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
                            """
                if itm.batch_no:
                    query += """ and batch_no = %(batch_no)s """
                if itm.serial_no:
                    query += """ and serial_no = %(serial_no)s """

                query += """ order by modified desc"""

                total_count = frappe.db.sql(query, {'warehouse': itm.t_warehouse, 'item_code': itm.item_code,
                                                    'batch_no': itm.batch_no,
                                                    'serial_no': itm.serial_no})

                if total_count[0][0] == 0:
                    pr_qty = flt(itm.qty) * flt(itm.conversion_factor)
                    new_mle = frappe.new_doc("Milk Ledger Entry")
                    new_mle.item_code = itm.item_code
                    new_mle.serial_no = cstr(itm.serial_no).strip()
                    new_mle.batch_no = itm.batch_no
                    new_mle.warehouse = itm.t_warehouse
                    new_mle.posting_date = self.posting_date
                    new_mle.posting_time = self.posting_time
                    new_mle.voucher_type = "Stock Entry"
                    new_mle.voucher_no = self.name
                    new_mle.voucher_detail_no = itm.name
                    new_mle.actual_qty = (itm.transfer_qty * itm_weight)
                    new_mle.fat = itm.fat
                    new_mle.snf = itm.snf_clr
                    new_mle.stock_uom = weight_uom
                    new_mle.qty_after_transaction = (itm.transfer_qty * itm_weight)
                    new_mle.fat_after_transaction = itm.fat
                    new_mle.snf_after_transaction = itm.snf_clr
                    new_mle.fat_per = (itm.fat / (itm.transfer_qty * itm_weight)) * 100
                    new_mle.snf_per = (itm.snf_clr / (itm.transfer_qty * itm_weight)) * 100
                    new_mle.save(ignore_permissions=True)
                    # new_mle.submit()
                else:
                    query = """ select name from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
                                        """
                    if itm.batch_no:
                        query += """ and batch_no = %(batch_no)s """
                    if itm.serial_no:
                        query += """ and serial_no = %(serial_no)s """

                    query += """ order by modified desc limit 1 """
                    mle = frappe.db.sql(query, {'warehouse': itm.t_warehouse, 'item_code': itm.item_code,
                                                'batch_no': itm.batch_no,
                                                'serial_no': itm.serial_no}, as_dict=True)
                    if len(mle) > 0:
                        if mle[0]['name']:
                            mle_obj = frappe.get_doc("Milk Ledger Entry", mle[0]['name'])
                            new_mle = frappe.new_doc("Milk Ledger Entry")
                            new_mle.item_code = mle_obj.item_code
                            new_mle.serial_no = cstr(mle_obj.serial_no).strip()
                            new_mle.batch_no = mle_obj.batch_no
                            new_mle.warehouse = mle_obj.warehouse
                            new_mle.posting_date = self.posting_date
                            new_mle.posting_time = self.posting_time
                            new_mle.voucher_type = "Stock Entry"
                            new_mle.voucher_no = self.name
                            new_mle.voucher_detail_no = itm.name
                            new_mle.actual_qty = (itm.transfer_qty * itm_weight)
                            new_mle.fat = itm.fat
                            new_mle.snf = itm.snf_clr
                            new_mle.stock_uom = weight_uom
                            new_mle.qty_after_transaction = (itm.transfer_qty * itm_weight) + mle_obj.qty_after_transaction
                            new_mle.fat_after_transaction = mle_obj.fat_after_transaction + itm.fat
                            new_mle.snf_after_transaction = mle_obj.snf_after_transaction + itm.snf_clr
                            new_mle.fat_per = ((mle_obj.fat_after_transaction + itm.fat) / (
                                    (itm.transfer_qty * itm_weight) + mle_obj.qty_after_transaction)) * 100
                            new_mle.snf_per = ((mle_obj.snf_after_transaction + itm.snf_clr) / (
                                    (itm.transfer_qty * itm_weight) + mle_obj.qty_after_transaction)) * 100
                            new_mle.save(ignore_permissions=True)
                            # new_mle.submit()

def cancel_create_milk_stock_ledger(self,method):
    for itm in self.items:
        if itm.t_warehouse:
            itm_obj = frappe.get_doc("Item", itm.item_code)
            itm_weight = float(itm_obj.weight_per_unit)
            weight_uom = itm_obj.weight_uom
            maintain_snf_fat = itm_obj.maintain_fat_snf_clr
            good_cow_milk = frappe.db.get_single_value("Dairy Settings", "cow_pro")
            good_buff_milk = frappe.db.get_single_value("Dairy Settings", "buf_pro")
            good_mix_milk = frappe.db.get_single_value("Dairy Settings", "mix_pro")
            if itm.item_code == good_cow_milk or itm.item_code == good_buff_milk or itm.item_code == good_mix_milk or maintain_snf_fat == 1:
                query = """ select name from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
                                                """
                if itm.batch_no:
                    query += """ and batch_no = %(batch_no)s """
                if itm.serial_no:
                    query += """ and serial_no = %(serial_no)s """
                query += """ and voucher_type = "Stock Entry" and voucher_no = %(voucher_no)s 
                                                            and voucher_detail_no = %(voucher_detail_no)s """
                query += """ order by modified desc limit 1 """
                mle = frappe.db.sql(query, {'warehouse': itm.t_warehouse, 'item_code': itm.item_code, 'batch_no': itm.batch_no,
                                            'serial_no': itm.serial_no,"voucher_detail_no":itm.name,"voucher_no":itm.parent}, as_dict=True)


                if len(mle) > 0:
                    if mle[0]['name']:
                        mle_obj = frappe.get_doc("Milk Ledger Entry", mle[0]['name'])
                        new_mle = frappe.new_doc("Milk Ledger Entry")
                        new_mle.item_code = mle_obj.item_code
                        new_mle.serial_no = cstr(mle_obj.serial_no).strip()
                        new_mle.batch_no = mle_obj.batch_no
                        new_mle.warehouse = mle_obj.warehouse
                        new_mle.posting_date = self.posting_date
                        new_mle.posting_time = self.posting_time
                        new_mle.voucher_type = "Stock Entry"
                        new_mle.voucher_no = self.name
                        new_mle.voucher_detail_no = itm.name
                        new_mle.actual_qty = -1 * (itm.transfer_qty * itm_weight)
                        new_mle.fat = -1 * itm.fat
                        new_mle.snf = -1 * itm.snf_clr
                        new_mle.stock_uom = weight_uom
                        new_mle.qty_after_transaction = mle_obj.qty_after_transaction - (itm.transfer_qty * itm_weight)
                        new_mle.fat_after_transaction = mle_obj.fat_after_transaction - itm.fat
                        new_mle.snf_after_transaction = mle_obj.snf_after_transaction - itm.snf_clr
                        if (mle_obj.qty_after_transaction - (itm.transfer_qty * itm_weight))>0:
                            new_mle.fat_per = ((mle_obj.fat_after_transaction - itm.fat) / (mle_obj.qty_after_transaction - (itm.transfer_qty * itm_weight))) * 100
                            new_mle.snf_per = ((mle_obj.snf_after_transaction - itm.snf_clr) / (mle_obj.qty_after_transaction - (itm.transfer_qty * itm_weight))) * 100

                       
                        frappe.db.sql(""" update `tabMilk Ledger Entry` set is_cancelled = 1 where name = %(name)s """,
                                      {'name': mle_obj.name})
                        frappe.db.commit()

                        new_mle.save(ignore_permissions=True)
                        # new_mle.submit()
                        frappe.db.sql(""" update `tabMilk Ledger Entry` set is_cancelled = 1 where name = %(name)s """,
                                      {'name': new_mle.name})
                        frappe.db.commit()
                        
        

        if itm.s_warehouse:
            itm_obj = frappe.get_doc("Item", itm.item_code)
            itm_weight = float(itm_obj.weight_per_unit)
            weight_uom = itm_obj.weight_uom
            maintain_snf_fat = itm_obj.maintain_fat_snf_clr
            good_cow_milk = frappe.db.get_single_value("Dairy Settings", "cow_pro")
            good_buff_milk = frappe.db.get_single_value("Dairy Settings", "buf_pro")
            good_mix_milk = frappe.db.get_single_value("Dairy Settings", "mix_pro")
            if itm.item_code == good_cow_milk or itm.item_code == good_buff_milk or itm.item_code == good_mix_milk or maintain_snf_fat == 1:
                query = """ select name from `tabMilk Ledger Entry` where item_code = %(item_code)s and warehouse = %(warehouse)s 
                                                        """
                if itm.batch_no:
                    query += """ and batch_no = %(batch_no)s """
                if itm.serial_no:
                    query += """ and serial_no = %(serial_no)s """

                query += """ and voucher_type = "Stock Entry" and voucher_no = %(voucher_no)s 
                                                        and voucher_detail_no = %(voucher_detail_no)s """

                query += """ order by modified desc limit 1 """

                mle = frappe.db.sql(query,
                                    {'warehouse': itm.s_warehouse, 'item_code': itm.item_code, 'batch_no': itm.batch_no,
                                     'serial_no': itm.serial_no, "voucher_detail_no": itm.name,
                                     "voucher_no": itm.parent}, as_dict=True)

                if len(mle) > 0:
                    if mle[0]['name']:
                        mle_obj = frappe.get_doc("Milk Ledger Entry", mle[0]['name'])

                        new_mle = frappe.new_doc("Milk Ledger Entry")
                        new_mle.item_code = mle_obj.item_code
                        new_mle.serial_no = cstr(mle_obj.serial_no).strip()
                        new_mle.batch_no = mle_obj.batch_no
                        new_mle.warehouse = mle_obj.warehouse
                        new_mle.posting_date = self.posting_date
                        new_mle.posting_time = self.posting_time
                        new_mle.voucher_type = "Stock Entry"
                        new_mle.voucher_no = self.name
                        new_mle.voucher_detail_no = itm.name
                        new_mle.actual_qty = (itm.transfer_qty * itm_weight)
                        new_mle.fat = float(itm.fat)
                        new_mle.snf = float(itm.snf_clr)
                        new_mle.stock_uom = weight_uom
                        new_mle.qty_after_transaction = mle_obj.qty_after_transaction + (itm.transfer_qty * itm_weight)
                        new_mle.fat_after_transaction = mle_obj.fat_after_transaction + itm.fat
                        new_mle.snf_after_transaction = mle_obj.snf_after_transaction + itm.snf_clr
                        new_mle.fat_per = (float(itm.fat) / (itm.transfer_qty * itm_weight)) * 100
                        new_mle.snf_per = (float(itm.snf_clr) / (itm.transfer_qty * itm_weight)) * 100

                        frappe.db.sql(""" update `tabMilk Ledger Entry` set is_cancelled = 1 where name = %(name)s """,
                                      {'name': mle_obj.name})
                        frappe.db.commit()

                        new_mle.save(ignore_permissions=True)
                        # new_mle.submit()
                        frappe.db.sql(""" update `tabMilk Ledger Entry` set is_cancelled = 1 where name = %(name)s """,
                                      {'name': new_mle.name})
                        frappe.db.commit()
                                      
    vci = frappe.get_all('Van Collection Items',{'gate_pass':self.name},['name'])
    print('vciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    for i in vci:
        doc=frappe.get_doc("Van Collection Items",i.name)
        se_del = doc.gate_pass
        doc.db_set("gate_pass","")
        self.van_collection_item = ""
        frappe.db.sql("""DELETE FROM `tabStock Entry` where name = '{0}' """.format(se_del))
        print('se_del***********************************')

    r_lines = frappe.get_all('RMRD Lines',{'stock_entry':self.name},['name'])
    for rl in r_lines:
        doc1 = frappe.get_doc('RMRD Lines',rl.name)
        se_dlt = doc1.stock_entry
        doc1.db_set('stock_entry',"")
        self.rmrd = ""
        print('se dlt*****************************************')
        frappe.db.sql("""DELETE FROM `tabStock Entry` where name = '{0}' """.format(se_dlt))


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
            print('van collection satus *************************')

    if self.rmrd and self.rmrd_lines:
        r_lines = frappe.get_doc('RMRD Lines',self.rmrd_lines)
        if r_lines.rmrd == self.rmrd:
            rmrd = frappe.get_doc('RMRD',self.rmrd)
            rmrd.db_set('status','Completed')
            rmrd.db_update()
            print('van collection satus *************************')


def calculate_wfs(self,method):
    if self.item:
        doc=frappe.get_doc("Item",self.item)
        if doc.maintain_fat_snf_clr:
            self.required_fat=doc.standard_fat
            self.required_snf=doc.standard_snf
            self.total_fat_in_kg=(self.fg_completed_qty*doc.weight_per_unit)*doc.standard_fat/100
            self.total_snf_in_kg=(self.fg_completed_qty*doc.weight_per_unit)*doc.standard_fat/100
        

        total_rm_fat=[]
        total_rm_snf=[]
        total_fat_in_kg=[]
        total_snf_in_kg=[]
        for i in self.items:
            item=frappe.get_doc("Item",i.item_code)
            if doc.maintain_fat_snf_clr:
                total_rm_fat.append(item.standard_fat)
                total_rm_snf.append(item.standard_snf)
                total_fat_in_kg.append((i.qty*item.weight_per_unit)*item.standard_fat/100)
                total_snf_in_kg.append((i.qty*item.weight_per_unit)*item.standard_snf/100)
        if len(total_rm_fat)>0:
            self.total_rm_fat=sum(total_rm_fat)/len(self.items)

        if len(total_rm_snf)>0:
            self.total_rm_snf=sum(total_rm_snf)/len(self.items)
        if len(total_fat_in_kg)>0:
            self.total_rm_fats_in_kg=sum(total_fat_in_kg)
        if len(total_snf_in_kg)>0:
            self.total_rm_snfs_in_kg=sum(total_snf_in_kg)
        

        self.total_diff_fat=self.required_fat- self.total_rm_fat
        self.total_diff_snf=self.required_snf-self.total_diff_snf
        self.total_diff_fat_in_kg=self.total_fat_in_kg-self.total_rm_fats_in_kg
        self.total_diff_snf_in_kg=self.total_snf_in_kg-self.total_rm_snfs_in_kg


    



@frappe.whitelist()
def get_add_fat(name):
    doc=frappe.get_doc("Dairy Settings")
    items=[]
    for i in doc.items_to_add_fat:
        doc=frappe.get_doc("Item",i.item)
        items.append({"item_code":doc.name,"item_name":doc.item_name,"qty":1,"uom":doc.stock_uom,
                      "fat":doc.standard_fat,"snf":doc.standard_snf,
                      "total_fat_in_kg":(1*doc.weight_per_unit)*doc.standard_fat/100,"total_snf_in_kg":(1*doc.weight_per_unit)*doc.standard_fat/100})
    return items
        
        
@frappe.whitelist()
def get_add_snf(name):
    doc=frappe.get_doc("Dairy Settings")
    items=[]
    for i in doc.items_to_add_fat:
        doc=frappe.get_doc("Item",i.item)
        items.append({"item_code":doc.name,"item_name":doc.item_name,"qty":1,"uom":doc.stock_uom,
                      "fat":doc.standard_fat,"snf":doc.standard_snf,
                      "total_fat_in_kg":(1*doc.weight_per_unit)*doc.standard_fat/100,"total_snf_in_kg":(1*doc.weight_per_unit)*doc.standard_fat/100})
    return items
        
@frappe.whitelist()
def get_remove_snf(name):
    doc=frappe.get_doc("Dairy Settings")
    items=[]
    for i in doc.items_to_add_fat:
        doc=frappe.get_doc("Item",i.item)
        items.append({"item_code":doc.name,"item_name":doc.item_name,"qty":1,"uom":doc.stock_uom,
                      "fat":doc.standard_fat,"snf":doc.standard_snf,
                      "total_fat_in_kg":(1*doc.weight_per_unit)*doc.standard_fat/100,"total_snf_in_kg":(1*doc.weight_per_unit)*doc.standard_fat/100})
    return items
        

@frappe.whitelist()
def get_remove_fat(name):
    doc=frappe.get_doc("Dairy Settings")
    items=[]
    for i in doc.items_to_add_fat:
        doc=frappe.get_doc("Item",i.item)
        items.append({"item_code":doc.name,"item_name":doc.item_name,"qty":1,"uom":doc.stock_uom,
                      "fat":doc.standard_fat,"snf":doc.standard_snf,
                      "total_fat_in_kg":(1*doc.weight_per_unit)*doc.standard_fat/100,"total_snf_in_kg":(1*doc.weight_per_unit)*doc.standard_fat/100})
    return items
        


@frappe.whitelist()
def append_item(values,name):
    se=frappe
    pass
