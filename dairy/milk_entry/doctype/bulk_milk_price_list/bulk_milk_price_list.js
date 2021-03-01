// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Milk Price List', {
	milk_type: function(frm,cdt,cdn){
		frm.set_query("item", function() {
			return {
				filters: [
					["Item","milk_type", "in", [frm.doc.milk_type]]
				]
			}
		});

	}
});
