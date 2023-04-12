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
    item=remove_fat_item(self.company,self.source_warehouse,date,self.required_items)
    for i in item:
        for j in self.required_items:
            if i.get("item")==j.item_code:
                j.fat_per=i.get("fatper")
                j.snf_per=i.get("snfper")
                j.fat_per_in_kg=(i.get("fatper")/100)*j.required_qty
                j.snf_in_kg=(i.get("snfper")/100)*j.required_qty
    for j in self.required_items:
        fat.append(flt(j.fat_per_in_kg))
        snf.append(flt(j.snf_in_kg))
    if len(fat)>1:
        self.rm_fat_in_kg=sum(fat)
        self.diff_fat_in_kg=self.required_fat_in_kg-sum(fat)

    if len(snf)>1:
        self.rm_snf_in_kg=sum(snf)
        self.diff_snf_in_kg=self.required_snt_in_kg-sum(snf)




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
def get_data_fat(name):
    doc=frappe.get_doc("Dairy Settings")
    wo=frappe.get_doc("Work Order",name)
    items_to_add_fat=frappe.db.sql("Select item from `tabfatsnf table` where parent='Dairy Settings' order by priority1 asc ",as_dict=1)
    date=""
    if wo.actual_start_date:
        date=getdate( wo.actual_start_date)
    else:
        date=getdate( wo.planned_start_date)
    list=[]
    if wo.diff_fat_in_kg >0:
        list=add_fat_item(abs(wo.diff_fat_in_kg),wo.company,wo.source_warehouse,date,items_to_add_fat)
        for k in list:
            if len(wo.fg_item_scrap)==0:
                    wo.append("fg_item_scrap",{
                        "item":wo.production_item,
                        "qty":k.get("pickedqty")
                    })
            else:
                for j in wo.fg_item_scrap:
                    j.qty=flt(j.qty)+k.get("pickedqty")
        return list
    else:
        if wo.diff_fat_in_kg>0:
            if doc.threshold_for_fat_separation<abs(wo.diff_fat_in_kg):
                list.append({"operation":doc.operation,"workstation":doc.workstation,"workstation_type":doc.workstation_type,
                            "completed_qty":wo.qty,"time_in_mins":doc.operation_time,"bom":wo.bom_no,"threshhold":1})
            return list
        elif wo.diff_fat_in_kg<0:
            rmfatkg=[]
            rm_weight=[]
            for j in wo.required_items:
                rmfatkg.append(j.fat_per_in_kg)
                item=frappe.get_doc("Item",j.item_code)
                rm_weight.append(j.required_qty*item.weight_per_unit)
            rmweight=(sum(rmfatkg)*100)/4
            print("&&&&&&&&&&&&&&&",rmweight)
            print("$$$$$$$$$$$$$$$$",sum(rm_weight))
            water=rmweight-sum(rm_weight)+wo.process_loss_qty
            list.append({"item":doc.item_to_add_snf_fat,"warehouse":wo.source_warehouse,"pickedqty":abs(water),"threshhold":0})
            if len(wo.fg_item_scrap)==0:
                wo.append("fg_item_scrap",{
                    "item":wo.production_item,
                    "qty":abs(water)

                })
            else:
                for j in wo.fg_item_scrap:
                    j.qty=flt(j.qty)+abs(water)
            return list


