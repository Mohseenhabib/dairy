frappe.provide("erpnext.stock");

frappe.ui.form.on('Stock Entry', {

})

frappe.ui.form.on('Stock Entry Detail', {

    s_warehouse : function(frm, cdt, cdn){
        var d = locals[cdt][cdn];
        if(d.s_warehouse){
            var df = frappe.meta.get_docfield("Stock Entry Detail","fat", cur_frm.doc.name);
            df.read_only = 1;
            var df = frappe.meta.get_docfield("Stock Entry Detail","fat_per", cur_frm.doc.name);
            df.read_only = 1;
            var df = frappe.meta.get_docfield("Stock Entry Detail","snf_clr", cur_frm.doc.name);
            df.read_only = 1;
            var df = frappe.meta.get_docfield("Stock Entry Detail","snf_clr_per", cur_frm.doc.name);
            df.read_only = 1;

        }
    },

	fat: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.fat){
            frappe.call({
				method: "dairy.milk_entry.custom_stock_entry.get_item_weight",
				args: {"item_code": d.item_code },
				callback: function(r) {
					if (!r.exe){
					       var weight = r.message * d.transfer_qty
					       var per = ((d.fat / weight) * 100)
					       if(! d.fat_per){
					        frappe.model.set_value(cdt, cdn, "fat_per", per);
					       }

					}
				}
			});
        }
	},

   fat_per: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.fat_per){
            frappe.call({
				method: "dairy.milk_entry.custom_stock_entry.get_item_weight",
				args: {"item_code": d.item_code },
				callback: function(r) {
					if (!r.exe){
					       var weight = r.message * d.transfer_qty
					       var fat = ((d.fat_per / 100) * weight)
					       if(! d.fat){
					        frappe.model.set_value(cdt, cdn, "fat", fat);
					       }

					}
				}
			});
        }
	},

	snf_clr: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.snf_clr){
            frappe.call({
				method: "dairy.milk_entry.custom_stock_entry.get_item_weight",
				args: {"item_code": d.item_code },
				callback: function(r) {
					if (!r.exe){
					       var weight = r.message * d.transfer_qty
					       var per = ((d.snf_clr / weight) * 100)
					       if(! d.snf_clr_per){
					        frappe.model.set_value(cdt, cdn, "snf_clr_per", per);
					       }

					}
				}
			});
        }
	},

    snf_clr_per: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.snf_clr_per){
            frappe.call({
				method: "dairy.milk_entry.custom_stock_entry.get_item_weight",
				args: {"item_code": d.item_code },
				callback: function(r) {
					if (!r.exe){
					       var weight = r.message * d.transfer_qty
					       var snf_clr = ((d.snf_clr_per / 100) * weight)
					       if(! d.snf_clr){
					        frappe.model.set_value(cdt, cdn, "snf_clr", snf_clr);
					       }

					}
				}
			});
        }
	},

});