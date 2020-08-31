// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Pass', {
     onload : function(frm){
        frm.set_query('route', function(doc) {
            return {
                filters: {
                    "company":doc.company,
                     "route_type":"Milk Marketing",
                    "docstatus":1
                }
            };
        });

        frm.set_query('transporter', function() {
			return {
				filters: {
					'is_transporter': 1
				}
			}
		});
     },
	 refresh: function(frm) {
	        if(! frm.doc.__islocal){
	            frm.set_df_property("items_section", "hidden", 1);
	        }
	        if( frm.doc.__islocal){
	            frm.set_df_property("merge_items", "hidden", 1);
	            frm.set_df_property("crate_count_section", "hidden", 1);
                frm.set_df_property("loose_crate_section", "hidden", 1);
	        }
	        if ((frm.is_new())) {
            if (frm.doc.docstatus===0) {
				frm.add_custom_button(__('Delivery Note'),
					function() {
						erpnext.utils.map_current_doc({
							method: "dairy.milk_entry.doctype.gate_pass.gate_pass.make_delivery_note",
							source_doctype: "Delivery Note",
							target: me.frm,
							setters: [
                            {
                                label: "Date",
                                fieldname: "posting_date",
                                fieldtype: "Date",
                                default: frm.doc.date || undefined,
                            },
                            {
                                label: "Route",
                                fieldname: "route",
                                fieldtype: "Link",
                                options: "Route Master",
                                default: frm.doc.route || undefined,
                            },
                            {
                                label: "Shift",
                                fieldname: "shift",
                                fieldtype: "Data",
                                default: frm.doc.shift || undefined,
                            },
                            {
                                label: "Transporter",
                                fieldname: "transporter",
                                fieldtype: "Link",
                                options: "Supplier",
                                default: frm.doc.transporter || undefined,
                            }
                        ],
							get_query_filters: {
								docstatus: 1,
								status: ["=", ["To Bill"]],
                                crate_gate_pass_done:0
							}
						})
						frappe.msgprint("After getting item. Save the document to see item details...");
					}, __("Get items from"));
			}
			}
	 },

	 after_save: function(frm){
            if(frm.doc.status != "Draft"){
                frm.call({
                        method:"dairy.milk_entry.doctype.gate_pass.gate_pass.merge_items",
                        args: {
                            doc_name: frm.doc.name
                        },
                        callback: function(r) {
                            }
                        });
//                        cur_frm.refresh();
//                        cur_frm.reload_doc();
                frappe.ui.toolbar.clear_cache();
            }

	 },

    before_save: function(frm){
        var total = 0;
         $.each(frm.doc["item"],function(i, item)
	    {
             if(item.item_code){
                total += 1;
             }
	    });
	    if(total == 0){
	        frappe.validated = false;
	        frappe.throw("Get items from delivery note and then save doc to see items information");
	    }
    },

     after_submit:function(frm){
        // knowingly leave empty to resolve method callling of after_save on submit button

	 },

    calculate_crate: function(frm){
                return cur_frm.call({
                    method:"dairy.milk_entry.doctype.gate_pass.gate_pass.calculate_crate",
                    args: {
                            doc_name: cur_frm.doc.name
                          },
                    callback: function(r)
                        {
                           cur_frm.reload_doc();
                        }
                });
        },
});

//cur_frm.cscript.calculate_crate = function(){
//
//        return cur_frm.call({
//            method:"dairy.milk_entry.doctype.gate_pass.gate_pass.merge_items",
//            args: {
//                doc_name: frm.doc.name
//            },
//            callback: function(r) {
//            frappe.ui.toolbar.clear_cache();
//                }
//            });
//    return cur_frm.call({
//        method:"dairy.milk_entry.doctype.gate_pass.gate_pass.calculate_crate",
//        args: {
//                doc_name: cur_frm.doc.name
//              },
//        callback: function(r)
//            {
//               cur_frm.reload_doc();
//            }
//    });
//}