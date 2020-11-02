from __future__ import unicode_literals
import frappe
from frappe import _

def change_milk_entry_status(pc,method):
    if pc.milk_entry:
        doc = frappe.get_doc("Milk Entry",pc.milk_entry)
        res = frappe.db.sql(""" select docstatus from `tabRaw Milk Sample` where name in 
                                (Select distinct(parent) from `tabSample lines`  where milk_entry =%s) limit 1""",(doc.name))
        if res:
            if res[0][0] ==1 and doc.sample_created:
                doc.status = "To Post"
            elif res[0][0] ==0 and doc.sample_created:
                doc.status ="To Post and Sample"
            else:
                doc.status = "To Post and Sample"
        else:
            doc.status = "To Post and Sample"
        doc.db_update()

def change_milk_status(pc,method):
    if pc.milk_entry:
        doc = frappe.get_doc("Milk Entry",pc.milk_entry)
        res = frappe.db.sql("""select docstatus from `tabRaw Milk Sample` where name in 
                                (Select distinct(parent) from `tabSample lines`  where milk_entry =%s) limit 1""",(doc.name))
        if res:
            if res[0][0] ==1 and doc.sample_created:
                doc.status = "Posted"
            elif res[0][0] == 1 and not doc.sample_created:
                doc.status = "Posted"
            else:
                doc.status ="To Sample"
        else:
            doc.status = "To Sample"
        doc.db_update()

# def update_snf(pc,method):
#     for itm in pc.items:
#         # sle = frappe.db.sql(""" select count(name) from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt" """)
#         sle = frappe.db.sql(""" select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
#                             and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled != 1
#                              order by modified desc  """,
#                             {'name': pc.name,'c_name': itm.name,'batch_no':itm.batch_no, 'serial_no':itm.serial_no},as_dict=True)
#         print("******************************************************",sle)
#         if sle[0]['name']:
#             doc = frappe.get_doc("Stock Ledger Entry",sle[0]['name'])
#             doc.actual_snf = itm.clr
#             f_slv = frappe.db.sql(""" select actual_snf_after_transaction from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
#                                      and item_code = %(item_code)s and warehouse = %(warehouse)s and name != %(name)s
#                                     order by modified desc """,
#                                 {'item_code': itm.item_code,"warehouse": itm.warehouse,'name':sle[0]['name']}, as_dict=True)
#             print("**********************************************************",f_slv)
#             if f_slv:
#                 if float(f_slv[0]['actual_snf_after_transaction']) > 0.0:
#                     doc.actual_snf_after_transaction = f_slv[0]['actual_snf_after_transaction'] + itm.clr
#                 else:
#                     doc.actual_snf_after_transaction = itm.clr
#             doc.save(ignore_permissions=True)

def update_snf(pc,method):
    for itm in pc.items:
        query = """ select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
                            and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled != 1 """
        if itm.batch_no:
            query += """ and batch_no = %(batch_no)s """
        if itm.serial_no:
            query += """ and serial_no = %(serial_no)s """

        query += """ order by modified desc """
        sle = frappe.db.sql(query,{'name': pc.name,'c_name': itm.name,'batch_no':itm.batch_no, 'serial_no':itm.serial_no},as_dict=True)
        if sle[0]['name']:
            doc = frappe.get_doc("Stock Ledger Entry",sle[0]['name'])
            doc.actual_snf = itm.clr
            query2 = """ select actual_snf_after_transaction from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
                                     and item_code = %(item_code)s and warehouse = %(warehouse)s and name != %(name)s
                                     """
            if itm.batch_no:
                query2 += """ and batch_no = %(batch_no)s """
            if itm.serial_no:
                query2 += """ and serial_no = %(serial_no)s """

            query2 += """ order by modified desc """
            f_slv = frappe.db.sql(query2,{'item_code': itm.item_code,"warehouse": itm.warehouse,'name':sle[0]['name'],'batch_no':itm.batch_no, 'serial_no':itm.serial_no}
                                  , as_dict=True)

            print("**********************************************************",f_slv)
            if f_slv:
                if float(f_slv[0]['actual_snf_after_transaction']) > 0.0:
                    doc.actual_snf_after_transaction = f_slv[0]['actual_snf_after_transaction'] + itm.clr
                else:
                    doc.actual_snf_after_transaction = itm.clr
            doc.save(ignore_permissions=True)


# def update_fat(pc,method):
#     for itm in pc.items:
#         # sle = frappe.db.sql(""" select count(name) from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt" """)
#         sle = frappe.db.sql(""" select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
#                             and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled != 1
#                              order by modified desc  """,
#                             {'name': pc.name,'c_name': itm.name},as_dict=True)
#         print("******************************************************",sle)
#         if sle[0]['name']:
#             doc = frappe.get_doc("Stock Ledger Entry",sle[0]['name'])
#             doc.actual_fat = itm.fat
#             f_slv = frappe.db.sql(""" select actual_fat_after_transaction from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
#                                      and item_code = %(item_code)s and warehouse = %(warehouse)s and name != %(name)s
#                                     order by modified desc """,
#                                 {'item_code': itm.item_code,"warehouse": itm.warehouse,'name':sle[0]['name']}, as_dict=True)
#             print("**********************************************************",f_slv)
#             if f_slv:
#                 if float(f_slv[0]['actual_fat_after_transaction']) > 0.0:
#                     doc.actual_fat_after_transaction = f_slv[0]['actual_fat_after_transaction'] + itm.fat
#                 else:
#                     doc.actual_fat_after_transaction = itm.fat
#             doc.save(ignore_permissions=True)

