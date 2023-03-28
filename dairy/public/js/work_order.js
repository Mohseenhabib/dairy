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
    if (frm.doc.status=="Not Started"){
        frm.add_custom_button(__("Create Manufacture Entry"),function(){
            var today = new Date();
            var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
            var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();

            frappe.model.with_doctype("Stock Entry", function() {
                let se = frappe.model.get_new_doc("Stock Entry");
                se.stock_entry_type="Manufacture"
                se.posting_date=date
                se.posting_time=time
                se.work_order=frm.doc.name
    
                frappe.set_route("Form", "Stock Entry", se.name);
            });


        })
    
    }
}


})

