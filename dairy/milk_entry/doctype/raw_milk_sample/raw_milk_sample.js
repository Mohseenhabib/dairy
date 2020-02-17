// Copyright (c) 2019, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt
// frappe.provide("dairy.milk_entry");

frappe.ui.form.on('Raw Milk Sample', {
    // refresh: function(frm) {
    
    onload: function(frm){
        frm.set_query('dcs_id', function(doc) {
            return {
                filters: {
                    "is_dcs":1,
                    "sample_collector":1,
                }
            };
        });
    },
    

    dcs_id:function(frm){
        frm.set_query("milk_entry","sample_lines", function() {
            console.log("======frm.doc.dcs_id",frm.doc.dcs_id);
            return {
                filters: {
                    "dcs_id": frm.doc.dcs_id,
                    "docstatus": 1,
                    "date":["=",frm.doc.date]
                }
            }
        });
    },




    refresh: function(frm, cdt, cdn) {
        var me = this;
        console.log("=========dcs_id",frm.doc.dcs_id);
        console.log("=========doc",frm.doc,"====date",frm.doc.date);
        
       if (frm.doc.docstatus==0) {
            frm.add_custom_button(__('Milk Entry'),
                function() {
                        // console.log("====dcs",frm.doc.dcs_id==undefined);
                        // console.log("===frm.doc.dcs_id",frm.doc.dcs_id);
                        // let dcs = frappe.model.get_doc("Warehouse",frm.doc.dcs_id);
                        // console.log("===dcs",dcs);
                        // let is_collector = dcs.sample_collector;

                        if (frm.doc.dcs_id==undefined){
                            frappe.throw(__("Please Provide DCS"));
                        }
                        // if (is_collector === 0) {
                        //     frappe.throw(__("DCS is not Sample Collector"));
                        // }

                        erpnext.utils.map_current_doc({
                        method: "dairy.milk_entry.doctype.milk_entry.milk_entry.make_delivery_note",
                        source_doctype: "Milk Entry",
                        target: frm,
                        setters: {
                            dcs_id: frm.doc.dcs_id || undefined,
                            date :frm.doc.date || undefined,
                        },
                        get_query_filters: {
                            docstatus: 1,
                            sample_created:0
                        }
                    })
                }, __("Get items from"));
       }
    }
    

});

// frappe.ui.form.on("Sample lines", {
//
//     milk_entry: function(frm) {
//         return frm.call('get_milk_entry_data').then(() => {
//             frm.refresh_field('dcs_id');
//             frm.refresh_field('milk_type');
//             frm.refresh_field('fat');
//             frm.refresh_field('clr');
//         });
//     },
// });

// dairy.milk_entry.MilkSampleController = dairy.milk_entry.MilkEntryController.extend({
// 
// //     
//     
//     
//     
//     refresh: function(doc, dt, dn) {
//         var me = this;
//         if (doc.docstatus==0) {
//             this.frm.add_custom_button(__('Milk Entry'),
//                 function() {
//                     erpnext.utils.map_current_doc({
//                         method: "dairy.milk_entry.doctype.milk_entry.make_delivery_note",
//                         source_doctype: "Milk Entry",
//                         target: me.frm,
//                         setters: {
//                             customer: me.frm.doc.customer || undefined,
//                         },
//                         get_query_filters: {
//                             docstatus: 1,
//                         }
//                     })
//                 }, __("Get items from"));
//             
//         }
//     }
//     
//     
//     
//     
// });