from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt,cint, cstr, getdate

def before_submit(self,method):
    if frappe.db.get_single_value("Dairy Settings", "crate_reconciliation_based_on") == "Sales Invoice":
        dist_cratetype = frappe.db.sql(""" select distinct(crate_type) 
                                           from `tabCrate Count Child` 
    	                                   where parent = %(name)s""", {'name': self.name})

        for crate in dist_cratetype:
            dist_warehouse = frappe.db.sql(""" select distinct(warehouse) 
                                               from `tabCrate Count Child` 
    					                        where parent = %(name)s and crate_type = %(crate_type)s """,
                                                       {'name': self.name, 'crate_type': crate})

            for warehouse in dist_warehouse:
                sums = frappe.db.sql(""" select 
                                            sum(outgoing_count) as crate, sum(incoming_count) as crate_ret, sum(damaged_count) as damaged_crate
    			                          from 
    			                            `tabCrate Count Child` 
    			                          where 
    			                                crate_type = %(crate)s and parent = %(name)s and warehouse = %(warehouse)s""",
                                                {'crate': crate, 'name': self.name, 'warehouse': warehouse}, as_dict=1)
                log = frappe.new_doc("Crate Log")
                log.customer = self.customer
                # log.vehicle = self.vehicle
                log.route = self.route
                log.date = frappe.utils.nowdate()
                log.company = self.company
                log.voucher_type = "Sales Invoice"
                log.voucher = self.name
                log.damaged = sums[0]['damaged_crate']
                log.crate_issue = sums[0]['crate']
                log.crate_return = sums[0]['crate_ret']
                log.crate_type = crate[0]
                log.source_warehouse = warehouse[0]
                log.note = "Entry Created From Sales Invoice"

                openning_cnt = frappe.db.sql(""" select count(*) 
                                                 from `tabCrate Log`  
                                                 where crate_type = %(crate)s and source_warehouse = %(warehouse)s and company = %(company)s and  docstatus = 1	 order by date desc  """,
                                                 {'crate': crate, 'warehouse': warehouse,'company': self.company}, as_dict=1)

                if openning_cnt[0]['count(*)'] > 0:
                    openning = frappe.db.sql(""" select crate_balance 
                                                 from `tabCrate Log`  
                                                 where crate_type = %(crate)s and source_warehouse = %(warehouse)s and
    				                                    company = %(company)s and  docstatus = 1 order by date desc limit 1 """,
                                                        {'crate': crate, 'warehouse': warehouse, 'company': self.company},as_dict=1)

                    log.crate_opening = int(openning[0]['crate_balance'])
                    log.crate_balance = openning[0]['crate_balance'] - (sums[0]['crate'] + sums[0]['crate_ret'])

                else:
                    log.crate_opening = int(0)
                    log.crate_balance = int(0) - (sums[0]['crate'] + sums[0]['crate_ret'])

                log.save(ignore_permissions=True)
                log.submit()




