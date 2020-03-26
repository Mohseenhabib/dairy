// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Van Collection Items', {
	 after_save: function(frm) {
	     cur_frm.cscript.calculate_milk_cans()
	 },
	 cow_milk_collected: function(frm) {
	     cur_frm.cscript.calculate_milk_cans()
	 },
	 buffalow_milk_collected: function(frm) {
	     cur_frm.cscript.calculate_milk_cans()
	 },
	 mix_milk_collected: function(frm) {
	     cur_frm.cscript.calculate_milk_cans()
	 },
//	 refresh: function(frm) {
//	     cur_frm.cscript.calculate_milk_cans()
//	 },
});

cur_frm.cscript.calculate_milk_cans= function()
 {
      return frappe.call({
            doc: cur_frm.doc,
            method: 'calculate_milk_cans',
            callback: function(r) {
               cur_frm.refresh_fields();
            }
      });
 };