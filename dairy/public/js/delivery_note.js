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
