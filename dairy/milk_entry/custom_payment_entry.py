import frappe
import json

@frappe.whitelist()
def get_filter_data(filter_list):
    if filter_list:
        filter.append(filter_list)

    # for val in filter_list:
        # print("@@@@@@@@@@@@@@@@@@@@@@@@", [val])
           