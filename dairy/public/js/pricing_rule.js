frappe.ui.form.on('Pricing Rule', {
    
    //     frm.fields_dict.applicable_for.new_doc = function(){
    
    set_options_for_applicable_for: function(frm){
        

            frm.set_df_property('applicable_for','options',[" ", "Customer", "Customer Group", "Territory", "Sales Partner", "Campaign", "Address"]);
            frm.refresh_field('applicable_for');
        
    }  

});