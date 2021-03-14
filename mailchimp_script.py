from mailchimp3 import MailChimp
import hashlib
import pandas as pd
from string import Template
import os
import config
from bs4 import BeautifulSoup


client = MailChimp(mc_api=config.MAILCHIMP_API_KEY)  


def create_a_list(list_name, company, address, city, state, zip, country, from_name, from_email, subject, permission_reminder='yes'):
    '''
    Creates a new list using the function parameters
    NB: list and email list are the same 
    '''
    data = {
        "name": list_name,
        "contact": {
            "company": company,
            "address1": address,
            "city": city,
            "state": state,
            "zip": zip,
            "country": country
        },
        'permission_reminder': permission_reminder,
        'campaign_defaults': {
            'from_name': from_name,
            'from_email': from_email,
            'subject': subject,
            'language': 'English'
            
        },
        "email_type_option": True
    }
    
    try:
        return client.lists.create(data=data)
        
    except Exception as e:
        print(e)
        print('You can only create one list with the mailchimp free plan'.upper())
    

def create_a_list_and_add_contacts():
    '''
    Creates a list and adds contacts to the created list
    using the information in the config file
    Created contacts are subscribed by default when created
    '''
    usernames = list(config.MAILING_LIST.keys())
   
    for username in usernames[0:1]:
        #sliced 0:1 because there can be only one list in mailchimp free plan
        try:
            #you can only have one list because of the free mailchimp plan
            list_id = client.lists.all(get_all=True)['lists'][0]['id']
            
            with open('list_names_and_ids.txt', 'w') as f:
                f.write(username + '-->' + str(list_id))
            
            for contact in config.MAILING_LIST[username]:
                add_a_contact_to_list(list_id=list_id, email_address=contact['email'], fname=contact['first_name'], lname=contact['last_name'], status='unsubscribed')
            
        except Exception as e:
            email_list = create_a_list(list_name=username, company=config.USERNAMES_DATA[username]['company'], 
            address=config.USERNAMES_DATA[username]['address'], city=config.USERNAMES_DATA[username]['city'], 
            state=config.USERNAMES_DATA[username]['state'], zip=config.USERNAMES_DATA[username]['zip'], 
            country=config.USERNAMES_DATA[username]['country'], 
            from_name=config.USERNAMES_DATA[username]['from_name'], from_email=config.USERNAMES_DATA[username]['from_email'], 
            subject=config.USERNAMES_DATA[username]['subject'])
            list_name = username
            list_id= email_list['id']
            print('A list with a list id {} was created successfully'.format(list_id))
            
            with open('list_names_and_ids.txt', 'w') as f:
                f.write(list_name + '-->' + str(list_id))
                
            for contact in config.MAILING_LIST[username]:
                add_a_contact_to_list(list_id=list_id, email_address=contact['email'], fname=contact['first_name'], lname=contact['last_name'], status='subscribed')
               
    print('Done')
    

def create_a_campaign(list_id=None):
    '''
    Creates a campaign with the given function parameters
    '''
    if not list_id:
        list_id = client.lists.all()['lists'][0]['id']
        
    if not check_if_list_exists(list_id):
        raise('list with an id of '+ list_id + ' does not exis')
        
    if os.path.exists(os.path.join(os.getcwd(), 'campaign.txt')):
        raise('You can only create only one campaign')
        
    username = list(config.USERNAMES_DATA.keys())[0]
    
    data = {
            "recipients" :
            {
                "list_id": list_id
            },
            "settings":
            {
                "subject_line": config.USERNAMES_DATA[username]['subject'],
                "from_name": config.USERNAMES_DATA[username]['from_name'],
                "reply_to": config.USERNAMES_DATA[username]['reply_to']
            },
            "type": "regular"
        }

    new_campaign = client.campaigns.create(data=data)
    
    with open('campaign.txt', 'w') as f:
        f.write(username + '-->' + new_campaign['id'])
        
    print('Campaign created successfully')
    return new_campaign['id']




def get_lists_names_and_ids():
    '''
    prints and saves as a txt file all lists names and
    their corresponding ids
    '''
    arr = []
    for item in client.lists.all()['lists']:
        obj = {}
        obj['List_Name'] = item['name']
        obj['List_Id'] = item['id']
        arr.append(obj)
        print(item['name'] + '-->'+item['id'])
     
    file_name = 'Lists_Names_And_Ids.csv'
    df1 = pd.DataFrame(arr)
    df1.to_csv(file_name, index=False)
    print('check the current working directory for '+file_name)
    
    
        

