
frappe.ui.form.on("Sales Order", {
    setup: function(frm) {
		frm.add_fetch("route", "source_warehouse", "set_warehouse");
		frm.add_fetch("route", "price_list", "selling_price_list");
	},
	validate: function(frm) {
        // var otm = frappe.model.get_value("Dairy Settings","Dairy Settings","morning_locking_time");
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes();
        
        frappe.model.get_value('Dairy Settings', {'name': 'Dairy Settings'}, 'morning_locking_time', function(d)
        {
            var otm = d.morning_locking_time;  
            var td = frappe.datetime.add_days(frappe.datetime.get_today(),1);
            
            if (frm.doc.delivery_shift == 'Morning') 
            {            
                if(frm.doc.delivery_date == frappe.datetime.get_today())
                {
                    frappe.validated = false;
                    frappe.throw(__('Order locking time is over'));
                    
                }
                if(frm.doc.delivery_date == td)
                {
                    if(time > otm)
                    {
                        frappe.validated = false;
                        frappe.throw(__('Order locking time is over'));
                    }
                }
            }
        });

        frappe.model.get_value('Dairy Settings', {'name': 'Dairy Settings'}, 'evening_locking_time', function(e)
        {
            var ote = e.evening_locking_time;
            if(frm.doc.delivery_shift == 'Evening')
            {
                if(frm.doc.delivery_date == frappe.datetime.get_today())
                {
                    if(time > ote)
                    {
                        frappe.validated = false;
                        frappe.throw(__('Order locking time is over'));
                    }
                }
            }
        });
    },
    delivery_shift: function(frm){
        if (frm.doc.delivery_shift == 'Morning')
        {
            var td = frappe.datetime.add_days(frappe.datetime.get_today(),1);
            frm.set_value("delivery_date",td);
        }
        else
        {
             frm.set_value("delivery_date",frappe.datetime.get_today());
        }
    }
});
