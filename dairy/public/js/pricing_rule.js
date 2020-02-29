frappe.ui.form.on(
    'Pricing Rule', {
    
    //     frm.fields_dict.applicable_for.new_doc = function(){
    
    set_options_for_applicable_for: function(frm){
        if(frm.doc.selling == '1') {
        
            frm.set_df_property('applicable_for','options',[" ", "Customer", "Customer Group", "Territory", "Sales Partner", "Campaign", "Address"]);
            
        }
        if(frm.doc.buying== '1'){
            frm.set_df_property('applicable_for','options',[" ", "Supplier", "Supplier Type"]);

        }
        frm.refresh_field('applicable_for');
    },  

});