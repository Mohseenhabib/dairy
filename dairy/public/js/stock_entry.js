frappe.provide("erpnext.stock");

frappe.ui.form.on('Stock Entry', {
	refresh:function(frm){
		if(frm.doc.total_diff_fat_in_kg>0){
			frm.set_df_property("add_fat_button","hidden",0)
		}
		if(frm.doc.total_diff_fat_in_kg<0){
			frm.set_df_property("remove_fat_button","hidden",0)

		}
		if(frm.doc.total_diff_snf_in_kg>0){
			frm.set_df_property("add_snf_button","hidden",0)

		}
		if(frm.doc.total_diff_snf_in_kg<0){
			frm.set_df_property("remove_snf_button","hidden",0)

		}
		frappe.db.get_value(
			"Item",
			frm.doc.item,
			"maintain_fat_snf_clr",
			(r) => {
				console.log(r.maintain_fat_snf_clr)
				if(r.maintain_fat_snf_clr==1){
					frm.set_df_property("fg_fat_snf_calculations","hidden",0)
					frm.set_df_property("rm_fat__snf_calculations","hidden",0)
					frm.set_df_property("difference_in_fat__snf","hidden",0)

				}

			})

	},
	add_fat_button:function(frm){
		frappe.call({
			method:"dairy.milk_entry.custom_stock_entry.get_add_fat",
			args:{
				"name":frm.doc.name
			},
			callback:function(r){
		console.log("$$$$$$$$$$$$$$$$$")
		let data = [];
		const me = this;		
		var child_table = [
			{
				fieldtype: 'Link',
				fieldname: "item_code",
				options: "Item",
				in_list_view: 1,
				read_only: 1,
				label: __('Item'),
			},
			{
				fieldtype: 'Data',
				fieldname: "item_name",
				read_only: 1,
				in_list_view: 1,
				label: __('Item Name'),
			},
			{
				fieldtype: 'Float',
				fieldname: "qty",
				in_list_view: 1,
				label: ('Qty'),
				onchange: () => {
					dialog.fields_dict.trans_items.df.data.some(d => {
						d.total_snf_in_kg=(d.qty*d.weight)*d.snf/100
						d.total_fat_in_kg=(d.qty*d.weight)*d.fat/100
						dialog.fields_dict.trans_items.grid.refresh();
					});
					
				  },
			},
			{
				fieldtype: 'Link',
				fieldname: "uom",
				options: "UOM",
				read_only: 1,
				in_list_view: 1,
				label: ('UOM') 
			},
			{
				fieldtype: 'Percent',
				fieldname: "fat",
				read_only: 1,
				in_list_view: 1,
				label: ('Fat % ') 
			},
			{
				fieldtype: 'Percent',
				fieldname: "snf",
				read_only: 1,
				in_list_view: 1,
				label: ('Snf % ') 
			},
			{
				fieldtype: 'Float',
				fieldname: "weight",
				read_only: 1,
				in_list_view: 1,
				label: ('Weight') 
			},
			{
				fieldtype: 'Float',
				fieldname: "total_fat_in_kg",
				read_only: 1,
				in_list_view: 1,
				label: ('Total Fat in KG') 
			},
			{
				fieldtype: 'Float',
				fieldname: "total_snf_in_kg",
				read_only: 1,
				in_list_view: 1,
				label: ('Total Snf in KG') 
			},
		]
		const dialog = new frappe.ui.Dialog({
			title: __("Item Update"),
			fields: [{
				fieldname: "trans_items",
				fieldtype: "Table",
				label: "Items",
				cannot_add_rows: 1,
				cannot_delete_rows : 1,
				in_place_edit: false,
				reqd: 1,
				read_only: 1,
				data: data,
				get_data: () => {
					return data;
				},
				fields: child_table
			}],
			primary_action: function (values) {
				console.log(values)
				var child_table = frm.fields_dict['items'].grid;

					// Create a new row object
					var new_row = child_table.add_new_row();
			
					// Set the values for the new row
					frappe.model.set_value(new_row.doctype, new_row.name, 's_warehouse', frm.doc.from_warehouse);
					frappe.model.set_value(new_row.doctype, new_row.name, 'item_code', d.item_code);
					frappe.model.set_value(new_row.doctype, new_row.name, 'qty', d.qty);
					frappe.model.set_value(new_row.doctype, new_row.name, 'snf_per', d.snf);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat_per', d.fat);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat', d.total_fat_in_kg);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat', d.total_fat_in_kg);
					child_table.refresh();
				dialog.hide();
				
			},
			primary_action_label: __('Submit'),

		});
		r.message.forEach(d => {
			dialog.fields_dict.trans_items.df.data.push({
				"item_code": d.item_code,
				"item_name": d.item_name,
				"qty":d.qty,
				"uom":d.uom,
				"fat":d.fat,
				"snf":d.snf,
				"weight":d.weight,
				"total_fat_in_kg":d.total_fat_in_kg,
				"total_snf_in_kg":d.total_snf_in_kg
				
				});
	})
		//dialog.fields_dict.trans_items.df.data = r.message;
		data = dialog.fields_dict.trans_items.df.data;
		dialog.fields_dict.trans_items.grid.refresh();
		
	
		dialog.show();
	}
	})
	},
	add_snf_button:function(frm){
		frappe.call({
			method:"dairy.milk_entry.custom_stock_entry.get_add_snf",
			args:{
				"name":frm.doc.name
			},
			callback:function(r){
		console.log("$$$$$$$$$$$$$$$$$")
		let data = [];
		const me = this;		
		var child_table = [
			{
				fieldtype: 'Link',
				fieldname: "item_code",
				options: "Item",
				in_list_view: 1,
				read_only: 1,
				label: __('Item'),
			},
			{
				fieldtype: 'Data',
				fieldname: "item_name",
				read_only: 1,
				in_list_view: 1,
				label: __('Item Name'),
			},
			{
				fieldtype: 'Float',
				fieldname: "qty",
				in_list_view: 1,
				label: ('Qty'),
				onchange: () => {
					dialog.fields_dict.trans_items.df.data.some(d => {
						d.total_snf_in_kg=(d.qty*d.weight)*d.snf/100
						d.total_fat_in_kg=(d.qty*d.weight)*d.fat/100
						dialog.fields_dict.trans_items.grid.refresh();
					});
					
				  },
			},
			{
				fieldtype: 'Link',
				fieldname: "uom",
				options: "UOM",
				read_only: 1,
				in_list_view: 1,
				label: ('UOM') 
			},
			{
				fieldtype: 'Percent',
				fieldname: "fat",
				read_only: 1,
				in_list_view: 1,
				label: ('Fat % ') 
			},
			{
				fieldtype: 'Percent',
				fieldname: "snf",
				read_only: 1,
				in_list_view: 1,
				label: ('Snf % ') 
			},
			{
				fieldtype: 'Float',
				fieldname: "weight",
				read_only: 1,
				in_list_view: 1,
				label: ('Weight') 
			},
			{
				fieldtype: 'Float',
				fieldname: "total_fat_in_kg",
				read_only: 1,
				in_list_view: 1,
				label: ('Total Fat in KG') 
			},
			{
				fieldtype: 'Float',
				fieldname: "total_snf_in_kg",
				read_only: 1,
				in_list_view: 1,
				label: ('Total Snf in KG') 
			},
		]
		const dialog = new frappe.ui.Dialog({
			title: __("Item Update"),
			fields: [{
				fieldname: "trans_items",
				fieldtype: "Table",
				label: "Items",
				cannot_add_rows: 1,
				cannot_delete_rows : 1,
				in_place_edit: false,
				reqd: 1,
				read_only: 1,
				data: data,
				get_data: () => {
					return data;
				},
				fields: child_table
			}],
			primary_action: function (values) {
				console.log(values)
				var child_table = frm.fields_dict['items'].grid;

					// Create a new row object
					var new_row = child_table.add_new_row();
			
					// Set the values for the new row
					frappe.model.set_value(new_row.doctype, new_row.name, 's_warehouse', frm.doc.from_warehouse);
					frappe.model.set_value(new_row.doctype, new_row.name, 'item_code', d.item_code);
					frappe.model.set_value(new_row.doctype, new_row.name, 'qty', d.qty);
					frappe.model.set_value(new_row.doctype, new_row.name, 'snf_per', d.snf);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat_per', d.fat);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat', d.total_fat_in_kg);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat', d.total_fat_in_kg);
					child_table.refresh();
				dialog.hide();
				
			},
			primary_action_label: __('Submit'),

		});
		r.message.forEach(d => {
			dialog.fields_dict.trans_items.df.data.push({
				"item_code": d.item_code,
				"item_name": d.item_name,
				"qty":d.qty,
				"uom":d.uom,
				"fat":d.fat,
				"snf":d.snf,
				"weight":d.weight,
				"total_fat_in_kg":d.total_fat_in_kg,
				"total_snf_in_kg":d.total_snf_in_kg
				
				});
	})
		//dialog.fields_dict.trans_items.df.data = r.message;
		data = dialog.fields_dict.trans_items.df.data;
		dialog.fields_dict.trans_items.grid.refresh();
		
	
		dialog.show();
	}
	})
	},
	remove_fat_button:function(frm){
		frappe.call({
			method:"dairy.milk_entry.custom_stock_entry.get_remove_fat",
			args:{
				"name":frm.doc.name
			},
			callback:function(r){
		console.log("$$$$$$$$$$$$$$$$$")
		let data = [];
		const me = this;		
		var child_table = [
			{
				fieldtype: 'Link',
				fieldname: "item_code",
				options: "Item",
				in_list_view: 1,
				read_only: 1,
				label: __('Item'),
			},
			{
				fieldtype: 'Data',
				fieldname: "item_name",
				read_only: 1,
				in_list_view: 1,
				label: __('Item Name'),
			},
			{
				fieldtype: 'Float',
				fieldname: "qty",
				in_list_view: 1,
				label: ('Qty'),
				onchange: () => {
					dialog.fields_dict.trans_items.df.data.some(d => {
						d.total_snf_in_kg=(d.qty*d.weight)*d.snf/100
						d.total_fat_in_kg=(d.qty*d.weight)*d.fat/100
						dialog.fields_dict.trans_items.grid.refresh();
					});
					
				  },
			},
			{
				fieldtype: 'Link',
				fieldname: "uom",
				options: "UOM",
				read_only: 1,
				in_list_view: 1,
				label: ('UOM') 
			},
			{
				fieldtype: 'Percent',
				fieldname: "fat",
				read_only: 1,
				in_list_view: 1,
				label: ('Fat % ') 
			},
			{
				fieldtype: 'Percent',
				fieldname: "snf",
				read_only: 1,
				in_list_view: 1,
				label: ('Snf % ') 
			},
			{
				fieldtype: 'Float',
				fieldname: "weight",
				read_only: 1,
				in_list_view: 1,
				label: ('Weight') 
			},
			{
				fieldtype: 'Float',
				fieldname: "total_fat_in_kg",
				read_only: 1,
				in_list_view: 1,
				label: ('Total Fat in KG') 
			},
			{
				fieldtype: 'Float',
				fieldname: "total_snf_in_kg",
				read_only: 1,
				in_list_view: 1,
				label: ('Total Snf in KG') 
			},
		]
		const dialog = new frappe.ui.Dialog({
			title: __("Item Update"),
			fields: [{
				fieldname: "trans_items",
				fieldtype: "Table",
				label: "Items",
				cannot_add_rows: 1,
				cannot_delete_rows : 1,
				in_place_edit: false,
				reqd: 1,
				read_only: 1,
				data: data,
				get_data: () => {
					return data;
				},
				fields: child_table
			}],
			primary_action: function (values) {
				console.log(values)
				var child_table = frm.fields_dict['items'].grid;

					// Create a new row object
					var new_row = child_table.add_new_row();
			
					// Set the values for the new row
					frappe.model.set_value(new_row.doctype, new_row.name, 's_warehouse', frm.doc.from_warehouse);
					frappe.model.set_value(new_row.doctype, new_row.name, 'item_code', d.item_code);
					frappe.model.set_value(new_row.doctype, new_row.name, 'qty', d.qty);
					frappe.model.set_value(new_row.doctype, new_row.name, 'snf_per', d.snf);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat_per', d.fat);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat', d.total_fat_in_kg);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat', d.total_fat_in_kg);
					child_table.refresh();
				dialog.hide();
				
			},
			primary_action_label: __('Submit'),

		});
		r.message.forEach(d => {
			dialog.fields_dict.trans_items.df.data.push({
				"item_code": d.item_code,
				"item_name": d.item_name,
				"qty":d.qty,
				"uom":d.uom,
				"fat":d.fat,
				"snf":d.snf,
				"weight":d.weight,
				"total_fat_in_kg":d.total_fat_in_kg,
				"total_snf_in_kg":d.total_snf_in_kg
				
				});
	})
		//dialog.fields_dict.trans_items.df.data = r.message;
		data = dialog.fields_dict.trans_items.df.data;
		dialog.fields_dict.trans_items.grid.refresh();
		
	
		dialog.show();
	}
	})
	},
	remove_snf_button:function(frm){
		frappe.call({
			method:"dairy.milk_entry.custom_stock_entry.get_remove_snf",
			args:{
				"name":frm.doc.name
			},
			callback:function(r){
		console.log("$$$$$$$$$$$$$$$$$")
		let data = [];
		const me = this;		
		var child_table = [
			{
				fieldtype: 'Link',
				fieldname: "item_code",
				options: "Item",
				in_list_view: 1,
				read_only: 1,
				label: __('Item'),
			},
			{
				fieldtype: 'Data',
				fieldname: "item_name",
				read_only: 1,
				in_list_view: 1,
				label: __('Item Name'),
			},
			{
				fieldtype: 'Float',
				fieldname: "qty",
				in_list_view: 1,
				label: ('Qty'),
				onchange: () => {
					dialog.fields_dict.trans_items.df.data.some(d => {
						d.total_snf_in_kg=(d.qty*d.weight)*d.snf/100
						d.total_fat_in_kg=(d.qty*d.weight)*d.fat/100
						dialog.fields_dict.trans_items.grid.refresh();
					});
					
				  },
			},
			{
				fieldtype: 'Link',
				fieldname: "uom",
				options: "UOM",
				read_only: 1,
				in_list_view: 1,
				label: ('UOM') 
			},
			{
				fieldtype: 'Percent',
				fieldname: "fat",
				read_only: 1,
				in_list_view: 1,
				label: ('Fat % ') 
			},
			{
				fieldtype: 'Percent',
				fieldname: "snf",
				read_only: 1,
				in_list_view: 1,
				label: ('Snf % ') 
			},
			{
				fieldtype: 'Float',
				fieldname: "weight",
				read_only: 1,
				in_list_view: 1,
				label: ('Weight') 
			},
			{
				fieldtype: 'Float',
				fieldname: "total_fat_in_kg",
				read_only: 1,
				in_list_view: 1,
				label: ('Total Fat in KG') 
			},
			{
				fieldtype: 'Float',
				fieldname: "total_snf_in_kg",
				read_only: 1,
				in_list_view: 1,
				label: ('Total Snf in KG') 
			},
		]
		const dialog = new frappe.ui.Dialog({
			title: __("Item Update"),
			fields: [{
				fieldname: "trans_items",
				fieldtype: "Table",
				label: "Items",
				cannot_add_rows: 1,
				cannot_delete_rows : 1,
				in_place_edit: false,
				reqd: 1,
				read_only: 1,
				data: data,
				get_data: () => {
					return data;
				},
				fields: child_table
			}],
			primary_action: function (values) {
				console.log(values)
				values.trans_items.forEach(d => {
				if (d.qty>0){
					var child_table = frm.fields_dict['items'].grid;

					// Create a new row object
					var new_row = child_table.add_new_row();
			
					// Set the values for the new row
					frappe.model.set_value(new_row.doctype, new_row.name, 's_warehouse', frm.doc.from_warehouse);
					frappe.model.set_value(new_row.doctype, new_row.name, 'item_code', d.item_code);
					frappe.model.set_value(new_row.doctype, new_row.name, 'qty', d.qty);
					frappe.model.set_value(new_row.doctype, new_row.name, 'snf_per', d.snf);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat_per', d.fat);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat', d.total_fat_in_kg);
					frappe.model.set_value(new_row.doctype, new_row.name, 'fat', d.total_fat_in_kg);
					child_table.refresh();
				
				}
				})
				dialog.hide();
				
			},
			primary_action_label: __('Submit'),

		});
		r.message.forEach(d => {
			dialog.fields_dict.trans_items.df.data.push({
				"item_code": d.item_code,
				"item_name": d.item_name,
				"qty":d.qty,
				"uom":d.uom,
				"fat":d.fat,
				"snf":d.snf,
				"weight":d.weight,
				"total_fat_in_kg":d.total_fat_in_kg,
				"total_snf_in_kg":d.total_snf_in_kg
				
				});
	})
		//dialog.fields_dict.trans_items.df.data = r.message;
		data = dialog.fields_dict.trans_items.df.data;
		dialog.fields_dict.trans_items.grid.refresh();
		
	
		dialog.show();
	}
	})
	}


})

