from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def calculate_crate(doc_name = None):
    if doc_name:
        doc = frappe.get_doc("Delivery Note",doc_name)
        # add_crate_count_item_line(doc)
        frappe.db.sql("delete from `tabCrate Count Child` where parent = %s",(doc.name))
        doc = frappe.get_doc("Delivery Note", doc_name)
        dict_create_type = dict()
        dist_itm = list(frappe.db.sql("""select distinct(item_code) from `tabDelivery Note Item` where parent= %(parent)s """,{'parent':doc.name}))
        print("**************************************************",dist_itm)
        for i in range(0,len(dist_itm)):
            overage_details = frappe.get_doc("Item",dist_itm[i][0])
            overage = overage_details.crate_overage
            has_batch_no = overage_details.has_batch_no
            print("##################################################",overage)
            dist_warehouse = list(frappe.db.sql("""select distinct(warehouse) from `tabDelivery Note Item` where item_code= %(item_code)s """,
                                           {'item_code':dist_itm[i]}))
            print("##################################",dist_warehouse)
            for j in range(0,len(dist_warehouse)):
                if has_batch_no == 1:
                    dist_batch_no = list(frappe.db.sql(
                        """select distinct(batch_no) from `tabDelivery Note Item` where warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s """,
                                                {'warehouse':dist_warehouse[j],'item_code':dist_itm[i],'doc_name':doc_name}))
                    for k in range(0, len(dist_batch_no)):
                        total_qty = frappe.db.sql(""" select sum(stock_qty) from `tabDelivery Note Item` where
                                                        is_free_item = 0 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s and batch_no = %(batch_no)s""",
                                                   {'warehouse':dist_warehouse[j],'item_code':dist_itm[i],'doc_name':doc_name,'batch_no':dist_batch_no[k]})

                        free_qty = 0
                        free_qty_list = frappe.db.sql(""" select sum(stock_qty) from `tabDelivery Note Item` where
                                                                               is_free_item = 1 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s and batch_no = %(batch_no)s""",
                                                  {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i],
                                                   'doc_name': doc_name, 'batch_no': dist_batch_no[k]})
                        if free_qty_list:
                            free_qty = free_qty_list[0][0]
                        print("total qty",total_qty,dist_warehouse[j],dist_itm[i],doc_name)
                        ttl_qty = str(total_qty[0][0])
                        print(ttl_qty)
                        if ttl_qty != "None":
                            crate_details = frappe.db.sql(""" select crate_quantity,crate_type from `tabCrate` where parent = %(item_code)s and
                                                                warehouse = %(warehouse)s limit 1 """,{'item_code':dist_itm[i],'warehouse':dist_warehouse[j]})
                            print("000000000000000000000000000000000000000",crate_details)
                            if len(crate_details) > 0:

                                doc.append('crate_count', {
                                                    'crate_type': crate_details[0][1],
                                                    'outgoing_count': int(round((total_qty[0][0] / int((crate_details[0][0])* (1 + overage/100))), 2)),
                                                    'item_code': dist_itm[i],
                                                    'item_name': overage_details.item_name,
                                                    'qty': total_qty[0][0],
                                                    'batch_no': dist_batch_no[k],
                                                    'uom': overage_details.stock_uom,
                                                    'free_qty': free_qty,
                                                    # 'outgoing_count': int(total_qty[0][0]) / int((crate_details[0][0]) * (1 + (overage/100)))
                                                })
                                doc.append('loose_crate_', {
                                    'crate_type': crate_details[0][1],
                                    'qty': int(round((total_qty[0][0] % int(((crate_details[0][0]) * (1 + overage/100)))), 2))
                                })

            #                 free items
            #             total_qty = frappe.db.sql(""" select sum(stock_qty) from `tabDelivery Note Item` where
            #                             is_free_item = 1 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s and batch_no = %(batch_no)s""",
            #                                       {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i],
            #                                        'doc_name': doc_name, 'batch_no': dist_batch_no[k]})
            #             print("total qty", total_qty, dist_warehouse[j], dist_itm[i], doc_name)
            #             ttl_qty = str(total_qty[0][0])
            #             print(ttl_qty)
            #             if ttl_qty != "None":
            #                 crate_details = frappe.db.sql(""" select crate_quantity,crate_type from `tabCrate` where parent = %(item_code)s and
            #                                                                         warehouse = %(warehouse)s limit 1 """,
            #                                               {'item_code': dist_itm[i], 'warehouse': dist_warehouse[j]})
            #                 print("000000000000000000000000000000000000000", crate_details)
            #                 if len(crate_details) > 0:
            #                     doc.append('crate_count', {
            #                         'free_qty': total_qty[0][0],
            #                         'item_code': dist_itm[i],
            #                         'item_name': overage_details.item_name,
            #                         'qty': total_qty[0][0],
            #                         'batch_no': dist_batch_no[k],
            #                         'uom': overage_details.stock_uom
            #                         # 'outgoing_count': int(round((total_qty[0][0] / int((crate_details[0][0]) * (1 + overage / 100))), 2))
            #                         # 'outgoing_count': int(total_qty[0][0]) / int((crate_details[0][0]) * (1 + (overage/100)))
            #                     })
                elif has_batch_no == 0:
                    free_qty = 0
                    free_qty_list = frappe.db.sql(""" select sum(stock_qty) from `tabDelivery Note Item` where is_free_item = 1 and 
                    warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s""",
                                        {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i], 'doc_name': doc_name})
                    if free_qty_list:
                        free_qty = free_qty_list[0][0]

                    total_qty = frappe.db.sql(""" select sum(stock_qty) from `tabDelivery Note Item` where
                                                    is_free_item = 0 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s""",
                                              {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i],
                                               'doc_name': doc_name})
                    print("total qty", total_qty, dist_warehouse[j], dist_itm[i], doc_name)
                    ttl_qty = str(total_qty[0][0])
                    print(ttl_qty)
                    if ttl_qty != "None":
                        crate_details = frappe.db.sql(""" select crate_quantity,crate_type from `tabCrate` where parent = %(item_code)s and
                                                            warehouse = %(warehouse)s limit 1 """,
                                                      {'item_code': dist_itm[i],
                                                       'warehouse': dist_warehouse[j]})
                        print("000000000000000000000000000000000000000", crate_details)
                        if len(crate_details) > 0:
                            doc.append('crate_count', {
                                'crate_type': crate_details[0][1],
                                'outgoing_count': int(
                                    round((total_qty[0][0] / int((crate_details[0][0]) * (1 + overage / 100))),
                                          2)),
                                'item_code': dist_itm[i],
                                'item_name': overage_details.item_name,
                                'qty': total_qty[0][0],
                                'uom': overage_details.stock_uom,
                                'free_qty': free_qty,
                                # 'outgoing_count': int(total_qty[0][0]) / int((crate_details[0][0]) * (1 + (overage/100)))
                            })
                            doc.append('loose_crate_', {
                                'crate_type': crate_details[0][1],
                                'qty': int(round(
                                    (total_qty[0][0] % int(((crate_details[0][0]) * (1 + overage / 100)))), 2))
                            })



                    #                 free items
                    # total_qty = frappe.db.sql(""" select sum(stock_qty) from `tabDelivery Note Item` where
                    #                                                     is_free_item = 1 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s""",
                    #                           {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i],
                    #                            'doc_name': doc_name})
                    # print("total qty", total_qty, dist_warehouse[j], dist_itm[i], doc_name)
                    # ttl_qty = str(total_qty[0][0])
                    # print(ttl_qty)
                    # if ttl_qty != "None":
                    #     crate_details = frappe.db.sql(""" select crate_quantity,crate_type from `tabCrate` where parent = %(item_code)s and
                    #                                                             warehouse = %(warehouse)s limit 1 """,
                    #                                   {'item_code': dist_itm[i],
                    #                                    'warehouse': dist_warehouse[j]})
                    #     print("000000000000000000000000000000000000000", crate_details)
                    #     if len(crate_details) > 0:
                    #         doc.append('crate_count', {
                    #             'free_qty': total_qty[0][0],
                    #             'item_code': dist_itm[i],
                    #             'item_name': overage_details.item_name,
                    #             'qty': total_qty[0][0],
                    #             'uom': overage_details.stock_uom
                    #             # 'outgoing_count': int(round((total_qty[0][0] / int((crate_details[0][0]) * (1 + overage / 100))), 2))
                    #             # 'outgoing_count': int(total_qty[0][0]) / int((crate_details[0][0]) * (1 + (overage/100)))
                    #         })


        # for itm in doc.items:
        #     count = 0
        #     crate_count = frappe.get_doc("Item",itm.item_code)
        #     for itms in crate_count.crate:
        #         if itm.warehouse == itms.warehouse and count == 0:
        #             if itms.crate_quantity and itms.crate_type:
        #                 doc.append('crate_count', {
        #                     'crate_type': itms.crate_type,
        #                     'outgoing_count': int(round((itm.stock_qty / (itms.crate_quantity)),2))
        #                 })
        #                 count = 1
        #
        doc.save(ignore_permissions=True)
        return dict_create_type


