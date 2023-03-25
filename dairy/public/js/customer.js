// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", {
    onload: function(frm){
        frm.set_query('route', function(doc) {
            return {
                filters: {
                    "company":doc.company,
                     "route_type":"Milk Marketing",
                    "docstatus":1
                }
            };
        });
    },
    refresh: function(frm,cdt,cdn){
        frm.fields_dict['links'].grid.get_field('link_name').get_query = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn]
            return {    
                filters:[
                    ['docstatus', '!=', 2]
                   
                ]
            }

        }
    }
});
// frappe.ui.form.on('Dynamic Link', {
//     link_doctype:function(frm,cdt,cdn){
//         console.log('%%%%%%%%%%%%%%%%')
//         var child = locals[cdt][cdn]
//         if(child.link_doctype){
//             var sub = 0;
//             frappe.db.get_doc('DocType',child.link_doctype).then(ld => {
//                 if (ld.is_submittable == 1){
//                     var sub = 1
//                 }
//             })
//             if(sub == 1){
            
//         }
            
//         }
//     }
    
// });