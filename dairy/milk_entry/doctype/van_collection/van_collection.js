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
    
//     validate: function(frm) {
//         var van_colle = frappe.db.get_value("Van Collection",{
//                             "route": frm.doc.route,
//                             "date":frappe.datetime.get_today(),
//                             "shift":frm.doc.shift,
//                             "vehicle":frm.doc.vehicle,
//                             "status":["!=","Cancelled"]
//                             })
//         console.log("van_colle",van_colle)
//         if (van_colle){
//             frappe.throw(__("Already vehicle has been scheduled in this period."))
//             }
//         frm.call('check_van_collections').then(() => {
//             frm.refresh_field('status');
//         });
//     }
});
