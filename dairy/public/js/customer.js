// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", {
	refresh: function(frm) {
		if(frm.doc.__islocal) {
			const last_doc = dairy.vehicle_dynamic_link.get_last_doc(frm);
				frm.set_value('links', '');
				frm.add_child('links', {
					link_doctype: last_doc.doctype,
					link_name: last_doc.docname
				});
		}
		frm.set_query('link_doctype', "links", function() {
			return {
				query: "dairy.vehicle_dynamic_link.filter_dynamic_link_doctypes",
				filters: {
					fieldtype: "HTML",
					fieldname: "customer_html",
				}
			}
		});
		frm.refresh_field("links");

		if (frm.doc.links) {
			for (let i in frm.doc.links) {
				let link = frm.doc.links[i];
				frm.add_custom_button(__("{0}: {1}", [__(link.link_doctype), __(link.link_name)]), function() {
					frappe.set_route("Form", link.link_doctype, link.link_name);
				}, __("Links"));
			}
		}
	},
	validate: function(frm) {
		// clear linked customer / supplier / sales partner on saving...
		if(frm.doc.links) {
			frm.doc.links.forEach(function(d) {
				frappe.model.remove_from_locals(d.link_doctype, d.link_name);
			});
		}
	},
	after_save: function(frm) {
		frappe.run_serially([
			() => frappe.timeout(1),
			() => {
				const last_doc = dairy.vehicle_dynamic_link.get_last_doc(frm);
				if (last_doc.doctype =='Route Master')
				{
					for (let i in frm.doc.links) {
						let link = frm.doc.links[i];
						if (last_doc.doctype == link.link_doctype && last_doc.docname == link.link_name) {
							frappe.set_route('Form', last_doc.doctype, last_doc.docname);
						}
					}
				}
			}
		]);
	}
});
