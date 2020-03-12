from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
        {
          "label": _("Key Reports"),
            "icon": "fa fa-table",
            "items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Milk Entry Detail",
                    "reference_doctype": "Milk Entry",
                    "onboard": 1
                }
            ]
        }
    ]