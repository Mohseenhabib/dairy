// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('RMRD', {
	 refresh: function(frm) {
	    if(!frm.doc.__islocal && frm.doc.docstatus == 0)
	    {
            frm.add_custom_button(__('Get Van Collection Data'), function () {
                 return frappe.call({
                    doc: frm.doc,
                    method: 'get_van_collection',
                    callback: function(r) {
                        frm.refresh();
                    }
                });
            }).addClass("btn-primary");
        }
	 }
});