def check_if_contact_exists(email_address, list_id=None):
    ''' Checks if a user exists in a list
    '''
    if not list_id:
        list_id = client.lists.all()['lists'][0]['id']
            
    subscriber_hash = hashlib.md5(email_address.lower().encode())
    subscriber_hash = subscriber_hash.hexdigest()
    try:
        contact = client.lists.members.get(list_id=list_id, subscriber_hash=subscriber_hash)
        return True
        
    except Exception:
        return False
        
        
def check_if_list_exists(list_id=None):
    try:
        if not list_id:
            list_id = client.lists.all()['lists'][0]['id']
            
        client.lists.get(list_id=list_id)
        return True
        
    except Exception:
        return False
    
    
 

def add_a_contact_to_list(email_address, fname, lname, status='unsubscribed', list_id=None):
    '''
    Adds a member to an existing list using the list_id
    '''
    
    #Check if email exists first
    if not list_id:
        list_id = client.lists.all()['lists'][0]['id']
        
    if not check_if_contact_exists(list_id=list_id, email_address=email_address):
        try:
            client.lists.members.create(list_id, {
            'email_address': email_address,
            'status': status,
            'merge_fields': {
                'FNAME': fname,
                'LNAME': lname,
            },
        })
    
            print(fname + ' with an email of ' + email_address + ' was added successfully to list with a list_id of ' + list_id)
    
        except Exception as e:
            print(e)
        
    else:
        print(email_address + ' already exists! passing')
        
    

    
    
    
    
def delete_a_contact_from_a_list(email_address, list_id=None):
    '''
    Deletes a member from a list using the list_id and email_address
    of a contact 
    '''
    
    #Check if contact exists first
    if not list_id:
        list_id = client.lists.all()['lists'][0]['id']
        
    if not check_if_contact_exists(list_id, email_address):
        raise Exception('Can not delete contact because '+email_address + ' does not exist')
    
    subscriber_hash = hashlib.md5(email_address.lower().encode())
    subscriber_hash = subscriber_hash.hexdigest()
    client.lists.members.delete(list_id, subscriber_hash=subscriber_hash)
    


def delete_all_campaigns():
    for campaign in client.campaigns.all()['campaigns']:
        c_id = campaign['id']
        client.campaigns.delete(campaign_id=c_id)
        
    os.remove(os.path.join(os.getcwd(), 'campaign.txt'))
    print('All campaigns deleted successfully')
    
    
def delete_all_lists():
    for lst in client.lists.all()['lists']:
        lst_id = lst['id']
        client.lists.delete(list_id=lst_id)
    print('All lists deleted successfully')



def get_all_contacts_from_a_list(list_id=None): 
    ''' Displays and makes a csv of all
    contacts in a given list_id
    '''
    contacts_array = []
    
    if not list_id:
        list_id = client.lists.all()['lists'][0]['id']
        
    for member in client.lists.members.all(list_id, get_all=True)['members']:
        obj = {}
        unique_email_id = member['unique_email_id']
        contact_id = member['id']
        contact_email = member['email_address']
        contact_subscribed_status = member['status']
        first_name = member['merge_fields']['FNAME']
        last_name = member['merge_fields']['LNAME']
        
        obj['Contact_ID'] = contact_id
        obj['Contact_Email'] = contact_email
        obj['Contact_Subscribed_Status'] = contact_subscribed_status
        obj['First_Name'] = first_name
        obj['Last_Name'] = last_name
        
        contacts_array.append(obj)
        
    file_name = 'All_Contacts_From_List_.csv'  
    df1 = pd.DataFrame(contacts_array)
    df1.to_csv(file_name, index=False)
    print('check the current working directory for '+file_name)
    
    
