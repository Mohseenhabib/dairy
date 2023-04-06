frappe.ui.form.on("Work Order", {

    production_item:function(frm){
        frappe.call({
            method : "dairy.milk_entry.custom_work_order.get_required_fat_snf",
            args:{
                production_item: frm.doc.production_item,
                quantity : frm.doc.qty
            },
            callback:function(response){
                console.log(response)
                frm.set_value('required_fat',response.message[0]);
                frm.set_value('required_snf_',response.message[1]);
                frm.set_value('required_fat_in_kg',response.message[2]);
                frm.set_value('required_snt_in_kg',response.message[3]);
                frm.refresh_field('required_fat')
                frm.refresh_field('required_snf_')
                frm.refresh_field('required_fat_in_kg')
                frm.refresh_field('required_snt_in_kg')
            }
        })
    },
    qty:function(frm){
        frappe.call({
            method : "dairy.milk_entry.custom_work_order.get_required_fat_snf",
            args:{
                production_item: frm.doc.production_item,
                quantity : frm.doc.qty
            },
            callback:function(response){
                console.log(response)
                frm.set_value('required_fat',response.message[0]);
                frm.set_value('required_snf_',response.message[1]);
                frm.set_value('required_fat_in_kg',response.message[2]);
                frm.set_value('required_snt_in_kg',response.message[3]);
                frm.refresh_field('required_fat')
                frm.refresh_field('required_snf_')
                frm.refresh_field('required_fat_in_kg')
                frm.refresh_field('required_snt_in_kg')
            }
        })
    },
    refresh:function(frm){
    frappe.db.get_value(
        "Item",
        frm.doc.production_item,
        "maintain_fat_snf_clr",
        (r) => {
            console.log(r.maintain_fat_snf_clr)
            if(r.maintain_fat_snf_clr==0){
                frm.set_df_property("required_fat","hidden",1)
                frm.set_df_property("required_snf_","hidden",1)
                frm.set_df_property("required_fat_in_kg","hidden",1)
                frm.set_df_property("required_snt_in_kg","hidden",1)
            }

        })
        if(frm.doc.production_item && frm.doc.qty && frm.doc.required_fat_in_kg==0 && frm.doc.required_snt_in_kg==0){
            frappe.call({
                method : "dairy.milk_entry.custom_work_order.get_required_fat_snf",
                args:{
                    production_item: frm.doc.production_item,
                    quantity : frm.doc.qty
                },
                callback:function(response){
                    console.log(response)
                    frm.set_value('required_fat',response.message[0]);
                    frm.set_value('required_snf_',response.message[1]);
                    frm.set_value('required_fat_in_kg',response.message[2]);
                    frm.set_value('required_snt_in_kg',response.message[3]);
                    frm.refresh_field('required_fat')
                    frm.refresh_field('required_snf_')
                    frm.refresh_field('required_fat_in_kg')
                    frm.refresh_field('required_snt_in_kg')
                }
            })
        }
    if (!frm.doc.__islocal){
        frm.add_custom_button(__("Calculate Snf & Fat"),function(){
           
            frappe.call({
                method : "dairy.milk_entry.custom_work_order.get_data",
                args:{
                    name: frm.doc.name
                },
                callback:function(response){
                   
                }
            })
        })
    
    }
}


})

