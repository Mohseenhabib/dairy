// Copyright (c) 2023, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Payment', {
    before_save: function(frm) {
        frappe.call({
            method: "get_data",
            doc: frm.doc,
            callback:function(r){
                frm.refresh_field("items")
            }

            })
       

    },
	after_save: function(frm) {
        frappe.call({
            method: "get_lines",
            doc: frm.doc,
            callback:function(r){
                frm.refresh_field("items")
            }

            })
       

    },
    refresh:function(frm){
		if(!frm.doc.__islocal){
        frm.add_custom_button(__("Download Csv"),function(){
           
        var url = frappe.urllib.get_full_url(
            '/api/method/dairy.dairy.doctype.bulk_payment.bulk_payment.get_download?'
            + 'name='+encodeURIComponent(frm.doc.name))
    
        $.ajax({
            url: url,
            type: 'GET',
            success: function(result) {
                if(jQuery.isEmptyObject(result)){
                    frappe.msgprint(__('No Records for these settings.'));
                }
                else{
                    window.location = url;
                }
            }
        });
    })
	}
    }
    


});