def get_all_campaigns():
    ''' Saves all campaigns to a csv file
    in the current working directory
    '''
    arr = []
    for campaign in client.campaigns.all(get_all=True)['campaigns']:
        obj = {}
        campaign_id = campaign['id']
        campaign_type = campaign['type']
        created_at = campaign['create_time']
        emails_sent = campaign['emails_sent']
        send_time = campaign['send_time']
        content_type = campaign['content_type']
        list_id = campaign['recipients']['list_id']
        list_name = campaign['recipients']['list_name']
        recipient_count = campaign['recipients']['recipient_count']
        
        obj['Campaign_id'] = campaign_id
        obj['Campaign_type'] = campaign_type
        obj['Created_at'] = created_at
        obj['Emails_sent'] = emails_sent
        obj['Send_time'] = send_time
        obj['Content_type'] = content_type
        obj['List_id'] = list_id
        obj['List_name'] = list_name
        obj['Recipient_count'] = recipient_count
        arr.append(obj)
        
    df = pd.DataFrame(arr)
    df.to_csv('All_Campaigns.csv', index=False)
    print('Open All_Campaigns.csv in the current directory to see campaigns')
    
    
    

 
def subscribe_a_contact(email_address, list_id=None):
    '''
    To subscribe a contact
    Note only subscribe contacts would be able to recieve campaign emails sent
    '''
    #Check if contact exists
    if not list_id:
        list_id = client.lists.all()['lists'][0]['id']
        
    if not check_if_contact_exists(list_id, email_address):
        raise Exception(email_address + ' not in contact list')
        
        
    try:
        client.lists.update_members(list_id=list_id, data={
            'members':[{'email_address': email_address, 'status': 'subscribed'}],
            'update_existing': True,
        })
        print(email_address + ' successfully subscribed')
        
    except Exception as e:
        print(e)
        print('Please ensure your entered the correct list_id or email_address'.upper())
    
    
def unsubscribe_a_contact(email_address, list_id=None):
    #Check if contact exists
    if not list_id:
        list_id = client.lists.all()['lists'][0]['id']
    
    if not check_if_contact_exists(list_id, email_address):
        raise Exception(email_address + ' not in contact list')
        
    try:
        client.lists.update_members(list_id=list_id, data={
            'members':[{'email_address': email_address, 'status': 'unsubscribed'}],
            'update_existing': True,
        })
        print(email_address + ' successfully unsubscribed')
        
    except Exception as e:
        print(e)
        print('Please ensure your entered the correct list_id or email_address'.upper())
        
 
def get_html_template():
    for path, dirs, files in os.walk(os.getcwd(), 'template'):
        for file in files:
            if file.endswith('.html'):
                target_path = os.path.join(path, file)
                break
    try:            
        with open(target_path) as f:
            raw_html = f.read()
            
    except Exception as e:
        raise Exception(e)
        
    return raw_html
                
    
 
        
def send_campaign_email():
    '''
    To send a campaign email to subscribed contacts
    place the email template html file in the template directory 
    in the working directory
    '''
    campaign_id = create_a_campaign()
    html_code= '<h1>Hello world. Testing mailchimp</h1>'
    raw_html = get_html_template()
    soup = BeautifulSoup(raw_html, 'html.parser')
    html_code = str(soup)
    string_template = Template(html_code).safe_substitute()
        
    try:
        client.campaigns.content.update(
        campaign_id=campaign_id,
        data={'message': 'my message2', 'html': string_template}
        )
    
    except Exception as e:
        print(e)
    
    try:
        client.campaigns.actions.send(campaign_id=campaign_id)
        print('Campaign message sent successfully')
    except Exception as e:
        print(e)
    
    
    
def get_email_report():
    '''
    Returns a csv report of the campaign emails sent
    '''
    arr = []
    campaign_id = client.campaigns.all()['campaigns'][0]['id']
    data = client.reports.email_activity.all(campaign_id=campaign_id, get_all=True)
    
    for item in data['emails']:
        obj = {}
        campaign_id = item['campaign_id']
        list_id = item['list_id']
        email_address = item['email_address']
        if item['activity']:
            for info in item['activity']:
                if info['action'] == 'open':
                    has_been_read = 'Contact has opened and read the email'
                else:
                    has_been_read = 'Unknown'
                    
                time_opened = info['timestamp']
                ip_address = info['ip']
                
        else:
            has_been_read = 'Not opened yet'
            time_opened = ''
            ip_address = ''
            
        obj['Campaign_id'] = campaign_id
        obj['List_id'] = list_id
        obj['Email_address'] = email_address
        obj['Has_been_read'] = has_been_read
        obj['Time_stamp'] = time_opened
        obj['Ip_address'] = ip_address
        
        arr.append(obj)
        
    df = pd.DataFrame(arr)
    df.to_csv('campaign_email_report.csv', index=False)
    print('Check your working directory for campaign_email_report.csv to see the report')
        
        
        
        
        
        
        
        
        

























































