// Copyright (c) 2019, Dexciss Technology by Sid and contributors
// For license information, please see license.txt

frappe.ui.form.on('Dairy Settings', {
	
	
	validate: function(frm) {
		if(frm.doc.max_allowed > frm.doc.can_volume)
		{
			frappe.throw(__(" 'Max Allowed Capacity' should be equal to or less than 'Can Volume' "));
		}
	 
	 
	},
	
	
});
