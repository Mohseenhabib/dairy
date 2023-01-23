// Copyright (c) 2019, Dexciss Technology by Sid and contributors
// For license information, please see license.txt

frappe.ui.form.on('Dairy Settings', {
    onload: function(frm) {
        frm.trigger('set_property');
        if(frm.doc.__islocal){
            frm.set_value("get_territory","Customer");

        }
        if(! frm.doc.leakage_calculated_on)
        {
        frm.set_value("leakage_calculated_on","Sales Order");
        }

        if(! frm.doc.crate_reconciliation_based_on){
            frm.set_value("crate_reconciliation_based_on","Delivery Note");
        }

    },
    set_property: function(frm) {
        if(frm.doc.default_payment_type =="Daily")
         {
            frappe.call({
                method: 'dairy.milk_entry.doctype.dairy_settings.dairy_settings.purchase_invoice',
                // args: {employee: frm.doc.employee, fieldname: property},
            });
            console.log('purchase_incoiveEEEEEEEEEEEEEEEEEEEE')
         }
         if(frm.doc.default_payment_type =="Days")
         {
            frm.set_df_property("days", "reqd", 1);
         }
         else
         {
            frm.set_df_property("days", "reqd", 0);
         }
         
    },
    default_payment_type :function(frm){
        

        frm.trigger('set_property');
        
    },
	validate: function(frm) {
		if(frm.doc.max_allowed > frm.doc.can_volume)
		{
			frappe.throw(__(" 'Max Allowed Capacity' should be equal to or less than 'Can Volume' "));
		}
		if(frm.doc.default_payment_type =="Days" && frm.doc.days ==0)
		{
		    frappe.throw(__("Set Days greater than the Zero!"));
		}
	},
	
	// purchase_invoice: function(frm){
    //     frappe.call({
	// 		method: 'dairy.milk_entry.doctype.dairy_settings.dairy_settings.purchase_invoice',
	// 		// args: {employee: frm.doc.employee, fieldname: property},
	// 	});
    //     console.log('purchase_incoiveEEEEEEEEEEEEEEEEEEEE')
    // },
});