@frappe.whitelist()
def calculate_crate(obj,method=None):
    if not obj.get("__islocal") and obj.crate_cal_done != "Done" and obj.is_return==0:
        doc_name = obj.name
        if doc_name:
            doc = frappe.get_doc("Sales Invoice",doc_name)
            # add_crate_count_item_line(doc)
            doc.crate_count=[]
            doc.loose_crate=[]
            frappe.db.sql("delete from `tabCrate Count Child` where parent = %s",(doc.name))
            frappe.db.sql("delete from `tabLoose Crate` where parent = %s", (doc.name))
            dict_create_type = dict()
            dist_itm = list(frappe.db.sql("""select 
                                                distinct(item_code) 
                                            from 
                                                `tabSales Invoice Item` 
                                            where 
                                                parent= %(parent)s """,{'parent':doc.name}))
            total_supp_qty = 0
            total_crate_qty = 0
            total_free_qty = 0

            for i in range(0,len(dist_itm)):
                print('range***********************',dist_itm)
                overage_details = frappe.get_doc("Item",dist_itm[i][0])
                overage = overage_details.crate_overage
                has_batch_no = overage_details.has_batch_no
                dist_warehouse = list(frappe.db.sql("""select 
                                                            distinct(warehouse) 
                                                        from 
                                                            `tabSales Invoice Item` 
                                                        where 
                                                            item_code= %(item_code)s """,{'item_code':dist_itm[i]}))
                


                for j in range(0,len(dist_warehouse)):
                    print('Batch no^^^^^^^^^^^^^^^^^^^^^^^^^^',dist_warehouse)
                    if has_batch_no == 1:
                        dist_batch_no = list(frappe.db.sql("""select 
                                                                distinct(batch_no) 
                                                              from 
                                                                `tabSales Invoice Item` 
                                                              where 
                                                                warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s """,
                                                                {'warehouse':dist_warehouse[j],'item_code':dist_itm[i],'doc_name':doc_name}))
                        for k in range(0, len(dist_batch_no)):
                            print('total qty&&&&&&&&&&&&&&&&&&&&&&',dist_batch_no)
                            total_qty = frappe.db.sql(""" select 
                                                                sum(stock_qty) 
                                                          from 
                                                                `tabSales Invoice Item` 
                                                          where
                                                                is_free_item = 0 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s and batch_no = %(batch_no)s""",
                                                                {'warehouse':dist_warehouse[j],'item_code':dist_itm[i],'doc_name':doc_name,'batch_no':dist_batch_no[k]})
                            print('total qty@@@@@@@@@@@@@@@@@@@@@@@',total_qty)
                            free_qty = 0
                            free_qty_list = frappe.db.sql(""" select 
                                                                    sum(stock_qty) 
                                                               from 
                                                                    `tabSales Invoice Item` 
                                                               where
                                                                    is_free_item = 1 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s and batch_no = %(batch_no)s""",
                                                                    {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i],'doc_name': doc_name, 'batch_no': dist_batch_no[k]})
                            if str(free_qty_list[0][0]) != "None":
                                free_qty = int(free_qty_list[0][0])

                            ttl_qty = str(total_qty[0][0])
                            print('ttl &&&&&&&&&&&&&&&&&&&&&',ttl_qty)
                            if ttl_qty != "None":
                                print('ttl qty**********************************',dist_warehouse[j],dist_itm[i])
                                crate_details = frappe.db.sql(""" select 
                                                                        crate_quantity,crate_type 
                                                                  from 
                                                                        `tabCrate` 
                                                                  where 
                                                                        parent = %(item_code)s and warehouse = %(warehouse)s limit 1 """,
                                                                        {'item_code':dist_itm[i],'warehouse':dist_warehouse[j]})


                                print('AAAAAAAAAAAAAAAAAAAAAAA',crate_details)
                                if len(crate_details) > 0:
                                    print('kkkkkkkkkkkkkkkkkkkkkkkk',len(crate_details))
                                    doc.append('crate_count', {
                                                        'crate_type': crate_details[0][1],
                                                        'outgoing_count': int(round(((total_qty[0][0] + free_qty) / int((crate_details[0][0])* (1 + overage/100))), 2)),
                                                        'item_code': dist_itm[i],
                                                        'item_name': overage_details.item_name,
                                                        'qty': total_qty[0][0],
                                                        'batch_no': dist_batch_no[k],
                                                        'uom': overage_details.stock_uom,
                                                        'free_qty': free_qty,
                                                        'warehouse': dist_warehouse[j][0]
                                                        # 'outgoing_count': int(total_qty[0][0]) / int((crate_details[0][0]) * (1 + (overage/100)))
                                                    })
                                    print('crate count append^^^^^^^^^^^^^^^^^',crate_details[0][1],int(round(((total_qty[0][0] + free_qty) / int((crate_details[0][0])* (1 + overage/100))), 2)),
                                          dist_itm[i], total_qty[0][0], dist_warehouse[j][0])
                                    total_supp_qty += total_qty[0][0]
                                    total_crate_qty += int(round(((total_qty[0][0] + free_qty) / int((crate_details[0][0])* (1 + overage/100))), 2))
                                    str_free_qty = str(free_qty)

                                    if (str_free_qty != "None"):
                                        total_free_qty += int(free_qty)

                                    qty = int(round(((total_qty[0][0] + free_qty) % int(((crate_details[0][0]) * (1 + overage/100)))), 2))

                                    if qty > 0:
                                        doc.append('loose_crate', {
                                            'item_code': dist_itm[i][0],
                                            'crate_type': crate_details[0][1],
                                            'qty': int(round(((total_qty[0][0] + free_qty) % int(((crate_details[0][0]) * (1 + overage/100)))), 2))
                                        })

                    elif has_batch_no == 0:
                        free_qty = 0
                        free_qty_list = frappe.db.sql(""" select 
                                                                sum(stock_qty) 
                                                          from 
                                                                `tabSales Invoice Item` 
                                                          where 
                                                                is_free_item = 1 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s""",
                                                                {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i], 'doc_name': doc_name})

                        if str(free_qty_list[0][0]) != "None":
                            free_qty = free_qty_list[0][0]

                        total_qty = frappe.db.sql(""" select 
                                                            sum(stock_qty) 
                                                      from 
                                                            `tabSales Invoice Item` 
                                                      where
                                                        is_free_item = 0 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s""",
                                                        {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i],'doc_name': doc_name})

                        ttl_qty = str(total_qty[0][0])

                        if ttl_qty != "None":
                            crate_details = frappe.db.sql(""" select 
                                                                    crate_quantity,crate_type 
                                                               from 
                                                                    `tabCrate` 
                                                               where 
                                                                     parent = %(item_code)s and warehouse = %(warehouse)s limit 1 """,
                                                                    {'item_code': dist_itm[i],'warehouse': dist_warehouse[j]})
                            print('jjjjjjjjjjjjjjjjjjjjjj',crate_details)
                            if len(crate_details) > 0:
                                print('crate detils$$$$$$$$$$$$$$$$$$$$$$',(crate_details))
                                doc.append('crate_count', {
                                    'crate_type': crate_details[0][1],
                                    'outgoing_count': int(round(((total_qty[0][0] + free_qty) / int((crate_details[0][0]) * (1 + overage / 100))),2)),
                                    'item_code': dist_itm[i],
                                    'item_name': overage_details.item_name,
                                    'qty': total_qty[0][0],
                                    'uom': overage_details.stock_uom,
                                    'free_qty': free_qty,
                                    'warehouse': dist_warehouse[j][0]
                                })
                                total_supp_qty += total_qty[0][0]
                                total_crate_qty += int(round(((total_qty[0][0] + free_qty) / int((crate_details[0][0]) * (1 + overage / 100))), 2))
                                str_free_qty = str(free_qty)

                                if (str_free_qty != "None"):
                                    total_free_qty += int(free_qty)
                                qty = int(round(((total_qty[0][0] + free_qty) % int(((crate_details[0][0]) * (1 + overage / 100)))), 2))

                                if qty > 0:
                                    doc.append('loose_crate', {
                                        'item_code': dist_itm[i][0],
                                        'crate_type': crate_details[0][1],
                                        'qty': int(round(((total_qty[0][0] + free_qty) % int(((crate_details[0][0]) * (1 + overage / 100)))), 2))
                                    })

            doc.total_supp_qty = total_supp_qty
            doc.total_crate_qty = total_crate_qty
            doc.total_free_qty = total_free_qty
            doc.crate_cal_done = "Done"
            doc.save(ignore_permissions=True)
            doc.db_update()            
            return dict_create_type



