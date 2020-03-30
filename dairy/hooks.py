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



# -----------------------quick entry temporay removed  -sid----------------------
app_include_js = "/assets/js/vehicle.min.js"




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
    "Sales Invoice": "public/js/sales_invoice.js"
    }

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
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
# after_install = "dairy.install.after_install"

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
        "after_insert": "dairy.milk_entry.custom_delivery_note.calculate_crate_after_insert",
        "validate": "dairy.milk_entry.custom_delivery_note.route_validation",
    },
    "Sales Order": {
        "validate": "dairy.milk_entry.custom_delivery_note.route_validation",
    },
    "Quotation": {
        "validate": "dairy.milk_entry.custom_delivery_note.route_validation",
    },
    "Sales Invoice": {
        "validate": "dairy.milk_entry.custom_delivery_note.route_validation",
    },
    "Stock Entry":{
        "after_insert": "dairy.milk_entry.doctype.van_collection.van_collection.change_van_collection_status"
    },
    "Purchase Receipt":{
        "after_insert": "dairy.milk_entry.custom_purchase_receipt.change_milk_entry_status"
    }
}

permission_query_conditions = {
    "Vehicle": "dairy.vehicle_dynamic_link.get_permission_query_conditions_for_vehicle",
    "Customer": "dairy.vehicle_dynamic_link.get_permission_query_conditions_for_customer",
}

has_permission = {
    "Vehicle": "dairy.vehicle_dynamic_link.has_permission",
    "Customer": "dairy.vehicle_dynamic_link.has_permission",
}

# doc_events={
#     "Milk Entry": {
#  		"onload": "dairy.milk_entry.doctype.milk_entry.milk_entry.filters_to_quick_entry"
# 	}
# }


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"dairy.tasks.all"
# 	],
# 	"daily": [
# 		"dairy.tasks.daily"
# 	],
# 	"hourly": [
# 		"dairy.tasks.hourly"
# 	],
# 	"weekly": [
# 		"dairy.tasks.weekly"
# 	]
# 	"monthly": [
# 		"dairy.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "dairy.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"erpnext.selling.doctype.quotation.quotation.make_sales_order": "dairy.milk_entry.custom_delivery_note.make_sales_order"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dairy.task.get_dashboard_data"
# }

