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
                        if not mle:
                            frappe.throw("Milk Ledger Entry Not Found For This Item")
                        if mle[0]['name']:
                            mle_obj = frappe.get_doc("Milk Ledger Entry",mle[0]['name'])
                            print('mle_obj*************************',mle_obj)
                            itm.fat = (mle_obj.fat_per / 100) * (itm.transfer_qty * itm_weight)
                            itm.fat_per = mle_obj.fat_per
                            itm.snf_clr = (mle_obj.snf_per / 100) * (itm.transfer_qty * itm_weight)
                            itm.snf_clr_per = mle_obj.snf_per

                        # rate
                        if milk_type != "":
                            
                            query2 = frappe.db.sql(""" select bmpl.name, bmpl.rate, bmpl.snf_clr_rate 
                                                    from `tabBulk Milk Price List` bmpl, `tabBulk Milk Price List Warehouse` bmplw, `tabBulk Milk Price List Customer` bmplc
                                                    where bmplw.warehouse = %(warehouse)s and bmpl.active = 1 and bmpl.milk_type = %(milk_type)s 
                                                    and bmplc.customer = %(customer)s and bmpl.name = bmplc.parent and bmpl.name = bmplw.parent
                                                    and bmpl.docstatus =1 
                                                    order by bmpl.modified desc limit 1 """,
                                                {'warehouse':itm.s_warehouse,'milk_type':milk_type,'customer':self.customer},
                                                    as_dict=True)
                            if not query2:
                                query3 = frappe.db.sql(""" select bmpl.name, bmpl.rate, bmpl.snf_clr_rate 
                                                                            from `tabBulk Milk Price List` bmpl, `tabBulk Milk Price List Warehouse` bmplw, `tabBulk Milk Price List Customer` bmplc
                                                                            where bmplw.warehouse = %(warehouse)s and bmpl.active = 1 and bmpl.milk_type = %(milk_type)s 
                                                                            and bmpl.name = bmplw.parent and bmpl.docstatus =1 order by bmpl.modified desc limit 1 """,
                                                    {'warehouse': itm.s_warehouse, 'milk_type': milk_type,
                                                        'customer': self.customer},
                                                    as_dict=True)
                                if not query3:
                                    frappe.throw("No Rate Specified in Bulk Milk Price List")
                                else:
                                    itm.rate = (((itm.fat_per * query3[0]['rate']) + (
                                                itm.snf_clr_per * query3[0]['snf_clr_rate'])) /  (itm.transfer_qty * itm_weight))
                            else:
                                itm.rate = (((itm.fat_per * query2[0]['rate']) + (itm.snf_clr_per * query2[0]['snf_clr_rate'])) /  (itm.transfer_qty * itm_weight))



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
    for i in vci:
        doc=frappe.get_doc("Van Collection Items",i.name)
        doc.db_set("gate_pass","")
@frappe.whitelist()
def get_item_weight(item_code):
    obj = frappe.get_doc("Item",item_code)
    return obj.weight_per_unit


