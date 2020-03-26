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
//                         frm.set_value('status', "In-Progress");
                        frm.refresh();
                    }
                });
            }).addClass("btn-primary");
        
        
// 	        frm.add_custom_button(__('Start Collection'), function () {
// 				return frappe.call({
// 				    method:"dairy.milk_entry.doctype.van_collection.van_collection.van_start_collection",
// 				    args: {
// 				        name: frm.doc.name
// 			        }
// 				});
// 				callback: function(frm) {
// 				    frm.refresh();
// 				}
// 			},).addClass("btn-primary");
        }
              
            
            
        
        if (frm.doc.status=='In-Progress'){
            frm.add_custom_button(__('Add / Edit Collection'), function () {
                frappe.set_route('query-report','Collection Item Details',
                    {'parent':frm.doc.name,'company':frm.doc.company});
            },).addClass("btn-primary");
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
