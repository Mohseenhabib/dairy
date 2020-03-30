 frappe.listview_settings['Milk Entry'] = {
 	add_fields: [ "status"],
 	get_indicator: function(doc) {
 		if (doc.status === "To Bill")
 		{
 			return [__("To Bill"), "orange", "status,=,To Bill"];
 		}
 		else if (doc.status === "Completed")
 		{
 			return [__("Completed"), "green", "status,=,Completed"];
 		}
 		else if (doc.status === "Closed")
 		{
 			return [__("Closed"), "green", "status,=,Closed"];
 		}
 	}
 };