@frappe.whitelist()
def get_data_snf(name):
    doc=frappe.get_doc("Dairy Settings")
    wo=frappe.get_doc("Work Order",name)
    items_to_add_snf=frappe.db.sql("Select item from `tabAdd Snf Table` where parent='Dairy Settings' order by priority1 asc ",as_dict=1)
    date=""
    if wo.actual_start_date:
        date=getdate( wo.actual_start_date)
    else:
        date=getdate( wo.planned_start_date)
    list=[]
    jlist=[]
    if wo.diff_snf_in_kg >0:
        list=add_snf_item(abs(wo.diff_snf_in_kg),wo.company,wo.source_warehouse,date,items_to_add_snf)
        for i in list:
            jlist.append(i)
        for i in list:
            for k in doc.items_to_add_snf:
                if k.part_of_water>0:
                    if i.get("item")==k.item:
                        j={"item":k.water_item,"pickedqty":flt(i.get("pickedqty"))*flt(k.part_of_water),"warehouse":i.get("warehouse")}
                        jlist.append(j)
        for k in jlist:
            if len(wo.fg_item_scrap)==0:
                    wo.append("fg_item_scrap",{
                        "item":wo.production_item,
                        "qty":k.get("pickedqty")
                    })
            else:
                for j in wo.fg_item_scrap:
                    j.qty=flt(j.qty)+k.get("pickedqty")
        return jlist
    else:
        if wo.diff_snf_in_kg<0:
            rmsnfkg=[]
            rm_weight=[]
            for j in wo.required_items:
                rmsnfkg.append(j.snf_per_in_kg)
                item=frappe.get_doc("Item",j.item_code)
                rm_weight.append(j.required_qty*item.weight_per_unit)
            rmweight=(sum(rmsnfkg)*100)/wo.required_fat
            water=rmweight-sum(rm_weight)+wo.process_loss_qty
            # wo.db_set("qty",flt(wo.qty)+flt(water))
            list.append({"item":doc.item_to_add_snf_fat,"warehouse":wo.source_warehouse,"pickedqty":abs(water),"threshhold":0})
            if len(wo.fg_item_scrap)==0:
                wo.append("fg_item_scrap",{
                    "item":wo.production_item,
                    "qty":abs(water)

                })
            else:
                for j in wo.fg_item_scrap:
                    j.qty=flt(j.qty)+abs(water)
            return list

    


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
        if td:
            if len(td)>1:
                td=td[-1]
                if td.get("qty_after_transaction")>0 and td.get("fat_after_transaction")>=remaningfatinkg:
                    fatper=(td.get("fat_after_transaction")/td.get("qty_after_transaction"))*100
                    pickedwt=(td.get("qty_after_transaction")/td.get("fat_after_transaction"))*remaningfatinkg
                    picked_fat_in_kg=pickedwt*(fatper/100)
                    pickedqty=pickedwt/item.weight_per_unit
                    remaningfatinkg=0
                    list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_fat_in_kg":remaningfatinkg,"fatper":fatper,"pickedwt":pickedwt,"picked_fat_in_kg":picked_fat_in_kg,"pickedqty":pickedqty,"threshhold":0})
                    break
                else:
                    if td.get("qty_after_transaction")>0 and td.get("fat_after_transaction")>0:
                        remaningfatinkg=remaningfatinkg-td.get("fat_after_transaction")
                        fatper=(td.get("fat_after_transaction")/td.get("qty_after_transaction"))*100
                        pickedwt=td.get("qty_after_transaction")
                        picked_fat_in_kg=pickedwt*(fatper/100)
                        pickedqty=td.get("balance_qty")
                        list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_fat_in_kg":remaningfatinkg,"fatper":fatper,"pickedwt":pickedwt,"picked_fat_in_kg":picked_fat_in_kg,"pickedqty":pickedqty,"threshhold":0})

            
            else:
                td=td[0]
                if td.get("qty_after_transaction")>0 and td.get("fat_after_transaction")>remaningfatinkg:
                    fatper=(td.get("fat_after_transaction")/td.get("qty_after_transaction"))*100
                    pickedwt=(td.get("qty_after_transaction")/td.get("fat_after_transaction"))*remaningfatinkg
                    picked_fat_in_kg=pickedwt*(fatper/100)
                    pickedqty=pickedwt/item.weight_per_unit
                    remaningfatinkg=0
                    list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_fat_in_kg":remaningfatinkg,"fatper":fatper,"pickedwt":pickedwt,"picked_fat_in_kg":picked_fat_in_kg,"pickedqty":pickedqty,"threshhold":0})
                    break
                else:
                    if td.get("qty_after_transaction")>0 and td.get("fat_after_transaction")>0:
                        remaningfatinkg=remaningfatinkg-td.get("fat_after_transaction")
                        fatper=td.get("fat_after_transaction")/td.get("qty_after_transaction")*100
                        pickedwt=td.get("qty_after_transaction")
                        picked_fat_in_kg=pickedwt*(fatper/100)
                        pickedqty=td.get("balance_qty")
                        list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_fat_in_kg":remaningfatinkg,"fatper":fatper,"pickedwt":pickedwt,"picked_fat_in_kg":picked_fat_in_kg,"pickedqty":pickedqty,"threshhold":0})
        if remaningfatinkg<=0:
            break
    if len(list)==0:
        frappe.throw("Item Not Available")

    return list

