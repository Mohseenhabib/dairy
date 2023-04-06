from dairy.milk_entry.report.milk_ledger.milk_ledger import get_columns, get_item_details, get_items, get_opening_balance, get_stock_ledger_entries
from erpnext.stock.utils import update_included_uom_in_report
import frappe
from frappe.utils.data import cint, flt, getdate, today



@frappe.whitelist()
def get_required_fat_snf(production_item, quantity):  
    reqd_fat = frappe.get_doc("Item",{'name' : production_item})
    
    if reqd_fat.maintain_fat_snf_clr == 1:
        if reqd_fat.standard_fat > 0 or reqd_fat.standard_snf > 0 : 

            item_fat = (flt(quantity) * flt(reqd_fat.weight_per_unit)) * (flt(reqd_fat.standard_fat) / 100)
            item_snf = (flt(quantity) * flt(reqd_fat.weight_per_unit)) * (flt(reqd_fat.standard_snf) / 100)
        

            return [reqd_fat.standard_fat, reqd_fat.standard_snf, item_fat, item_snf]


def bom_item_child_table(self, method):
    fat=[]
    snf=[]
    date=""
    if self.actual_start_date:
        date=getdate(self.actual_start_date)
    else:
        date=getdate(self.planned_start_date)
        item=remove_fat_item(self.company,self.warehouse,date,self.required_items)
        for i in item:
            pass

        # reqd_fat = frappe.get_doc("Item",{'name' : item.item_code})
        
        # if reqd_fat.maintain_fat_snf_clr == 1:
        #     if reqd_fat.standard_fat > 0 or reqd_fat.standard_snf > 0 : 
                
        #         i.standard_fat = reqd_fat.standard_fat
        #         i.standard_snf=reqd_fat.standard_snf
        #         standard_fat_in_kg = (flt(i.required_qty) * flt(reqd_fat.weight_per_unit)) * (flt(reqd_fat.standard_fat) / 100)
        #         fat.append(standard_fat_in_kg)
        #         standard_snf_in_kg= (flt(i.required_qty) * flt(reqd_fat.weight_per_unit)) * (flt(reqd_fat.standard_snf) / 100)
        #         snf.append(standard_snf_in_kg)

    # self.diff_fat_in_kg=self.required_fat_in_kg-sum(fat)
    # self.diff_fat_in_kg=self.required_snt_in_kg-sum(snf)




def get_required_fat_snf_item(self, method):  
    reqd_fat = frappe.get_doc("Item",{'name' : self.production_item})
    
    if reqd_fat.maintain_fat_snf_clr == 1:
        if reqd_fat.standard_fat > 0 or reqd_fat.standard_snf > 0 : 
            self.required_fat=reqd_fat.standard_fat
            self.required_snf_=reqd_fat.standard_snf
            self.required_fat_in_kg = (flt(self.qty) * flt(reqd_fat.weight_per_unit)) * (flt(reqd_fat.standard_fat) / 100)
            self.required_snt_in_kg = (flt(self.qty) * flt(reqd_fat.weight_per_unit)) * (flt(reqd_fat.standard_snf) / 100)
        


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
        # print('data*************************8',sle)

        if include_uom:
            conversion_factors.append(item_detail.conversion_factor)

    update_included_uom_in_report(columns, data, include_uom, conversion_factors)
    return data

@frappe.whitelist()
def get_data(name):
    wo=frappe.get_doc("Work Order",name)
    items_to_add_fat=frappe.db.sql("Select item from `tabfatsnf table` where parent='Dairy Settings' order by priority ",as_dict=1)
    print(items_to_add_fat)
    date=""
    if wo.actual_start_date:
        date=getdate( wo.actual_start_date)
    else:
        date=getdate( wo.planned_start_date)
    list=[]
    if wo.diff_fat_in_kg <0:
        list=add_fat_item(abs(wo.diff_fat_in_kg),wo.company,wo.source_warehouse,date,items_to_add_fat)
    else:
        list=add_fat_item(wo.diff_fat_in_kg,wo.company,wo.source_warehouse,date,items_to_add_fat)
    print(list)
    for j in list:
        wo.append("required_items",{
            "item_code":j.get("item"),
            "source_warehouse":j.get("warehouse"),
            "required_qty":j.get("pickedqty")
        })
    wo.save(ignore_permissions=True)


