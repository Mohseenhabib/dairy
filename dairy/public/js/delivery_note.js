frappe.ui.form.on("Delivery Note", {
    setup: function(frm) {
		frm.add_fetch("route", "source_warehouse", "set_warehouse");
	},
	calculate_crate: function(frm){
	    cur_frm.cscript.calculate_crate()
	},
	refresh: function(frm){
        if(!frm.doc.__islocal && frm.doc.docstatus == 0)
        {
            frm.add_custom_button(__('Calculate Crate'), function() {
				cur_frm.cscript.calculate_crate()
			}).addClass("btn-primary");
        }
	},
	before_submit: function(frm){
	    cur_frm.cscript.calculate_crate()
	},
	onload: function(frm){
	    frm.trigger('set_property');
	},
	set_property: function(frm) {
         if(!frm.doc.__islocal && frm.doc.docstatus == 0)
         {
            frm.set_df_property("calculate_crate", "hidden",0);
         }
         else
         {
            frm.set_df_property("calculate_crate", "hidden",1);
         }
    },
    docstatus:function(frm)
    {
        frm.trigger('set_property');
    }
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
