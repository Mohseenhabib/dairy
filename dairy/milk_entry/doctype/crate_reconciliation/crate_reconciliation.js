// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Crate Reconciliation', {
	 refresh: function(frm, dt, dn) {
        if (frm.doc.docstatus ==0)
        {
            frm.add_custom_button(__('Delivery Note'),function() {
                erpnext.utils.map_current_doc({
                    method: "dairy.milk_entry.doctype.crate_reconciliation.crate_reconciliation.make_delivery_note",
                    source_doctype: "Delivery Note",
                    target: frm,
                    date_field: "posting_date",
                    setters: {
                            customer: frm.doc.customer || undefined,
                            route: frm.doc.route || undefined
                        },
                    get_query_filters: {
                        company: frm.doc.company,
                        route: frm.doc.route,
                        crate_reconcilation_done:0,
                        docstatus: 1
                    }
                })
            }, __("Get items from"));
        }
        if (frm.doc.docstatus ==1)
        {
            frm.add_custom_button(__('Create Invoice'),function() {
                return frappe.call({
                    doc: frm.doc,
                    method: 'make_sales_invoice',
                    callback: function(r) {
                        var doc = frappe.model.sync(r.message);
                        frappe.set_route("Form", doc[0].doctype, doc[0].name);
                    }
                });
            }).addClass('btn-primary');
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
     },
     before_submit: function(frm)
     {
         return frappe.call({
            doc: frm.doc,
            method: 'calculate_crate_type_summary',
            callback: function(r) {
                frm.reload_doc();
            }
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