@frappe.whitelist()
def add_fat_item(required_fat_kg,company,warehouse,date,itemlist):
   
    list=[]
    filters={}
    remaningfatinkg=required_fat_kg
    for i in itemlist:
        item=frappe.get_doc("Item",i.item)
        filters.update({'warehouse':warehouse,"from_date":date,"to_date":date,"company":company,"item_code":item.name})
        filters=frappe._dict(filters)
        td=exec(filters)
        print(td)
        if len(td)>1:
            td=td[-1]
            if td.get("qty_after_transaction")>0 and td.get("fat_after_transaction")>=remaningfatinkg:
                fatper=(td.get("fat_after_transaction")/td.get("qty_after_transaction"))*100
                pickedwt=(td.get("qty_after_transaction")/td.get("fat_after_transaction"))*remaningfatinkg
                picked_fat_in_kg=pickedwt*(fatper/100)
                pickedqty=pickedwt/item.weight_per_unit
                remaningfatinkg=0
                list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_fat_in_kg":remaningfatinkg,"fatper":fatper,"pickedwt":pickedwt,"picked_fat_in_kg":picked_fat_in_kg,"pickedqty":pickedqty})
                break
            else:
                if td.get("qty_after_transaction")>0 and td.get("fat_after_transaction")>0:
                    remaningfatinkg=remaningfatinkg-td.get("fat_after_transaction")
                    fatper=(td.get("fat_after_transaction")/td.get("qty_after_transaction"))*100
                    pickedwt=td.get("qty_after_transaction")
                    picked_fat_in_kg=pickedwt*(fatper/100)
                    pickedqty=td.get("balance_qty")
                    list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_fat_in_kg":remaningfatinkg,"fatper":fatper,"pickedwt":pickedwt,"picked_fat_in_kg":picked_fat_in_kg,"pickedqty":pickedqty})

        
        else:
            td=td[0]
            if td.get("qty_after_transaction")>0 and td.get("fat_after_transaction")>remaningfatinkg:
                fatper=(td.get("fat_after_transaction")/td.get("qty_after_transaction"))*100
                pickedwt=(td.get("qty_after_transaction")/td.get("fat_after_transaction"))*remaningfatinkg
                picked_fat_in_kg=pickedwt*(fatper/100)
                pickedqty=pickedwt/item.weight_per_unit
                remaningfatinkg=0
                list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_fat_in_kg":remaningfatinkg,"fatper":fatper,"pickedwt":pickedwt,"picked_fat_in_kg":picked_fat_in_kg,"pickedqty":pickedqty})
                break
            else:
                if td.get("qty_after_transaction")>0 and td.get("fat_after_transaction")>0:
                    remaningfatinkg=remaningfatinkg-td.get("fat_after_transaction")
                    fatper=td.get("fat_after_transaction")/td.get("qty_after_transaction")*100
                    pickedwt=td.get("qty_after_transaction")
                    picked_fat_in_kg=pickedwt*(fatper/100)
                    pickedqty=td.get("balance_qty")
                    list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_fat_in_kg":remaningfatinkg,"fatper":fatper,"pickedwt":pickedwt,"picked_fat_in_kg":picked_fat_in_kg,"pickedqty":pickedqty})
        if remaningfatinkg<=0:
            break
    if len(list)==0:
        frappe.throw("Item Not Available")

    return list



@frappe.whitelist()
def remove_fat_item(company,warehouse,date,itemlist):
   
    list=[]
    filters={}
    for i in itemlist:
        item=frappe.get_doc("Item",i.item_code)
        filters.update({'warehouse':warehouse,"from_date":date,"to_date":date,"company":company,"item_code":item.name})
        filters=frappe._dict(filters)
        td=exec(filters)
        print(td)
        if len(td)>1:
            td=td[-1]
            if td.get("qty_after_transaction")>0:
                fat_per=(td.get("fat_after_transaction")/td.get("qty_after_transaction"))*100
                list.append({"item":item.name,"fatper":fat_per})
        else:
            td=td[0]
            if td.get("qty_after_transaction")>0:
                fatper=(td.get("fat_after_transaction")/td.get("qty_after_transaction"))*100
                list.append({"item":item.name,"fatper":fatper})
    if len(list)==0:
        frappe.throw("Item Not Available")

    return list

