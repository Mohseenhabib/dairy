# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "dairy"
app_title = "Dairy"
app_publisher = "Dexciss Technology Pvt Ltd"
app_description = "Dairy modules"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "dexciss"
app_license = "Dexciss"



# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dairy/css/dairy.css"

fixtures = [
		{"dt":"Custom Field", "filters": [["name", "in",("Timesheet-approved","Timesheet Detail-sales_order",
                "Timesheet Detail-approved","Employee-employee_costing_rate","Employee Group-group_lead","Employee Group-department","Employee Group-column_break_3",
                "Employee Group-group_lead_name","Employee Group-hod","Issue-test_session","Issue-task","Issue-base_estimated_cost","Issue-currency","Issue-estimated_cost",
                "Issue-department_","Issue-section_break_45","Issue-doctype_name","Issue-screenshot","Issue-console_log_description","Issue-if_issue_type_customisation_request_cr",
                "Issue-step_to_reproduce","Issue-task_created","Issue-estimated_cost_in_words","Issue-print_settings","Issue-heading","Issue-resolution_required",
                "Issue-section_break_16","Issue-employee_group","Issue-primary_consultant","Issue-project_lead","Issue-primary_consultant_name","Issue-project_lead_name",
                "Issue-column_break_20","Issue-grand_total","Issue-grand__total_cost_in_words","Issue-billing_section","Issue-column_break_17",
                "Task-employee_group","Task-primary_consultant","Task-is_billable",
                "Task-project_lead","Task-primary_consultant_name","Task-project_lead_name","Task-duration_per_day_in_hours",
                "Task-total_duration_in_days","Task-employee_group_section","Task-column_break_25","Project-currency","Project-auto_submit_invoice",
                "Project-billing_based_on","Project-start_date","Project-total_project_value_excluding_taxes","Project-billing_frequency","Project-milestone_section",
                "Project-milestone","Project-auto_creation_doctype","Project-auto_submit_order","Project-recurring_charges","Project-recurring_item","Project-timesheet_item",
                "Project-timesheet_days","Project-billing_charges_based_on_activity_cost","Project-billing_charges_based_on_project_timesheet_charges","Project-team_details",
                "Project-employee_group","Project-project_lead","Project-project_lead_name","Project-column_break_25","Project-primary_consultant","Project-primary_consultant_name",
                "Project-sales_taxes_charges_template","Project-terms","Project-project_billing_rate","Project-sales_order_naming_series","Project-sales_invoice_naming_series",
                "Project-cr_last_billing_date","Project-cr_item","Project-price_list","Project-last_billing_date","Project-allocation_item",
                "Sales Order-project_allocation_bill","Sales Invoice-project_allocation_bill","Issue-sales_invoice","Issue-sales_order","Issue-completed_on","Task-ticket","Sales Invoice-ticket"),]]}

    ]


# -----------------------quick entry temporay removed  -sid----------------------
app_include_js = "/assets/js/vehicle.min.js"


fixtures = fixtures = [
		{"dt":"Custom Field", "filters": [["name", "in",(
            "BOM-standard_fat" ,
            "BOM-standard_snf",
            "BOM-item_fat" ,
            "BOM-item_snf",
            "BOM-weight_details",
            "BOM-fg_weight",
            "BOM-total_rm_weight",
            "BOM-total_rm_fat",
            "BOM-total_rm_snf",
            "Item-standar_fat",
            "Item-standard_snf",
            "BOM Item-weight",
            "BOM Item-standard_fat",
            "BOM Item-bom_fat",
            "BOM Item-standard_snf",
            "BOM Item-bom_snf"
        )]]}
]

# include js, css files in header of web template
# web_include_css = "/assets/dairy/css/dairy.css"
# web_include_js = "/assets/dairy/js/dairy.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Warehouse": "public/js/utils/warehouse.js",
    "Sales Order": "public/js/sales_order.js",
    "Quotation": "public/js/quotation.js",
    "Delivery Note": "public/js/delivery_note.js",
    "Vehicle": "public/js/vehicle.js",
    "Customer": "public/js/customer.js",
    "Sales Invoice": "public/js/sales_invoice.js",
    # "Supplier": "public/js/supplier.js",
    "Item": "public/js/item.js",
    "Stock Entry": "public/js/stock_entry.js",
    "Purchase Receipt": "public/js/purchase_receipt.js",
    "BOM":"public/js/custom_bom.js"
    }

