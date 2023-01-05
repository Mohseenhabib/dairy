// Copyright (c) 2019, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Milk Rate', {
    setup:function(frm){
        frm.set_query('dcs', function(doc) {
            return {
                filters: {
                    "is_dcs":1,
                    "is_group":0
                }
            };
        });
           
    },
	milk_type: function(frm) {
	    return frm.call('get_snf_lines').then(() => {
            frm.refresh_field('milk_rate_chart');
        });
	},
	onload(frm) {
        if(frm.doc.__islocal) {
            return frm.call('get_snf_lines').then(() => {
                frm.refresh_field('milk_rate_chart');
            });
        }
    },
    validate: function(frm) {
        if(!frm.doc.milk_rate_chart) {
            frappe.throw(__('Cant Submit without Rate Chart.'));
        }
    },
    before_submit : function (frm) {
        for(let i in frm.doc.milk_rate_chart){
            if (frm.doc.milk_rate_chart[i].rate <= 0){
                frappe.throw(__('Rate must be greater then zero on row '+(parseInt(i,10)+1)));
            }
        }
    },
});

