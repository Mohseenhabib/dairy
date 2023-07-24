# Copyright (c) 2013, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from itertools import zip_longest


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("Name"),
            "fieldname": "name",
            "fieldtype": "Data",
            "width": 120
        },
		{
            "label": _("DCS"),
            "options": "Warehouse",
            "fieldname": "dcs_id",
            "fieldtype": "Link",
            "width": 160
        },
#         {
#             "label": _("Cow Milk Volume"),
#             "fieldname": "cow_milk_vol",
#             "fieldtype": "Float",
#             "width": 100
#         },
#         {
#             "label": _("Buffalow Milk Volume"),
#             "fieldname": "buf_milk_vol",
#             "fieldtype": "Float",
#             "width": 100            
#         },
# 		{
#             "label": _("Mix Milk Volume"),
#             "fieldname": "mix_milk_vol",
#             "fieldtype": "Float",
#             "width": 100
#         },
		
		
		{
            "label": _("Cow Milk Cans"),
            "fieldname": "cow_milk_cans",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Buffalo Milk Cans"),
            "fieldname": "buf_milk_cans",
            "fieldtype": "Float",
            "width": 100
        },
		{
            "label": _("Mix Milk Cans"),
            "fieldname": "mix_milk_cans",
            "fieldtype": "Float",
            "width": 100
        },
		
		
		{
            "label": _("Cow Sample Number"),
            "fieldname": "cow_milk_sam",
            "fieldtype": "Link",
            "options" : "Raw Milk Sample",
            "width": 100
        },
        {
            "label": _("Buffalo Sample Number"),
            "fieldname": "buf_milk_sam",
            "fieldtype": "Link",
            "options" : "Raw Milk Sample",
            "width": 100
        },
		{
            "label": _("Mix Sample Number"),
            "fieldname": "mix_milk_sam",
            "fieldtype": "Link",
            "options" : "Raw Milk Sample",
            "width": 100
        },
		
		
#         {
#             "label": _("Gate Pass"),
#             "fieldname": "gate_pass",
#             "fieldtype": "Link",
#             ""
#             "width": 80
#         },
        {
            "label": _("Time"),
            "fieldname": "time",
            "fieldtype": "Time",
            "width": 80
        },
		{
            "label": _("Van Collection"),
            "fieldname": "van_col",
            "fieldtype": "Link",
            "options":"Van Collection",
            "width": 120
        }
        
    ]
    return columns

