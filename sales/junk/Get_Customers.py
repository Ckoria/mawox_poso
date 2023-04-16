import requests

#Get Data from RepairShopr
def get_access(url_ext):
    key = 'T3a0c4dafe210a8977-bfe938726430d444731c27ee4a7121f1'
    my_url = "https://allelectronics.repairshopr.com/api/v1/" + url_ext
    headers = {    
            'Accept': 'application/json',  
            'Content-Type': 'application/json',
            'Authorization': 'Token '+ key
            }
    response = requests.get(my_url, headers= headers, verify= True)
    ticket = response.json()
    return ticket

def get_customer(page, status):
    #Get tickets info by status and Page No.
    tickets = get_access("tickets?status=" +status +"&page=" +page)
    tickets = tickets['tickets']
    HA_tickets = [
        ticket for ticket in tickets 
        if ticket.get('problem_type') == 'Home Appliance' or ticket.get('problem_type') == 'In Home Appliances'
        ]
    return HA_tickets

#Data cleaning process 
def get_ticket(page_no, status):
    tickets_list = []
    for page in range(1,(page_no + 1)):
        ticket_list = get_customer(str(page), status)
        for i, ticket in enumerate(ticket_list):
            #Get ticket info by ticket ID
            ticket = get_access("tickets/" +str(ticket_list[i].get("id"))) 
            invoice = get_access("invoices?ticket_id=" +str(ticket_list[i].get("id")))
            try:
                invoices = invoice.get('invoices')[0]
                total = str(invoices.get('total'))
                is_paid = str(invoices.get('is_paid'))
                ticket  = ticket.get('ticket')
                #Get ticket information
                comment = ticket.get("comments")[0]
                #Get asset information
                assets = ticket.get('assets')[0]
                #Get Customer information
                customer_info = assets.get('customer')
                model = assets.get("name")
                #Exclude Microwaves
                if model[:2] != "ME":
                    ticket_info = [
                    customer_info.get("firstname"),
                    customer_info.get("lastname"),
                    str(customer_info.get("phone")),
                    total +" - "+is_paid,
                    model,
                    ticket.get("subject"), 
                    ticket.get("created_at")[:10], 
                    comment.get("created_at")[:10],
                    comment.get("body"), 
                    str(customer_info.get("mobile")),
                    customer_info.get("email"),
                    customer_info.get("address") + customer_info.get("address_2") + customer_info.get("city") 
                    ]
                    tickets_list.append(ticket_info)
            except:
                pass
    return (tickets_list)      