# @frappe.whitelist()
# def calculate_crate_after_insert(doc, method):
#     if not doc.get("__islocal"):
#         doc = frappe.get_doc("Delivery Note",doc.name)
#         frappe.db.sql("delete from `tabCrate Count Child` where parent = %s",(doc.name))
#
#         # doc = frappe.get_doc("Delivery Note", doc.name)
#     add_crate_count_item_line(doc)
#     dict_create_type = {}
#     for itm in doc.items:
#         count = 0
#         crate_count = frappe.get_doc("Item", itm.item_code)
#         for itms in crate_count.crate:
#             if itm.warehouse == itms.warehouse and count == 0:
#                 if itms.crate_quantity and itms.crate_type:
#                     doc.append('crate_count', {
#                         'crate_type': itms.crate_type,
#                         'outgoing_count': int(round((itm.stock_qty / (itms.crate_quantity)), 2))
#                     })
#                     count = 1
    # doc.save(ignore_permissions=True)
    # return dict_create_type
    # doc.db_update()

def add_crate_count_item_line(doc):
    if doc:
        for itm in doc.items:
            crate_count = frappe.get_doc("Item", itm.item_code)
            overage = 0
            if crate_count.allow_crate_overage and crate_count.crate_overage:
                overage = crate_count.crate_overage
            # qty = round((itm.qty / (crate_count.crate_quantity * (1 + overage / 100))),2)
            qty = 0
            for itms in crate_count.crate:
                count = 0
                if itm.warehouse == itms.warehouse and count == 0:
                    if itms.crate_quantity:
                        qty = int(round((itm.stock_qty / (itms.crate_quantity)),2))
                    if 0 < qty < 1:
                        qty =1.0
                    itm.crate_count = float(((str(qty) + ".").split("."))[0])
                    itm.crate_type = crate_count.crate_type
                    count =1
            # itm.db_update()

