frappe.ui.form.on("Delivery Note", {
    setup: function(frm) {
		frm.add_fetch("route", "source_warehouse", "set_warehouse");
		frm.add_fetch("route", "price_list", "selling_price_list");
	},
	calculate_crate: function(frm){
	    cur_frm.cscript.calculate_crate()
	},
	refresh: function(frm){
//        if(!frm.doc.__islocal && frm.doc.docstatus == 0)
//        {
//            frm.add_custom_button(__('Calculate Crate'), function() {
//				cur_frm.cscript.calculate_crate()
//			}).addClass("btn-primary");
//        }

        if (frm.doc.docstatus==1) {
				frm.remove_custom_button("Delivery Trip", 'Create');
			}

	},
	onload: function(frm){
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

	before_save: function(frm){
	    var count = 0;
	    var lp = 0;
	    var lst = [];
       $.each(frm.doc["items"],function(i, items)
            {
                lst[lp] = items.against_sales_order
                lp += 1;
            });
       frm.call({
                method: "dairy.milk_entry.custom_delivery_note.delivery_shift",
                args: {name: lst[0]},
                callback: function(r) {
                    if(r.message){
                         var array = String(r.message[0]);
                         frm.set_value("shift",array);
                    }
                }
            });


//      frm.call({
//            method: "dairy.milk_entry.custom_delivery_note.calculate_crate",
//            args: {doc_name: cur_frm.doc.name},
//            callback: function(r) {
//                if(r.message){
//                     cur_frm.reload_doc();
//                }
//            }
//            });
//       for(var i=0;i<(lst.length - 1);i++){
//            if(lst[i] != lst[i+1]){
//                count = count+1;
//                console.log("******",count)
//            }
//            if(count > 0){
//                frm.clear_table("items");
//                frm.refresh_fields();
//                frm.reload_doc();
//                frappe.validated = false;
//                frappe.throw("Select only one sales order to fetch items");
//                    }
//            else{
//                         frm.call({
//                                method: "dairy.milk_entry.custom_delivery_note.delivery_shift",
//                                args: {name: lst[0]},
//                                callback: function(r) {
//                                    if(r.message){
//                                         var array = String(r.message[0]);
//                                         frm.set_value("shift",array);
//                                    }
//                                }
//                            });
//                    }
//       }

//	   $.each(frm.doc["items"],function(i, items)
//            {
//                if(items.item_code){
//                    count = count+1;
//                    if(count > 1){
//                        frm.clear_table("items");
//                        frm.refresh_fields();
//						frm.reload_doc();
//                        frappe.validated = false;
//                        frappe.throw("Select only one sales order to fetch items");
//                    }
//                    else{
//                         frm.call({
//                                method: "dairy.milk_entry.custom_delivery_note.delivery_shift",
//                                args: {name: items.against_sales_order},
//                                callback: function(r) {
//                                    if(r.message){
//                                         var array = String(r.message[0]);
//                                         frm.set_value("shift",array);
//                                    }
//                                }
//                            });
//                    }
//                }
//            });
	},
	after_save: function(frm){
	    cur_frm.cscript.calculate_crate()
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
    }
});


cur_frm.cscript.calculate_crate = function(){
    return cur_frm.call({
        method:"dairy.milk_entry.custom_delivery_note.calculate_crate",
        args: {
                doc_name: cur_frm.doc.name
              },
        callback: function(r)
            {
               cur_frm.reload_doc();
            }
    });
}
