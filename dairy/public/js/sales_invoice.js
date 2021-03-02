frappe.ui.form.on("Sales Invoice", {
    setup: function(frm) {
		frm.add_fetch("route", "price_list", "selling_price_list");
	},
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

frappe.ui.form.on("Sales Invoice Item", {
	item_code: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		frm.call({
            method:"dairy.milk_entry.custom_sales_order.defsellinguom",
            args: {
                    doc_name: row.item_code
                  },
            callback: function(r)
                {
                   if(r.message)
                   {
                    var array = r.message
                    if (array != 1){
                    row.uom = array["uom"];
                    row.conversion_factor = array["conversion_factor"];
                    }
                   }
                }
        });
	}
});
