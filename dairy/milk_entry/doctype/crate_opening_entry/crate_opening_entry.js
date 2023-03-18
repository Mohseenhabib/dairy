// Copyright (c) 2023, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Crate Opening Entry', {
	refresh: function(frm) {
		frm.disable_save();
		!frm.doc.import_in_progress && frm.trigger("make_dashboard");
		frm.page.set_primary_action(__('Create Crate Log'), () => {
			let btn_primary = frm.page.btn_primary.get(0);
			return frm.call({
				doc: frm.doc,
				btn: $(btn_primary),
				method: "make_log",
				freeze: 1,
				freeze_message: __("Creating {0} Invoice", [frm.doc.invoice_type]),
			});
		});

		// if (frm.doc.create_missing_party) {
		// 	frm.set_df_property("party", "fieldtype", "Data", frm.doc.name, "invoices");
		// }
	},
});
