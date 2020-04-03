from __future__ import print_function, unicode_literals
import frappe

def after_install():
    print("@@@@@@@@@@@@@@@@@@@@2------------------@@@@@@@@@@@@@@@@@")
    res = frappe.db.sql("""INSERT INTO `tabDomain` (domain) VALUES ('Dairy')""")
    print("@@@@@@@@@@@@@@@@@@@@2------------------@@@@@@@@@@@@@@@@@",res)
    res.db_update()