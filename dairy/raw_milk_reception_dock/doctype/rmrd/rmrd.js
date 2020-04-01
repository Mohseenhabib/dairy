// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('RMRD', {
	 refresh: function(frm) {
//	    if(!frm.doc.__islocal && frm.doc.docstatus == 0)
//	    {
//            frm.add_custom_button(__('Get Van Collection Data'), function () {
//                 return frappe.call({
//                    doc: frm.doc,
//                    method: 'get_van_collection',
//                    callback: function(r) {
//                        frm.refresh();
//                    }
//                });
//            }).addClass("btn-primary");
//        }
        if (frm.doc.docstatus == 1){
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
