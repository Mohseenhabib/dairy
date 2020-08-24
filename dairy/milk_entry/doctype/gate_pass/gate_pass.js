// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Pass', {
	 refresh: function(frm) {
	        if(! frm.doc.__islocal){
	            frm.set_df_property("items_section", "hidden", 1);
	        }
	        if( frm.doc.__islocal){
	            frm.set_df_property("merge_items", "hidden", 1);
	        }
            if (frm.doc.docstatus===0) {
				frm.add_custom_button(__('Delivery Note'),
					function() {
						erpnext.utils.map_current_doc({
							method: "dairy.milk_entry.doctype.gate_pass.gate_pass.make_delivery_note",
							source_doctype: "Delivery Note",
							target: me.frm,
							setters: {

							},
							get_query_filters: {
								docstatus: 1,
								status: ["=", ["To Bill"]]

							}
						})
					}, __("Get items from"));
			}
	 },

	 after_save: function(frm){
                frm.call({
                        method:"dairy.milk_entry.doctype.gate_pass.gate_pass.merge_items",
                        args: {
                            doc_name: frm.doc.name
                        },
                        callback: function(r) {
                            }
                        });
                        frappe.ui.toolbar.clear_cache();
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