def get_data(filters):
    # print("======")
    conditions = get_conditions(filters)

    vci = frappe.get_all('Van Collection Items',{'van_collection':filters.get('parent')},['name'])
    
    query = """ select vci.name,vci.dcs,vci.cow_milk_vol,vci.buf_milk_vol,vci.mix_milk_vol,vci.cow_milk_cans,vci.buf_milk_cans,
    			        vci.mix_milk_cans,vci.time,vci.van_collection ,mr.sample_lines,(case
                        when sl.milk_type = 'Cow' then 'cow_milk_sam'
                        when sl.milk_type = 'Buffalo' then 'buf_milk_sam'
                        when sl.milk_type = 'Mix' then 'mix_milk_sam' 
                        else "" end) as sm
                        from `tabVan Collection Items` as vci
                        join `tabMulti Row Milk Sample` as mr on mr.parent = vci.name
                        join `tabSample lines` as sl on mr.sample_lines = sl.name 
                        {conditions}  group by sl.milk_type,mr.sample_lines""".format(conditions = conditions)

   
    print('conditions=============',conditions)
    # print('query and conditions===========================',query+conditions)
    q_data = frappe.db.sql(query,as_dict=1)
    print("====query",q_data)
    data = []
    sams = []
    samlines =  {
        'cow_milk_sam':[],
        'buf_milk_sam':[],
        'mix_milk_sam':[]
    }
    for q in q_data:
        
        samlines.update({
            "name": q.get('name'),
            "dcs_id": q.get('dcs'),
            "cow_milk_vol": q.get('cow_milk_vol'),
            "buf_milk_vol": q.get('buf_milk_vol'),
            "mix_milk_vol": q.get('mix_milk_vol'),
            "cow_milk_cans": q.get('cow_milk_cans'),
            "buf_milk_cans": q.get('buf_milk_cans'),
            "mix_milk_cans": q.get('mix_milk_cans'),
            "time":q.get('time'),
            "van_col":q.get('van_collection')
        })
        
        if q.get('sm')== 'cow_milk_sam':
            if q.get('sm') in samlines:
                temp_list = samlines[q.get('sm')]
                temp_list.append(q.get('sample_lines'))
                samlines.update({
                    q.get('sm'): temp_list
                })
        if q.get('sm')== 'buf_milk_sam':
            if q.get('sm') in samlines:
                temp_list = samlines[q.get('sm')]
                temp_list.append(q.get('sample_lines'))
                samlines.update({
                    q.get('sm'): temp_list
                })
        if q.get('sm')== 'mix_milk_sam':
           if q.get('sm') in samlines:
                temp_list = samlines[q.get('sm')]
                temp_list.append(q.get('sample_lines'))
                samlines.update({
                    q.get('sm'): temp_list
                })
        if samlines not in sams:
            sams.append(samlines)
        
        
    print('samsssssssssssssssssssssssssssssss',sams)
    if sams:
        for r in sams:
            
            cms = []
            bms = []
            mms = []
            if r.get('cow_milk_sam'):
                cms = r.get('cow_milk_sam')
            if r.get('buf_milk_sam'):
                bms = r.get('buf_milk_sam')
            if r.get('mix_milk_sam'):
                mms = r.get('mix_milk_sam')

            max_length = max(len(cms), len(bms), len(mms))

            d = [[cms[i] if i < len(cms) else "", bms[i] if i < len(bms) else "", mms[i] if i < len(mms) else ""] for i in range(max_length)]

            

            if d:
                for k in d:
                    fd = {}
                    # print('ssssssssssssssssssssssss',s,s+1,s+2)
                    fd.update({
                            "name": q.get('name'),
                            "dcs_id": q.get('dcs'),
                            "cow_milk_vol": q.get('cow_milk_vol'),
                            "buf_milk_vol": q.get('buf_milk_vol'),
                            "mix_milk_vol": q.get('mix_milk_vol'),
                            "cow_milk_cans": q.get('cow_milk_cans'),
                            "buf_milk_cans": q.get('buf_milk_cans'),
                            "mix_milk_cans": q.get('mix_milk_cans'),
                            "cow_milk_sam": k[0],
                            "buf_milk_sam": k[1],
                            "mix_milk_sam": k[2],
                            "time":q.get('time'),
                            "van_col":q.get('van_collection'),
                            }

                    )
                    print('fd-------------------------',fd) 
            # if fd not in data:  
                    data.append(fd)


                
            

        #     if row not in data:
        #         data.append(row)
                    # if dict_sam[r][1]:
                        
                    #     for bs in dict_sam[r][1]:
                    #         row = {
    
                    #             "buf_milk_sam": bs
                    #         }
                    #         if row not in data:
                    #             data.append(row)
                    # if dict_sam[r][2]:
                    #     for ms in dict_sam[r][2]:
                    #         row = {
    
                    #             "mix_milk_sam": ms
                    #         }
                    #         if row not in data:
                    #             data.append(row)
                # print("======row",row)
                
	
    return data


def get_conditions(filters):
    print("=====filters",filters)
    query = """      """
    if filters:
        if filters.get('parent'):
            query += """ where  vci.van_collection = '%s' """%filters.parent
# 		if filters.get('dcs'):
# 		    query += """ and  dcs_id = '%s'  """%filters.dcs
# 		if filters.get('member'):
# 		    query += """ and  member = '%s'  """%filters.member
# 		if filters.get('pricelist'):
# 		    query += """ and  milk_rate = '%s'  """%filters.pricelist
# 		if filters.get('shift') != 'All':
# 		    query += """ and  shift = '%s' """%filters.shift
# 		if filters.get('milk_type') != 'All':
# 		    query += """ and  milk_type = '%s' """%filters.milk_type
        
    return query
