frappe.ui.form.on("Sales Invoice", {
    setup: function(frm) {
		frm.add_fetch("route", "price_list", "selling_price_list");
	},
	onload: function(frm){

        frm.set_query('route', function(doc) {
            return {
                filters: {
                    "company":doc.company,
                    "route_type":"Milk Marketing"
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

                   }
                }
        });
    },
    route:function(frm){
	         return cur_frm.call({
            method:"dairy.milk_entry.custom_sales_order.set_territory",
            args: {

                  },
            callback: function(r)
                {
                   if(r.message)
                   {
                    console.log(r.message);
                    if(r.message == "Route"){
                        frm.set_value("territory",frm.doc.route_territory);
                    }
                   }
                }
        });
    }
})
