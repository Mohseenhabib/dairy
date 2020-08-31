// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.item");

frappe.ui.form.on("Item", {

});

frappe.ui.form.on("Crate", {
	crate_quantity: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "uom", frm.doc.stock_uom);
	}
})
