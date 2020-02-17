// Copyright (c) 2019, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Milk Rate', {
	milk_type: function(frm) {
	    return frm.call('get_snf_lines').then(() => {
            frm.refresh_field('milk_rate_chart');
        });
	},
	onload(frm) {
        if(frm.doc.__islocal) {
            return frm.call('get_snf_lines').then(() => {
                frm.refresh_field('milk_rate_chart');
            });
        }
    },

    
    validate: function(frm) {
        if(!frm.doc.milk_rate_chart) {
            frappe.throw(__('Cant Submit without Rate Chart.'));
        }
    },

    before_submit : function (frm) {
        for(let i in frm.doc.milk_rate_chart){
            if (frm.doc.milk_rate_chart[i].rate <= 0){
                frappe.throw(__('Rate must be greater then zero on row '+(parseInt(i,10)+1)));
            }
        }
    },
    
//     dcs_name:function(frm){ 
//         frm.fields_dict['dcs_name'].grid.get_field("warehouse_id").get_query = function(doc, cdt, cdn) 
//         { 
//         return { 
//                 filters: {
//                     "is_dcs":1,
//                 }
// //             filters: 
// //                 [ 
// //                     ['DocType', 'is_dcs', '=',1] 
// //                 ] 
//                 } 
//         } 
//     }
});


// frappe.ui.form.on("Warehouse Child", {
// 
//     warehouse_id: function(frm){
//         frm.set_query('warehouse_id', function(doc) {
//             return {
//                 filters: {
//                     "is_dcs":1,
//                 }
//             };
//         });
//     },
// });