@frappe.whitelist()
def add_snf_item(required_snf_kg,company,warehouse,date,itemlist):
   
    list=[]
    filters={}
    remaningsnfinkg=required_snf_kg
    for i in itemlist:
        item=frappe.get_doc("Item",i.item)
        filters.update({'warehouse':warehouse,"from_date":date,"to_date":date,"company":company,"item_code":item.name})
        filters=frappe._dict(filters)
        td=exec(filters)
        if td:
            if len(td)>1:
                td=td[-1]
                if td.get("qty_after_transaction")>0 and td.get("snf_after_transaction")>=remaningsnfinkg:
                    snfper=(td.get("snf_after_transaction")/td.get("qty_after_transaction"))*100
                    pickedwt=(td.get("qty_after_transaction")/td.get("snf_after_transaction"))*remaningsnfinkg
                    picked_snf_in_kg=pickedwt*(snfper/100)
                    pickedqty=pickedwt/item.weight_per_unit
                    remaningsnfinkg=0
                    list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_snf_in_kg":remaningsnfinkg,"snfper":snfper,"pickedwt":pickedwt,"picked_snf_in_kg":picked_snf_in_kg,"pickedqty":pickedqty,"threshhold":0})
                    break
                else:
                    if td.get("qty_after_transaction")>0 and td.get("snf_after_transaction")>0:
                        remaningsnfinkg=remaningsnfinkg-td.get("snf_after_transaction")
                        snfper=(td.get("snf_after_transaction")/td.get("qty_after_transaction"))*100
                        pickedwt=td.get("qty_after_transaction")
                        picked_snf_in_kg=pickedwt*(snfper/100)
                        pickedqty=td.get("balance_qty")
                        list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_snf_in_kg":remaningsnfinkg,"snfper":snfper,"pickedwt":pickedwt,"picked_snf_in_kg":picked_snf_in_kg,"pickedqty":pickedqty,"threshhold":0})

            
            else:
                td=td[0]
                if td.get("qty_after_transaction")>0 and td.get("snf_after_transaction")>remaningsnfinkg:
                    snfper=(td.get("snf_after_transaction")/td.get("qty_after_transaction"))*100
                    pickedwt=(td.get("qty_after_transaction")/td.get("snf_after_transaction"))*remaningsnfinkg
                    picked_snf_in_kg=pickedwt*(snfper/100)
                    pickedqty=pickedwt/item.weight_per_unit
                    remaningsnfinkg=0
                    list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_snf_in_kg":remaningsnfinkg,"snfper":snfper,"pickedwt":pickedwt,"picked_snf_in_kg":picked_snf_in_kg,"pickedqty":pickedqty,"threshhold":0})
                    break
                else:
                    if td.get("qty_after_transaction")>0 and td.get("snf_after_transaction")>0:
                        remaningsnfinkg=remaningsnfinkg-td.get("snf_after_transaction")
                        snfper=td.get("snf_after_transaction")/td.get("qty_after_transaction")*100
                        pickedwt=td.get("qty_after_transaction")
                        picked_snf_in_kg=pickedwt*(snfper/100)
                        pickedqty=td.get("balance_qty")
                        list.append({"item":item.name,"warehouse":warehouse,"company":company,"remaining_snf_in_kg":remaningsnfinkg,"snfper":snfper,"pickedwt":pickedwt,"picked_snf_in_kg":picked_snf_in_kg,"pickedqty":pickedqty,"threshhold":0})
        if remaningsnfinkg<=0:
            break
    if len(list)==0:
        frappe.throw("Item Not Available")

    return list



@frappe.whitelist()
def remove_fat_item(company,warehouse,date,itemlist):
    list=[]
    filters={}
    print("#####################",itemlist)
    for i in itemlist:
        item=frappe.get_doc("Item",i.item_code)
        filters.update({'warehouse':warehouse,"from_date":date,"to_date":date,"company":company,"item_code":item.name})
        filters=frappe._dict(filters)
        td=exec(filters)
        print("&&&&&&&&&&&&&&&&&&&&&&&1234",td)
        if td:
            if len(td)>1:
                td=td[-1]
                if td.get("qty_after_transaction")>0:
                    fat_per=(td.get("fat_after_transaction")/td.get("qty_after_transaction"))*100
                    snf_per=(td.get("snf_after_transaction")/td.get("qty_after_transaction"))*100
                    list.append({"item":item.name,"fatper":fat_per,"snfper":snf_per})
            else:
                td=td[0]
                print("&&&&&&&&&&&&&&&&&&",td)
                if td.get("qty_after_transaction")>0:
                    fat_per=(td.get("fat_after_transaction")/td.get("qty_after_transaction"))*100
                    snf_per=(td.get("snf_after_transaction")/td.get("qty_after_transaction"))*100
                    list.append({"item":item.name,"fatper":fat_per,"snfper":snf_per})
    

    return list

