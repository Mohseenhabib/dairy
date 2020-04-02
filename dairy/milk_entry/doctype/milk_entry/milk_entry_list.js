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
 		else if (doc.status === "To Post and Sample")
 		{
 			return [__("To Post and Sample"), "green", "status,=,To Post and Sample"];
 		}
 		else if (doc.status === "To Sample")
 		{
 			return [__("To Sample"), "green", "status,=,To Sample"];
 		}
 		else if (doc.status === "To Post")
 		{
 			return [__("To Post"), "green", "status,=,To Post"];
 		}
 		else if (doc.status === "Posted")
 		{
 			return [__("Posted"), "green", "status,=,Posted"];
 		}
 	}
 };