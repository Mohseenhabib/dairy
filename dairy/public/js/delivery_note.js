frappe.ui.form.on("Delivery Note", {
    setup: function(frm) {
		frm.add_fetch("route", "source_warehouse", "set_warehouse");
	},
	calculate_crate: function(frm){
	    cur_frm.cscript.calculate_crate()
	},
	validate: function(frm){
	    if (!frm.doc.__islocal)
	    {
	        cur_frm.cscript.calculate_crate()
	    }
	},

});

cur_frm.cscript.calculate_crate = function(){
    return cur_frm.call({
        method:"dairy.milk_entry.custom_delivery_note.calculate_crate",
        args: {
                doc_name: cur_frm.doc.name
              },
        callback: function(r)
            {
               cur_frm.reload_doc();
            }
    });
}
