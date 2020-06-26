// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('RMRD Lines', {
	after_save: function(frm) {
//	    if(frm.doc.__islocal)
//	    {
	         cur_frm.cscript.calculate_total_cans_wt()
//	    }
	 },
	 g_cow_milk: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 g_buf_milk: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 g_mix_milk: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 g_cow_milk_can: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 g_buf_milk_can: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 g_mix_milk_can: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },

	 s_cow_milk: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 s_buf_milk: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 s_mix_milk: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 s_cow_milk_can: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 s_buf_milk_can: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 s_mix_milk_can: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },

	 c_cow_milk: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 c_buf_milk: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 c_mix_milk: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 c_cow_milk_can: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 c_buf_milk_can: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
	 c_mix_milk_can: function(frm) {
	     cur_frm.cscript.calculate_total_cans_wt()
	 },
});

cur_frm.cscript.calculate_total_cans_wt = function(){
    return frappe.call({
            doc: cur_frm.doc,
            method: 'calculate_total_cans_wt',
            callback: function(r) {
               cur_frm.refresh_fields();
            }
    });
}