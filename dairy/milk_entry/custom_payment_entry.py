import csv
import io
import random

import frappe
import json

@frappe.whitelist()
def get_filter_data(filter_list):
    
    d_data =[]
    if filter_list:   
        data = json.loads(filter_list)
        for d in data:
            d_data.append(d)


    a={}
    for d in d_data:
        # a.update({str(d[1]):[str(d[2]),d[3]]})
        a.update({str(d[1]):[str(d[2]),d[3]]})
    
    
    my_dict = a

    keys_list = list(my_dict.keys())
    keys_list1 = keys_list

    values_list = list(my_dict.values())
    values_list1 = values_list

    n =[]
    for d in values_list1:
        n.append(d[0])
        n.append(d[1])

    for x in n:
        keys_list1.append(x)
    
    



    f =frappe.get_all('Payment Entry',a,["*"])
    # print("********************************///////////////////",f)
    l =[]
    for d in f:
        x =[]
      
        x.append(d.name)
        x.append(d.creation)
        x.append(d.modified)
        x.append(d.modified_by)
        x.append(d.owner)
        x.append(d.docstatus)
        x.append(d.idx)
        x.append(d.naming_series)
        x.append(d.payment_type)
        x.append(d.payment_order_status)
        x.append(d.posting_date)
        x.append(d.company)
        x.append(d.mode_of_payment)
        x.append(d.party_type)
        x.append(d.party)
        x.append(d.party_name)
        x.append(d.bank_account)
        x.append(d.party_bank_account)
        x.append(d.contact_person)
        x.append(d.contact_email)
        x.append(d.party_balance)
        x.append(d.paid_from)
        x.append(d.paid_from_account_type)
        x.append(d.paid_from_account_currency)
        x.append(d.paid_from_account_balance)
        x.append(d.paid_amount)
        x.append(d.paid_amount_after_tax)
        x.append(d.source_exchange_rate)
        x.append(d.base_paid_amount)
        x.append(d.base_paid_amount_after_tax)
        x.append(d.received_amount)
        x.append(d.received_amount_after_tax)
        x.append(d.target_exchange_rate)
        x.append(d.base_received_amount)
        x.append(d.base_received_amount_after_tax)
        x.append(d.total_allocated_amount)
        x.append(d.base_total_allocated_amount)
        x.append(d.unallocated_amount)
        x.append(d.difference_amount)
        x.append(d.purchase_taxes_and_charges_templete)
        x.append(d.sales_taxes_and_charges_templete)
        x.append(d.apply_tax_withholding_amunt)
        l.append(x)


    path = '/home/erpuser/Downloads/'
    ran = random.randint(0,9999999999)
    full_name = path + str(ran) +".csv"

    # print("$$$$$$$$$$$$$$$$$",full_name)
  
    with open(full_name, 'w') as file:
        field = ["name", "creation"]
        writer = csv.writer(file)
        # writer.writerow(field)
        for row in  l:
            writer.writerow(row)

   
#    # field names 
#     fields = ['Name', 'Branch', 'Year', 'CGPA'] 

#     # data rows of csv file 
#     rows = l

#     # name of csv file 
#     filename = "university_records.csv"

#     # writing to csv file 
#     with open(filename, 'w') as csvfile: 
#         # creating a csv writer object 
#         csvwriter = csv.writer(csvfile) 

#         # writing the fields 
#         csvwriter.writerow(fields) 

#         # writing the data rows 
#         csvwriter.writerows(rows)
        







   




























# @frappe.whitelist()
# def download_csv(request):
#     data = [
#         {'Name': 'John', 'Age': 28, 'City': 'New York'},
#         {'Name': 'Jane', 'Age': 32, 'City': 'Los Angeles'},
#         {'Name': 'Bob', 'Age': 41, 'City': 'Chicago'}
#     ]
#     csv_file = io.StringIO()
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(['Name', 'Age', 'City'])
#     for row in data:
#         csv_writer.writerow([row['Name'], row['Age'], row['City']])
#     csv_file.seek(0)
#     response = HttpResponse(csv_file, content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="data.csv"'
#     return response  






























#//////////////////////////////////////Method no.2////////////////////////////////////////