doctype_list_js = {
                    "Warehouse": "public/js/utils/warehouse_list.js",
                    # "Supplier": "public/js/supplier_list.js"
                  }
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "dairy.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "dairy.install.before_install"
after_install = "dairy.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dairy.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Delivery Note": {
        # "before_insert": "dairy.milk_entry.custom_delivery_note.calculate_crate_after_insert",
        # "before_save": "dairy.milk_entry.custom_delivery_note.calculate_crate_after_insert",
        "validate": "dairy.milk_entry.custom_delivery_note.route_validation",
        "before_submit": ["dairy.milk_entry.custom_delivery_note.before_submit",
                          "dairy.milk_entry.custom_delivery_note.after_save"],
        "on_submit": "dairy.milk_entry.custom_delivery_note.on_submit",
        "after_insert": ["dairy.milk_entry.custom_delivery_note.calculate_crate",
                         "dairy.milk_entry.custom_delivery_note.after_save"],
        "before_save": ["dairy.milk_entry.custom_delivery_note.calculate_crate",
                        "dairy.milk_entry.custom_delivery_note.after_save",
                        # "dairy.milk_entry.custom_delivery_note.set_fat_and_snf_rate"
                        ],
        "on_cancel": "dairy.milk_entry.custom_delivery_note.cancel_milk_stock_ledger"
    },
    "Sales Order": {
        "validate": "dairy.milk_entry.custom_delivery_note.route_validation",
        "before_submit":"dairy.milk_entry.custom_sales_order.before_submit"
    },
    "Quotation": {
        "validate": "dairy.milk_entry.custom_delivery_note.route_validation",
    },
    "Sales Invoice": {
        "validate": "dairy.milk_entry.custom_delivery_note.route_validation",
        "before_submit": "dairy.milk_entry.custom_sales_invoice.before_submit",
        "after_insert": "dairy.milk_entry.custom_sales_invoice.calculate_crate"
        # "before_save": "dairy.milk_entry.custom_sales_invoice.calculate_crate_save"
    },
    "Stock Entry":{
        "after_insert": ["dairy.milk_entry.doctype.van_collection.van_collection.change_van_collection_status",
                         "dairy.milk_entry.custom_stock_entry.milk_ledger_stock_entry"],
        "before_save": "dairy.milk_entry.custom_stock_entry.milk_ledger_stock_entry",
        "before_submit": "dairy.milk_entry.custom_stock_entry.milk_ledger_stock_entry",
        "on_submit": "dairy.milk_entry.custom_stock_entry.on_submit",
        "on_submit": "dairy.milk_entry.custom_stock_entry.update_vc_status",
        "on_cancel": "dairy.milk_entry.custom_stock_entry.cancel_create_milk_stock_ledger"
    },
    "Purchase Receipt":{
        "after_insert": "dairy.milk_entry.custom_purchase_receipt.change_milk_entry_status",
        "on_cancel": ["dairy.milk_entry.custom_purchase_receipt.cancel_create_milk_stock_ledger"],
        "on_submit": ["dairy.milk_entry.custom_purchase_receipt.change_milk_status",
                      "dairy.milk_entry.custom_purchase_receipt.create_milk_stock_ledger"],
    },
    "BOM":{
    "before_save": "dairy.dairy.custom_bom.before_save"
    }
  
}

permission_query_conditions = {
    "Vehicle": "dairy.vehicle_dynamic_link.get_permission_query_conditions_for_vehicle"
}

has_permission = {
    "Vehicle": "dairy.vehicle_dynamic_link.has_permission",
}

# doc_events={
#     "Milk Entry": {
#  		"before_save" :"dairy.milk_entry.doctype.dairy_settings.dairy_settings.purchase_invoice"
# 	}
# }


# Scheduled Tasks
# ---------------

scheduler_events = {
# # 	"all": [
# # 		"dairy.tasks.all"
# # 	],
# # 	"daily": [
# # 		"dairy.tasks.daily"
# # 	],
	"hourly": [
		"dairy.milk_entry.doctype.dairy_settings.dairy_settings.purchase_invoice",
	],
# # 	"weekly": [
# # 		"dairy.tasks.weekly"
# # 	]
# # 	"monthly": [
# # 		"dairy.tasks.monthly"
# # 	]
 }

# Testing
# -------

# before_tests = "dairy.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.selling.doctype.sales_order.sales_order.make_delivery_note": "dairy.milk_entry.custom_sales_order.make_delivery_note"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Delivery Note": "dairy.delivery_note_dashboard.get_data"
}

jinja = {
	"methods": [
        "dairy.milk_entry.custom_delivery_trip.warehouse_address",

		"dairy.milk_entry.custom_delivery_trip.get_jinja_data",
        "dairy.milk_entry.custom_delivery_trip.get_jinja_data_del_note",
        "dairy.milk_entry.custom_delivery_trip.get_jinja_data_si",
        "dairy.milk_entry.custom_delivery_trip.get_jinja_data_del_note_item",
         "dairy.milk_entry.custom_delivery_trip.get_jinja_data_si_item",
        "dairy.milk_entry.custom_delivery_trip.del_note_total",
         "dairy.milk_entry.custom_delivery_trip.si_note_total",
        "dairy.milk_entry.custom_delivery_trip.del_note_details",
         "dairy.milk_entry.custom_delivery_trip.si_note_details",
        "dairy.milk_entry.custom_delivery_trip.total_supp_qty_based_on_itm_grp",
	]
}