@frappe.whitelist()
def calculate_crate_save(name):
    print('calculate crate^^^^^^^^^^^^^^^^^^^^^6')
    
    c_count=[]
    
    doc_name = name
    if doc_name:
        doc = frappe.get_doc("Sales Invoice",doc_name)
        # add_crate_count_item_line(doc)
        frappe.db.sql("delete from `tabCrate Count Child` where parent = %s",(doc.name))
        frappe.db.sql("delete from `tabLoose Crate` where parent = %s", (doc.name))
        dict_create_type = dict()
        dist_itm = list(frappe.db.sql("""select 
                                            distinct(item_code) 
                                        from 
                                            `tabSales Invoice Item` 
                                        where 
                                            parent= %(parent)s """,{'parent':doc.name}))
        total_supp_qty = 0
        total_crate_qty = 0
        total_free_qty = 0

        for i in range(0,len(dist_itm)):
            print('range***********************',dist_itm)
            overage_details = frappe.get_doc("Item",dist_itm[i][0])
            overage = overage_details.crate_overage
            has_batch_no = overage_details.has_batch_no
            dist_warehouse = list(frappe.db.sql("""select 
                                                        distinct(warehouse) 
                                                    from 
                                                        `tabSales Invoice Item` 
                                                    where 
                                                        item_code= %(item_code)s """,{'item_code':dist_itm[i]}))
            


            for j in range(0,len(dist_warehouse)):
                print('Batch no^^^^^^^^^^^^^^^^^^^^^^^^^^',dist_warehouse)
                if has_batch_no == 1:
                    dist_batch_no = list(frappe.db.sql("""select 
                                                            distinct(batch_no) 
                                                            from 
                                                            `tabSales Invoice Item` 
                                                            where 
                                                            warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s """,
                                                            {'warehouse':dist_warehouse[j],'item_code':dist_itm[i],'doc_name':doc_name}))
                    for k in range(0, len(dist_batch_no)):
                        print('total qty&&&&&&&&&&&&&&&&&&&&&&',dist_batch_no)
                        total_qty = frappe.db.sql(""" select 
                                                            sum(stock_qty) 
                                                        from 
                                                            `tabSales Invoice Item` 
                                                        where
                                                            is_free_item = 0 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s and batch_no = %(batch_no)s""",
                                                            {'warehouse':dist_warehouse[j],'item_code':dist_itm[i],'doc_name':doc_name,'batch_no':dist_batch_no[k]})
                        print('total qty@@@@@@@@@@@@@@@@@@@@@@@',total_qty)
                        free_qty = 0
                        free_qty_list = frappe.db.sql(""" select 
                                                                sum(stock_qty) 
                                                            from 
                                                                `tabSales Invoice Item` 
                                                            where
                                                                is_free_item = 1 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s and batch_no = %(batch_no)s""",
                                                                {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i],'doc_name': doc_name, 'batch_no': dist_batch_no[k]})
                        if str(free_qty_list[0][0]) != "None":
                            free_qty = int(free_qty_list[0][0])

                        ttl_qty = str(total_qty[0][0])
                        print('ttl &&&&&&&&&&&&&&&&&&&&&',ttl_qty)
                        if ttl_qty != "None":
                            print('ttl qty**********************************',dist_warehouse[j],dist_itm[i])
                            crate_details = frappe.db.sql(""" select 
                                                                    crate_quantity,crate_type 
                                                                from 
                                                                    `tabCrate` 
                                                                where 
                                                                    parent = %(item_code)s and warehouse = %(warehouse)s limit 1 """,
                                                                    {'item_code':dist_itm[i],'warehouse':dist_warehouse[j]})


                            print('AAAAAAAAAAAAAAAAAAAAAAA',crate_details)
                            if len(crate_details) > 0:
                                print('kkkkkkkkkkkkkkkkkkkkkkkk',len(crate_details))
                                c_count.append( {
                                                    'crate_type': crate_details[0][1],
                                                    'outgoing_count': int(round(((total_qty[0][0] + free_qty) / int((crate_details[0][0])* (1 + overage/100))), 2)),
                                                    'item_code': dist_itm[i][0],
                                                    'item_name': overage_details.item_name,
                                                    'qty': total_qty[0][0],
                                                    'batch_no': dist_batch_no[k][0],
                                                    'uom': overage_details.stock_uom,
                                                    'free_qty': free_qty,
                                                    'warehouse': dist_warehouse[j][0]
                                                })
                                
                                print('crate count append^^^^^^^^^^^^^^^^^',crate_details[0][1],int(round(((total_qty[0][0] + free_qty) / int((crate_details[0][0])* (1 + overage/100))), 2)),
                                        dist_itm[i], total_qty[0][0], dist_warehouse[j][0])
                                total_supp_qty += total_qty[0][0]
                                total_crate_qty += int(round(((total_qty[0][0] + free_qty) / int((crate_details[0][0])* (1 + overage/100))), 2))
                                str_free_qty = str(free_qty)

                                if (str_free_qty != "None"):
                                    total_free_qty += int(free_qty)

                                qty = int(round(((total_qty[0][0] + free_qty) % int(((crate_details[0][0]) * (1 + overage/100)))), 2))

                                if qty > 0:
                                    doc.append('loose_crate', {
                                        'item_code': dist_itm[i][0],
                                        'crate_type': crate_details[0][1],
                                        'qty': int(round(((total_qty[0][0] + free_qty) % int(((crate_details[0][0]) * (1 + overage/100)))), 2))
                                    })
                    

                elif has_batch_no == 0:
                    free_qty = 0
                    free_qty_list = frappe.db.sql(""" select 
                                                            sum(stock_qty) 
                                                        from 
                                                            `tabSales Invoice Item` 
                                                        where 
                                                            is_free_item = 1 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s""",
                                                            {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i], 'doc_name': doc_name})

                    if str(free_qty_list[0][0]) != "None":
                        free_qty = free_qty_list[0][0]

                    total_qty = frappe.db.sql(""" select 
                                                        sum(stock_qty) 
                                                    from 
                                                        `tabSales Invoice Item` 
                                                    where
                                                    is_free_item = 0 and warehouse = %(warehouse)s and item_code = %(item_code)s and parent = %(doc_name)s""",
                                                    {'warehouse': dist_warehouse[j], 'item_code': dist_itm[i],'doc_name': doc_name})

                    ttl_qty = str(total_qty[0][0])

                    if ttl_qty != "None":
                        crate_details = frappe.db.sql(""" select 
                                                                crate_quantity,crate_type 
                                                            from 
                                                                `tabCrate` 
                                                            where 
                                                                    parent = %(item_code)s and warehouse = %(warehouse)s limit 1 """,
                                                                {'item_code': dist_itm[i],'warehouse': dist_warehouse[j]})
                        print('jjjjjjjjjjjjjjjjjjjjjj',crate_details)
                        if len(crate_details) > 0:
                            print('crate detils$$$$$$$$$$$$$$$$$$$$$$',(crate_details))
                            c_count.append( {
                                'crate_type': crate_details[0][1],
                                'outgoing_count': int(round(((total_qty[0][0] + free_qty) / int((crate_details[0][0]) * (1 + overage / 100))),2)),
                                'item_code': dist_itm[i][0],
                                'item_name': overage_details.item_name,
                                'qty': total_qty[0][0],
                                'uom': overage_details.stock_uom,
                                'free_qty': free_qty,
                                'warehouse': dist_warehouse[j][0]
                            })
                            total_supp_qty += total_qty[0][0]
                            total_crate_qty += int(round(((total_qty[0][0] + free_qty) / int((crate_details[0][0]) * (1 + overage / 100))), 2))
                            str_free_qty = str(free_qty)

                            if (str_free_qty != "None"):
                                total_free_qty += int(free_qty)
                            qty = int(round(((total_qty[0][0] + free_qty) % int(((crate_details[0][0]) * (1 + overage / 100)))), 2))

                            if qty > 0:
                                doc.append('loose_crate', {
                                    'item_code': dist_itm[i][0],
                                    'crate_type': crate_details[0][1],
                                    'qty': int(round(((total_qty[0][0] + free_qty) % int(((crate_details[0][0]) * (1 + overage / 100)))), 2))
                                })
        doc.crate_count=c_count
        print("$$$$$$$$$$$$$$$$$1234",c_count)
        # frappe.db.set_value("")
        doc.total_supp_qty = total_supp_qty
        doc.total_crate_qty = total_crate_qty
        doc.total_free_qty = total_free_qty
        doc.crate_cal_done = "Done"
        
            
        return c_count

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

