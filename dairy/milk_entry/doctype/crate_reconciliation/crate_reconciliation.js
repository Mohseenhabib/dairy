// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Crate Reconciliation', {
	 refresh: function(frm) {
	        if (!frm.doc.__islocal)
	        {
                frm.add_custom_button(__('Delivery Note'),function() {
                    erpnext.utils.map_current_doc({
                        method: "dairy.milk_entry.doctype.crate_reconciliation.crate_reconciliation.make_delivery_note",
                        source_doctype: "Delivery Note",
                        target: frm,
                        date_field: "posting_date",
                        setters : [
                                    {   label : "Customer",
                                        fieldname : "customer",
                                        fieldtype : "Link",
                                        options :"Customer"
                                    }
                                ],
                        get_query_filters: {
                            company: frm.doc.company,
                            docstatus: 1,
                            disable: 0,
                        }
                    })
                }, __("Get items from"));

	        }
	 },
	 onload: function(frm){
        frm.set_query('route', function(doc) {
            return {
                filters: {
                    "customer":frm.doc.customer,
                    "company":frappe.defaults.get_user_default("Company"),
                }
            };
        });
     }

});

frappe.ui.form.on("Crate Reconciliation Child", {
	outgoing: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
			row.difference = row.outgoing -row.incoming
	},
	incoming: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
			row.difference = row.outgoing -row.incoming
	}
});
