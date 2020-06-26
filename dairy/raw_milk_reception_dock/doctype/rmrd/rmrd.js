// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('RMRD', {
	 refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.docstatus == 0 && !frm.doc.hide_start_rmrd_button){
            frm.add_custom_button(__('Start RMRD'), function () {
                return frappe.call({
                    doc: frm.doc,
                    method: 'start_rmrd',
                    callback: function(r) {
                        frm.refresh();
                    }
                });
            }).addClass("btn-primary");
        }

        frm.add_custom_button(__('Add / Edit RMRD'), function () {
            frappe.route_options = {"rmrd": frm.doc.name};
            frappe.set_route("Report", "RMRD Lines");
        });

//        if(frm.doc.docstatus == 1 && !frm.doc.stock_entry)
//        {
//            frm.add_custom_button(__('Make Stock Entry'),function() {
//                return frappe.call({
//                    doc: frm.doc,
//                    method: 'make_stock_entry',
//                    callback: function(r) {
//                        var doc = frappe.model.sync(r.message);
//                        frappe.set_route("Form", doc[0].doctype, doc[0].name);
//                    }
//                });
//            }).addClass('btn-primary');
//        }
	 },
	 onload: function(frm){
        frm.set_query('route', function(doc) {
            return {
                filters: {
                    "route_type":"Buying"
                }
            };
        });
        frm.set_query('target_warehouse', function(doc) {
            return {
                filters: {
//                    "is_dcs":0,
                    "is_group":0,
                    "company":frappe.defaults.get_user_default("Company"),
                    "disabled":0
                }
            };
        });
    },
});
