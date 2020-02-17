from __future__ import unicode_literals

from frappe import _

def get_data():
	return {
# 		'heatmap': False,
		'fieldname': 'milk_entry',
		# 'non_standard_fieldnames': {
		# 	'Raw Milk Sample': 'name',
			# 'Purchase Invoice': 'reference_name',
			# 'Material Request': 'reference_name',
			# 'Payment Entry': 'reference_name',
		# },
		# 'heatmap_message': _('This is based on transactions against this member. See timeline below for details'),
		'transactions': [
			{
				'label': _('Raw Milk Sample'),
				'items': ['Raw Milk Sample']
			},

			# {
			# 	'label': _('Purchase Invoice'),
			# 	'items': ['Purchase Invoice']
			# },
			{
				'label': _('Purchase Receipt'),
				'items': ['Purchase Receipt']
			},
 			
			# {
			# 	'label': _('Payment Entry'),
			# 	'items': ['Payment Entry']
			# }


		]
	}
