frappe.provide("erpnext.public");
frappe.provide("erpnext.controllers");
erpnext.salary_slip.prototype.leave_without_pay = function(){
    var me = this;
    console.log(":::::CUSTOM:::::me:::::",me);
    }

frappe.ui.form.on("Salary Slip", {

	leave_without_pay: function(frm){
		if (frm.doc.employee && frm.doc.from && frm.doc.to) {
			return frappe.call({
				method: 'process_salary_based_on_leave',
				doc: frm.doc,
				args: {"lwp": frm.doc.leave_without_pay},
				callback: function(r, rt) {
					frm.refresh();
				}
			});
		}
	},
});