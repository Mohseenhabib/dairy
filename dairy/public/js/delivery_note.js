frappe.ui.form.on("Delivery Note", {
    setup: function(frm) {
		frm.add_fetch("route", "source_warehouse", "set_warehouse");
		frm.add_fetch("route", "price_list", "selling_price_list");
		frm.add_fetch("route", "transporter", "transporter");
	},
    after_save:function(frm,cdt,cdn){
        var d = locals[cdt][cdn];
        console.log(d);
        $.each(d.items, function(index, row)
        {   
            var a = ((row.amount)/row.total_weight) 
            row.rate_of_stock_uom=a;
            console.log("Rate of stock uom",a)
            frm.refresh_field("rate_of_stock_uom")
        });
    },
//	calculate_crate: function(frm){
//	console.log("******************************************");
////	    cur_frm.cscript.calculate_crate()
//	    frm.call({
//        method:"dairy.milk_entry.custom_delivery_note.calculate_crate",
//        args: {
//                doc: cur_frm
//              },
//        callback: function(r)
//            {
//               cur_frm.reload_doc();
//            }
//        });
//
//	},
	refresh: function(frm){
        if (frm.doc.docstatus==1) {
				frm.remove_custom_button("Delivery Trip", 'Create');
			}
	},
	onload: function(frm){
	    if(frm.doc.__islocal){
//	         frm.set_df_property("calculate_crate", "hidden",1);
	         frm.set_df_property("crate_count", "hidden",1);
	         frm.set_df_property("loose_crate_", "hidden",1);
	    }
	    frm.trigger('set_property');
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


    after_save: function(frm){
            frm.set_df_property("crate_count", "hidden",0);
	        frm.set_df_property("loose_crate_", "hidden",0);
	        cur_frm.reload_doc();
      },

	customer:function(frm){
        return cur_frm.call({
            method:"dairy.milk_entry.custom_delivery_note.get_route_price_list",
            args: {
                    doc_name: cur_frm.doc.customer
                  },
            callback: function(r)
                {
                   if(r.message)
                   {
                    frm.set_value("route",r.message.route);
                     frm.set_value("selling_price_list",r.message.p_list);
                     frm.set_value("set_warehouse",r.message.warehouse);
                   }
                }
        });
    },

    route: function(frm){
        frm.add_fetch("route", "transporter", "transporter");
    },

    customer: function(frm){
        frappe.call({
            method: 'dairy.milk_entry.doctype.bulk_milk_price_list.bulk_milk_price_list.fetch_data',
            args: {
                'doctype': 'Bulk Milk Price List',
                'customer': frm.doc.customer
            },
            callback: function(r) {
                if (!r.exc) {
                    // code snippet
                    frm.set_value('fat_rate', r.message.rate)
                    frm.set_value('snf_clr_rate', r.message.snf)
                }
            }
        });
    }
});
 
frappe.ui.form.on("Delivery Note Item", {
    item_code: function(frm,cdt,cdn){
        let item = locals[cdt][cdn]
        frappe.call({
            method: "dairy.milk_entry.doctype.bulk_milk_price_list.bulk_milk_price_list.fetch_snf_and_fat",
            args: {
                "item": item.item_code,
                "customer": frm.doc.customer
            },
            callback: function(resp){
                if(resp.message){
                    let d = resp.message

                    item.fat_amount = d.rate * item.fat
                    item.snf_clr_amount = d.snf_clr_rate * item.snf_clr
                    frm.refresh_field('fat_amount')
                    frm.refresh_field('snf_clr_amount')
                }
            }
        })
    }
})

//cur_frm.cscript.calculate_crate = function(frm){
//    return cur_frm.call({
//        method:"dairy.milk_entry.custom_delivery_note.calculate_crate",
//        args: {
//                doc: cur_frm
//              },
//        callback: function(r)
//            {
//               cur_frm.reload_doc();
//            }
//    });
//}

//frappe.ui.form.on("Delivery Note Item", {
//	fat: function(frm,cdt,cdn) {
//	    console.log("****************************************fat");
//		var row = locals[cdt][cdn];
//		if (row.snf_clr){
//            frm.call({
//				method: 'dairy.milk_entry.custom_delivery_note.change_rate',
//				args: {
//					item_code: row.item_code,
//					warehouse: row.warehouse,
//					posting_date: frm.doc.posting_date,
//					fat: row.fat,
//					snf_clr: row.snf_clr
//				},
//				callback: function(r) {
//					if(r.message) {
//					    row.rate = r.message;
//					}
//				}
//			});
//		}
//
//	},
//	snf_clr: function(frm,cdt,cdn) {
//		var row = locals[cdt][cdn];
//		if (row.fat){
//		    frm.call({
//				method: 'dairy.milk_entry.custom_delivery_note.change_rate',
//				args: {
//					item_code: row.item_code,
//					warehouse: row.warehouse,
//					posting_date: frm.doc.posting_date,
//					fat: row.fat,
//					snf_clr: row.snf_clr
//				},
//				callback: function(r) {
//					if(r.message) {
//					    row.rate = r.message;
//					    frm.refresh();
//					}
//				}
//			});
//		}
//
//	},
//
//});