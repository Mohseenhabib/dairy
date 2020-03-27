// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Van Collection', {
	refresh: function(frm) {
        if (frm.doc.status=='Submitted'){
            frm.add_custom_button(__('Start Collection'), function () {
                return frappe.call({
                    doc: frm.doc,
                    method: 'van_start_collection',
                    callback: function(r) {
//                        frm.set_value('status', "In-Progress");
                        frm.refresh();
                    }
                });
            }).addClass("btn-primary");
        }
        if (frm.doc.status=='In-Progress'){

            frm.add_custom_button(__('Add / Edit Collection'), function () {
                frappe.route_options = {"van_collection": frm.doc.name};
                frappe.set_route("Report", "Van Collection Items");
            });

            frm.add_custom_button(__('Make Stock Entry'),function() {
                return frappe.call({
                    doc: frm.doc,
                    method: 'make_stock_entry',
                    callback: function(r) {
                        var doc = frappe.model.sync(r.message);
                        frappe.set_route("Form", doc[0].doctype, doc[0].name);
                    }
                });
            }).addClass('btn-primary');
        }
    },
    before_submit: function(frm) {
        return frm.call('submit_van_collection').then(() => {
            frm.refresh_field('status');
        });
    },
    onload: function(frm){
        frm.set_query('route', function(doc) {
            return {
                filters: {
                    "route_type":"Buying"
                }
            };
        });
    },
});
