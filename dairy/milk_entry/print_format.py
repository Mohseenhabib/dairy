import frappe


@frappe.whitelist()
def get_purchase(pr):
    doc=frappe.get_doc("Purchase Invoice",pr)
    dlst=[]
    for j in doc.items:
        pr_item=frappe.get_doc("Purchase Receipt",j.purchase_receipt)
        j.update({"posting_date":pr_item.posting_date,"shift":pr_item.shift})
        dlst.append(j)
    sorted_data = sorted(dlst, key=lambda x: (x['posting_date'], x['shift']))
    return sorted_data


