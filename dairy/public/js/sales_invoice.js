frappe.ui.form.on("Sales Invoice", {
    setup: function(frm) {
		frm.add_fetch("route", "price_list", "selling_price_list");
	},
	onload: function(frm){
        // frm.set_df_property("crate_count", "hidden",1);
        // frm.set_df_property("loose_crate_", "hidden",1);

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
       
        // frm.set_df_property("crate_count", "hidden",0);
        // frm.set_df_property("loose_crate_", "hidden",0);
        // cur_frm.reload_doc();
      
    },
    
    customer:function(frm){
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
                    frm.refresh_field("route")
                     frm.set_value("selling_price_list",r.message.p_list);
                     frm.refresh_field("selling_price_list")

                   }
                }
        });
    },
    route:function(frm){
        frm.add_fetch("route", "transporter", "transporter");
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
    
    },

    // customer: function(frm){
        
    // },
    // calculate_crate: function(frm){
    //     frm.call({
    //            method:"dairy.milk_entry.custom_sales_invoice.calculate_crate",
    //            args: {
    //                    doc: cur_frm
    //                  },
    //            callback: function(r)
    //                {
    //                   frm.refresh_field("crate_count")
    //                }
    //            });
        
    //     	},
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
