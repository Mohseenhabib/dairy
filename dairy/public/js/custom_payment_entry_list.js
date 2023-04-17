frappe.listview_settings['Payment Entry'] = {
    onload: function(list_view) {
		list_view.page.add_inner_button(__("Download CSV"), function() { 
        
        frappe.call({
            method: "dairy.milk_entry.custom_payment_entry.get_filter_data",
            args: {filter_list: list_view.filters}

            })
        })
	},
  
}