@frappe.whitelist()
def route_validation(obj, method):
    doc = frappe.get_doc(obj)
    item_code_lst = ['0000']
    for i in doc.items:
        item_code_lst.append(i.item_code)
    query = """select TIG.route_required,TI.name from `tabItem Group` TIG 
                inner join `tabItem` TI on TIG.name =TI.item_group 
                where route_required != 0 and TI.name in {0} """.format(tuple(item_code_lst))
    result = frappe.db.sql(query)
    if result and not doc.route:
        frappe.throw(_("Please select route is Mandatory"))

@frappe.whitelist()
def get_route_price_list(doc_name=None):
    if doc_name:
        route_name = frappe.db.sql("""select link_name from `tabDynamic Link` 
                                where parenttype ='Customer'  
                                and link_doctype ='Route Master' 
                                and parent =%s limit 1""",(doc_name))
        if route_name:
            dic ={}
            doc = frappe.get_doc("Route Master",route_name[0][0])
            dic['route'] = doc.name
            dic['p_list'] = doc.price_list
            dic['warehouse'] = doc.source_warehouse
            return dic
        return  False

@frappe.whitelist()
def get_route_price_list_route(doc_name=None):
    if doc_name:
        route_name = frappe.db.sql("""select parent from `tabDynamic Link`
                                where parenttype ='Customer'
                                and link_doctype ='Route Master'
                                and link_name =%s limit 1""",(doc_name))
        print("*************",route_name)
        if route_name:
            dic = {}
            dic['route'] = route_name[0][0]
            return dic
        return False

@frappe.whitelist()
def delivery_shift(name=None):
    shift = frappe.db.sql("""select delivery_shift from `tabSales Order` where name = %(name)s""",{'name':name})
    return shift


# @frappe.whitelist()
# def make_delivery_trip(source_name, target_doc=None):
# 	def update_stop_details(source_doc, target_doc, source_parent):
# 		target_doc.customer = source_parent.customer
# 		target_doc.address = source_parent.shipping_address_name
# 		target_doc.customer_address = source_parent.shipping_address
# 		target_doc.contact = source_parent.contact_person
# 		target_doc.customer_contact = source_parent.contact_display
# 		target_doc.route = source_parent.route
#
#
# 		# Append unique Delivery Notes in Delivery Trip
# 		delivery_notes.append(target_doc.delivery_note)
#
#
# 	delivery_notes = []
#
#
# 	doclist = get_mapped_doc("Delivery Note", source_name, {
# 		"Delivery Note": {
# 			"doctype": "Delivery Trip",
# 			"validation": {
# 				"docstatus": ["=", 1]
# 			}
# 		},
# 		"Delivery Note Item": {
# 				"doctype": "Delivery Stop",
# 			"field_map": {
# 				"parent": "delivery_note",
#
# 			},
# 			"condition": lambda item: item.parent in delivery_notes,
# 			"postprocess": update_stop_details
# 		},
#         "Delivery Note Item": {
#             "doctype": "Delivery Note Details",
#             "field_map": {
#                 "parent": "delivery_note",
#                 "qty": "quantity",
#                 "route": "route"
#             },
#             # "condition": lambda item: item.parent not in delivery_notes,
#             "postprocess": update_stop_details
#         },
# 	}, target_doc,ignore_permissions=True)
#
# 	return doclist