frappe.ui.form.on('Stock Entry Detail', {

    s_warehouse : function(frm, cdt, cdn){
        var d = locals[cdt][cdn];
        if(d.s_warehouse){
            var df = frappe.meta.get_docfield("Stock Entry Detail","fat", cur_frm.doc.name);
            df.read_only = 1;
            var df = frappe.meta.get_docfield("Stock Entry Detail","fat_per", cur_frm.doc.name);
            df.read_only = 1;
            var df = frappe.meta.get_docfield("Stock Entry Detail","snf_clr", cur_frm.doc.name);
            df.read_only = 1;
            var df = frappe.meta.get_docfield("Stock Entry Detail","snf_clr_per", cur_frm.doc.name);
            df.read_only = 1;

        }else{
            var df = frappe.meta.get_docfield("Stock Entry Detail","fat", cur_frm.doc.name);
            df.read_only = 0;
            var df = frappe.meta.get_docfield("Stock Entry Detail","fat_per", cur_frm.doc.name);
            df.read_only = 0;
            var df = frappe.meta.get_docfield("Stock Entry Detail","snf_clr", cur_frm.doc.name);
            df.read_only = 0;
            var df = frappe.meta.get_docfield("Stock Entry Detail","snf_clr_per", cur_frm.doc.name);
            df.read_only = 0;
        }
    },

	fat: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.fat){
            frappe.call({
				method: "dairy.milk_entry.custom_stock_entry.get_item_weight",
				args: {"item_code": d.item_code },
				callback: function(r) {
					if (!r.exe){
					       var weight = r.message * d.transfer_qty
					       var per = ((d.fat / weight) * 100)
					        frappe.model.set_value(cdt, cdn, "fat_per", per);
					}
				}
			});
        }
	},

   fat_per: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.fat_per){
            frappe.call({
				method: "dairy.milk_entry.custom_stock_entry.get_item_weight",
				args: {"item_code": d.item_code },
				callback: function(r) {
					if (!r.exe){
					       var weight = r.message * d.transfer_qty
					       var fat = ((d.fat_per / 100) * weight)
					       if(! d.fat){
					        frappe.model.set_value(cdt, cdn, "fat", fat);
					       }
					       frappe.model.set_value(cdt, cdn, "fat", fat);

					}
				}
			});
        }
	},

	snf_clr: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.snf_clr){
            frappe.call({
				method: "dairy.milk_entry.custom_stock_entry.get_item_weight",
				args: {"item_code": d.item_code },
				callback: function(r) {
					if (!r.exe){
					       var weight = r.message * d.transfer_qty
					       var per = ((d.snf_clr / weight) * 100)
					       if(! d.snf_clr_per){
					        frappe.model.set_value(cdt, cdn, "snf_clr_per", per);
					       }
					       frappe.model.set_value(cdt, cdn, "snf_clr_per", per);

					}
				}
			});
        }
	},

    snf_clr_per: function(frm, cdt, cdn) {
	    var d = locals[cdt][cdn];
        if(d.snf_clr_per){
            frappe.call({
				method: "dairy.milk_entry.custom_stock_entry.get_item_weight",
				args: {"item_code": d.item_code },
				callback: function(r) {
					if (!r.exe){
					       var weight = r.message * d.transfer_qty
					       var snf_clr = ((d.snf_clr_per / 100) * weight)
					       if(! d.snf_clr){
					        frappe.model.set_value(cdt, cdn, "snf_clr", snf_clr);
					       }
                            frappe.model.set_value(cdt, cdn, "snf_clr", snf_clr);
					}
				}
			});
        }
	},

});