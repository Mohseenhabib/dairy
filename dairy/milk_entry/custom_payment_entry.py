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
    a = 0
    l =[]
    for d in f:
        a = a+1
        ifsc = frappe.get_value("Bank Account",{"bank_account_no":d.bank_account_no},["branch_code"])
        x =[]
      
        x.append("N")
        x.append("           ")
        x.append(d.bank_account_no)
        x.append(d.paid_amount)
        x.append(d.party_name)
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append(str(d.posting_date) + "-"+ str("{:03d}".format(a)))
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append("           ")
        x.append(ifsc)
        x.append(d.bank)
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




