def update_fat(pc,method):
    for itm in pc.items:
        query = """ select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
                                    and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled != 1 """
        if itm.batch_no:
            query += """ and batch_no = %(batch_no)s """
        if itm.serial_no:
            query += """ and serial_no = %(serial_no)s """

        query += """ order by modified desc """
        sle = frappe.db.sql(query,
                            {'name': pc.name, 'c_name': itm.name, 'batch_no': itm.batch_no, 'serial_no': itm.serial_no},
                            as_dict=True)
        if sle[0]['name']:
            doc = frappe.get_doc("Stock Ledger Entry",sle[0]['name'])
            doc.actual_fat = itm.fat
            query2 = """ select actual_fat_after_transaction from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
                                     and item_code = %(item_code)s and warehouse = %(warehouse)s and name != %(name)s
                                    """
            if itm.batch_no:
                query2 += """ and batch_no = %(batch_no)s """
            if itm.serial_no:
                query2 += """ and serial_no = %(serial_no)s """

            query2 += """ order by modified desc """
            f_slv = frappe.db.sql(query2,{'item_code': itm.item_code,"warehouse": itm.warehouse,'name':sle[0]['name'],
                                          'batch_no':itm.batch_no, 'serial_no':itm.serial_no}, as_dict=True)

            print("**********************************************************",f_slv)
            if f_slv:
                if float(f_slv[0]['actual_fat_after_transaction']) > 0.0:
                    doc.actual_fat_after_transaction = f_slv[0]['actual_fat_after_transaction'] + itm.fat
                else:
                    doc.actual_fat_after_transaction = itm.fat
            doc.save(ignore_permissions=True)

def cancel_update_snf(pc,method):
    for itm in pc.items:
        # sle = frappe.db.sql(""" select count(name) from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt" """)
        query = """ select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
                            and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled = 1 """
        if itm.batch_no:
            query += """ and batch_no = %(batch_no)s """
        if itm.serial_no:
            query += """ and serial_no = %(serial_no)s """

        query += """ order by modified desc """

        sle = frappe.db.sql(query,{'name': pc.name,'c_name': itm.name,'batch_no':itm.batch_no, 'serial_no':itm.serial_no},as_dict=True)
                            # {'name': pc.name,'c_name': itm.name,'batch_no':itm.batch_no, 'serial_no':itm.serial_no},as_dict=True)
        print("******************************************************",sle)
        if sle[1]['name']:
            doc = frappe.get_doc("Stock Ledger Entry",sle[1]['name'])
            new_actual_snf = 0 - float(doc.actual_snf)
            new_tran_snf = float(doc.actual_snf_after_transaction) - float(doc.actual_snf)

            query2 = """ select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
                                         and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled = 1
                                          """
            if itm.batch_no:
                query2 += """ and batch_no = %(batch_no)s """
            if itm.serial_no:
                query2 += """ and serial_no = %(serial_no)s """

            query2 += """ order by modified desc limit 1 """
            # u_sle = frappe.db.sql(""" select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
            #                             and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled = 1
            #                             order by modified desc limit 1 """,
            #                     {'name': pc.name, 'c_name': itm.name}, as_dict=True)
            u_sle = frappe.db.sql(query2,{'name': pc.name, 'c_name': itm.name,'batch_no':itm.batch_no, 'serial_no':itm.serial_no}, as_dict=True)
            print("*****************************************u_sale*************", u_sle)
            if u_sle:
                if u_sle[0]['name']:
                    u_doc = frappe.get_doc("Stock Ledger Entry", u_sle[0]['name'])
                    u_doc.actual_snf = new_actual_snf
                    u_doc.actual_snf_after_transaction = new_tran_snf
                    u_doc.save(ignore_permissions=True)

def cancel_update_fat(pc,method):
    for itm in pc.items:

        # sle = frappe.db.sql(""" select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
        #                     and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled = 1 order by modified desc""",
        #                     {'name': pc.name,'c_name': itm.name},as_dict=True)
        query = """ select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
                  and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled = 1 """
        if itm.batch_no:
            query += """ and batch_no = %(batch_no)s """
        if itm.serial_no:
            query += """ and serial_no = %(serial_no)s """

        query += """ order by modified desc"""
        sle = frappe.db.sql(query,{'name': pc.name,'c_name': itm.name,'batch_no':itm.batch_no, 'serial_no':itm.serial_no},as_dict=True)
        print("******************************************************",sle)
        if sle[1]['name']:
            doc = frappe.get_doc("Stock Ledger Entry",sle[1]['name'])
            new_actual_fat = 0 - float(doc.actual_fat)
            new_tran_fat = float(doc.actual_fat_after_transaction) - float(doc.actual_fat)

            # u_sle = frappe.db.sql(""" select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
            #                             and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled = 1
            #                             order by modified desc limit 1 """,
            #                     {'name': pc.name, 'c_name': itm.name}, as_dict=True)
            query2 = """ select name from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt"
                                         and voucher_no = %(name)s and voucher_detail_no = %(c_name)s and is_cancelled = 1
                                          """
            if itm.batch_no:
                query2 += """ and batch_no = %(batch_no)s """
            if itm.serial_no:
                query2 += """ and serial_no = %(serial_no)s """

            query2 += """ order by modified desc limit 1 """
            u_sle = frappe.db.sql(query2,{'name': pc.name, 'c_name': itm.name,'batch_no':itm.batch_no, 'serial_no':itm.serial_no}, as_dict=True)
            print("*****************************************u_sale*************", u_sle)
            if u_sle:
                if u_sle[0]['name']:
                    u_doc = frappe.get_doc("Stock Ledger Entry", u_sle[0]['name'])
                    u_doc.actual_fat = new_actual_fat
                    u_doc.actual_fat_after_transaction = new_tran_fat
                    u_doc.save(ignore_permissions=True)



