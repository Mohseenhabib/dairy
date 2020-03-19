frappe.ui.form.on('Warehouse', {
	onload: function(frm){
        frm.set_query('route', function(doc) {
            return {
                filters: {
                    "company":doc.company,
//                    "dest_warehouse":["!=",doc.name],
                    "route_type":"Buying"
                }
            };
        });
    },
})