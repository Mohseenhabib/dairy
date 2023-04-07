frappe.provide("erpnext.stock");

frappe.ui.form.on('Purchase Receipt', {

})

frappe.ui.form.on('Purchase Receipt Item', {

	fat: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.fat){
           var weight = d.total_weight;
           var per = ((d.fat / weight) * 100);
           frappe.model.set_value(cdt, cdn, "fat_per_", per);
        }
	},

   fat_per_: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.fat_per_){
           var weight = d.total_weight;
           var fat = ((d.fat_per_ / 100) * weight);
           frappe.model.set_value(cdt, cdn, "fat", fat);
        }
	},

	clr: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.clr){
           var weight = d.total_weight;
           var per = ((d.clr / weight) * 100);
           frappe.model.set_value(cdt, cdn, "snf_clr_per", per);
        }
	},

   snf_clr_per: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.snf_clr_per){
           var weight = d.total_weight;
           var snf_clr = ((d.snf_clr_per / 100) * weight);
           frappe.model.set_value(cdt, cdn, "clr", snf_clr);
        }
	},

   clr_per: function(frm, cdt, cdn) {
      var d = locals[cdt][cdn];
      if(d.clr_per){
         var weight = d.total_weight;
         var snf = ((d.clr_per / 100) * weight);
         frappe.model.set_value(cdt, cdn, "snf", snf);
      }
  },

   snf: function(frm, cdt, cdn) {
      var d = locals[cdt][cdn];
      if(d.snf){
         var weight = d.total_weight;
         var per = ((d.snf / weight) * 100);
         frappe.model.set_value(cdt, cdn, "clr_per", per);
      }
   },


   qty : function(frm, cdt, cdn){
      var d = locals[cdt][cdn];
      if(d.qty){
         frappe.db.get_value("Item", d.item_code, ["weight_per_unit"]).then((r) => {
               console.log('rrrrrrrrrrrrrrrrrrrrr',r.message,d.qty)
         
         if(d.clr_per){
            var weight = d.total_weight;
            var snf = ((d.clr_per / 100) * weight);
            console.log('snfFFFFFFFFFFF',weight,d.clr_per)
            frappe.model.set_value(cdt, cdn, "snf", snf);
         }
         if(d.snf_clr_per){
            var weight = d.total_weight;
            console.log('snf_clrRRRRRRRRRRRRRRRRRRR',weight,d.snf_clr_per)
            var snf_clr = ((d.snf_clr_per / 100) * weight);
            frappe.model.set_value(cdt, cdn, "clr", snf_clr);
         }
         if(d.fat_per_){
            var weight = d.total_weight;
            var fat = ((d.fat_per_ / 100) * weight);
            console.log('fatTTTTTTTTTTTTTTTTTTTTTttt',weight,d.fat_per_)
            frappe.model.set_value(cdt, cdn, "fat", fat);
         }

        })
      }
   },


  

});