# def add_crate_count_item_line(doc):
#     if doc:
#         for itm in doc.items:
#             crate_count = frappe.get_doc("Item", itm.item_code)
#             overage = 0
#             if crate_count.allow_crate_overage and crate_count.crate_overage:
#                 overage = crate_count.crate_overage
#             # qty = round((itm.qty / (crate_count.crate_quantity * (1 + overage / 100))),2)
#             qty = 0
#             for itms in crate_count.crate:
#                 count = 0
#                 if itm.warehouse == itms.warehouse and count == 0:
#                     if itms.crate_quantity:
#                         qty = int(round((itm.stock_qty / (itms.crate_quantity)),2))
#                     if 0 < qty < 1:
#                         qty =1.0
#                     itm.crate_count = float(((str(qty) + ".").split("."))[0])
#                     itm.crate_type = crate_count.crate_type
#                     count =1
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
            print('Doc************************',doc)
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
        if route_name:
            dic = {}
            dic['route'] = route_name[0][0]
            print('dic^^^^^^^^^^^^^^^^^^^^',dic)
            return dic
        return False



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


@frappe.whitelist()
def set_fat_and_snf_rate(obj,method):
    if obj.customer:
        query = frappe.db.sql("""select tbm.name,tbm.milk_type,tbm.rate,tbm.snf_clr_rate from `tabBulk Milk Price List` as tbm inner join 
                `tabBulk Milk Price List Customer` as tbc on tbc.parent = tbm.name
                where tbm.docstatus = 1 and tbm.active = 1 and tbc.customer = %s and tbm.milk_type = %s  
                order by tbm.creation desc limit 1""", (obj.customer,obj.milk_type), as_dict=True)
        if query:
            obj.fat_rate = query[0].rate
            obj.snf_clr_rate = query[0].snf_clr_rate
            #
            for res in obj.items:
                if res.fat and query[0].rate:
                    res.fat_amount = res.fat * query[0].rate
                if res.snf_clr and query[0].snf_clr_rate:
                    res.snf_clr_amount = res.snf_clr * query[0].snf_clr_rate



# @frappe.whitelist()
# def get_party_bal(doc_name, customer_name=None):
#     if not customer_name:
#         frappe.throw(_("Please select customer"))
#     else:
#         doc = frappe.get_doc("Sales Invoice", doc_name)
#         cust_name = customer_name
#         doctype = "Customer"
#         loyalty_program = None
#         party_bal = get_dashboard_info(doctype, cust_name, loyalty_program)
#         if cust_name and party_bal:
#             doc._party_balance = party_bal[0]['total_unpaid']
#             doc.db_update()
#     return True

# def get_party_bals(sale, meth):
#     cust_name = sale.customer_name
#     doctype = "Customer"
#     loyalty_program = None
#     party_bal = get_dashboard_info(doctype, cust_name, loyalty_program)
#     if cust_name and party_bal:
#         sale._party_balance = party_bal[0]['total_unpaid']