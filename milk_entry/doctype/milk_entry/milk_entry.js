// Copyright (c) 2019, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Milk Entry', {

    onload: function(frm){
        frm.set_query('dcs_id', function(doc) {
            return {
                filters: {
                    "is_dcs":1,
                    "is_group":0,
                    "company":frappe.defaults.get_user_default("Company"),
                    "disabled":0
                }
            };
        });

    },

    validate: function(frm) {

        if(!frm.doc.dcs_id) {
            frappe.throw(__('Please provide DCS.'));
        }
        if(!frm.doc.member) {
            frappe.throw(__('Please provide Member.'));
        }

        if(!frm.doc.volume) {
            frappe.throw(__('Please provide Volume.'));
        }
        if(!frm.doc.fat) {
            frappe.throw(__('Please provide FAT.'));
        }
        if(!frm.doc.clr) {
            frappe.throw(__('Please provide CLR.'));
        }

        if(frm.doc.volume <= 0) {
            frappe.throw(__('Milk Volume less than or equal to zero is not allowed.'));
        }
        if(frm.doc.fat <= 0) {
            frappe.throw(__('Milk FAT less than or equal to zero is not allowed.'));
        }
        if(frm.doc.clr <= 0) {
            frappe.throw(__('Milk CLR less than or equal to zero is not allowed.'));
        }
        
        
//         return frm.call('get_pricelist').then(() => {
//             frm.refresh_field('milk_rate');
//             frm.refresh_field('unit_price');
//             frm.refresh_field('total');
//         });
        
    },
    
    
    dcs_id: function(frm) {
    
        frm.set_query('member', function(doc) {
            return {
                filters: {
                    "dcs_id": doc.dcs_id,
                }
            };
        });

    },
    
    
    
    refresh: function(frm) {
         console.log("=======frm.doc.member",frm.doc.member)
         if (frm.doc.docstatus===0 && frm.doc.member !== undefined){

            frm.add_custom_button(__('Accounting Ledger'), function () {
				frappe.set_route('query-report', 'General Ledger',
					{ party_type: 'Supplier', party: frm.doc.member,'company':frm.doc.company });
			}, __("View"));

			frm.add_custom_button(__('Accounts Payable'), function () {
				frappe.set_route('query-report', 'Accounts Payable',
				{supplier: frm.doc.member,'company':frm.doc.company });
			}, __("View"));
//             frm.add_custom_button(__('New Member'),function(){
//                frappe.model.open_mapped_doc({
//                    method: "dairy.milk_entry.doctype.milk_entry.milk_entry.create_new_member",
//                    frm:cur_frm,
//                })
//             }, __('Create'));
//             frm.page.set_inner_btn_group_as_primary(__('Create'));
         }



        if (frm.doc.docstatus===1) {
            frappe.model.with_doc("Warehouse",frm.doc.dcs_id, () => {
                let dcs = frappe.model.get_doc("Warehouse",frm.doc.dcs_id);
                let is_collector = dcs.sample_collector
                if (is_collector === 1) {
                    frm.add_custom_button(__('Raw Milk Sample'), function () {
                        frappe.model.open_mapped_doc({
                            method: "dairy.milk_entry.doctype.milk_entry.milk_entry.create_raw_sample",
                            frm: cur_frm,
                        })
                    }, __('Create'));
                }
            });

            // frm.add_custom_button(__('Purchase Receipt'), () => frm.create_purchase_receipt(), __('Create'));
            frm.add_custom_button(__('Purchase Receipt'),function() {
                frappe.model.open_mapped_doc({
                    method: "dairy.milk_entry.doctype.milk_entry.milk_entry.create_purchase_receipt",
                    frm: cur_frm,
                })
                // frm.reload_doc();
                // callback: function(r) {
                //     r.refresh()
                // },
                // callback: function(r){
                // console.log("======test====sid")
                // page.item_dashboard.refresh();
			    // }
            },__('Create'));

            // frm.add_custom_button(__('Purchase Invoice'),function() {
            //     frappe.model.open_mapped_doc({
            //         method: "dairy.milk_entry.doctype.milk_entry.milk_entry.create_purchase_invoice",
            //         frm: cur_frm,
            //     })
            // },__('Create'));

            // frm.add_custom_button(__('Payment Entry'),function () {
            //     frappe.model.open_mapped_doc({
            //         method: "dairy.milk_entry.doctype.milk_entry.milk_entry.create_payment_entry",
            //         frm: cur_frm,
            //     })
            // },__('Create'));

            frm.page.set_inner_btn_group_as_primary(__('Create'));

            
            
        }

    },

    // create_purchase_receipt:function() {
    //     console.log("=====this",this)
    //     frappe.model.open_mapped_doc({
    //         method: "dairy.milk_entry.doctype.milk_entry.milk_entry.create_purchase_receipt",
    //         frm: frm,
    //     })
    //     frm.reload_doc();
	// },
    
//     get_pricelist : function(frm){
//         return frappe.call({
//             method: 'dairy.milk_entry.doctype.milk_entry.milk_entry.get_pricelist',
//             args: {name:frm.name},
//             callback: function(r) {
//                 if (!r.exc) {
//                     // code snippet
//                 }
//             }
//         })
//         
//     }
    
    before_submit: function(frm) {
        return frm.call('get_pricelist').then(() => {
            frm.refresh_field('milk_rate');
            frm.refresh_field('unit_price');
            frm.refresh_field('total');
        });
    },
    


    
//     validate: function(frm) {
//         if(frm.doc.name=="All Departments") {
//             frappe.throw(__("You cannot edit root node."));
//         }
//     }
    
    
//     function get_pricelist(frm) {
//     if(frm.doc.){
//         erpnext.utils.copy_value_in_all_rows(frm.doc, frm.doc.doctype, frm.doc.name, "items", "schedule_date");
//     }
// }
    
});
//var current_user = frappe.session.user;
//var e = window.event;
//frappe.ui.form.on("Milk Entry",{
//	verify: function(frm) {
//		frappe.call({
//			method: "frappe.client.get",
//			args: {
//				doctype: "User",
//				filters: {"email":current_user}    //user is current user here
//			},
//			callback: function(r) {
//			    if (!cur_frm.doc.member || !cur_frm.doc.milk_type || cur_frm.doc.volume <= 0)
//			    {
//			        frappe.throw("Please fill all filed Data")
//			    }
//			    else
//			    {
//			        var v=frappe.model.add_child(cur_frm.doc,"Milk Entry List","milk_list");
//                    frappe.model.set_value(v.doctype, v.name, "code",cur_frm.doc.member)
//                    frappe.model.set_value(v.doctype, v.name, "milk_type",cur_frm.doc.milk_type)
//                    frappe.model.set_value(v.doctype, v.name, "volume",cur_frm.doc.volume)
//
//                    frm.refresh_field('milk_list');
//                    cur_frm.set_value("member",r.message["member"]);
//                    cur_frm.set_value("milk_type",r.message["milk_type"]);
//                    cur_frm.set_value("volume",r.message["volume"]);
//                    cur_frm.save();
//			    }
//			}
//		})
//	},
//})


