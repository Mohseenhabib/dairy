import frappe
from frappe.utils.data import flt



@frappe.whitelist()
def get_required_fat_snf(production_item, quantity):  
    reqd_fat = frappe.get_doc("Item",{'name' : production_item})
    
    if reqd_fat.maintain_fat_snf_clr == 1:
        if reqd_fat.standard_fat > 0 or reqd_fat.standard_snf > 0 : 

            item_fat = (flt(quantity) * flt(reqd_fat.weight_per_unit)) * (flt(reqd_fat.standard_fat) / 100)
            item_snf = (flt(quantity) * flt(reqd_fat.weight_per_unit)) * (flt(reqd_fat.standard_snf) / 100)
        

            return [reqd_fat.standard_fat, reqd_fat.standard_snf, item_fat, item_snf]


def bom_item_child_table(self, method):
    for i in self.required_items:
        reqd_fat = frappe.get_doc("Item",{'name' : i.item_code})
        if reqd_fat.maintain_fat_snf_clr == 1:
            if reqd_fat.standard_fat > 0 or reqd_fat.standard_snf > 0 : 

                i.standard_fat = reqd_fat.standard_fat
                i.standard_snf=reqd_fat.standard_snf
                i.standard_fat_in_kg = (flt(i.required_qty) * flt(reqd_fat.weight_per_unit)) * (flt(reqd_fat.standard_fat) / 100)
                i.standard_snf_in_kg= (flt(i.required_qty) * flt(reqd_fat.weight_per_unit)) * (flt(reqd_fat.standard_snf) / 100)

               