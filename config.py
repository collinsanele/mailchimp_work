#################### CONFIG VALUES ###################################################################
#NB: All emails and names used here are mine and was used for testing. Replace them with your's


MAILCHIMP_API_KEY = 'ADD YOUR API KEY HERE'


#NB: Only the contacts for murat would be used because of the mailchimp free plan restriction
MAILING_LIST = {'murat':
                    [{'first_name': 'Alex', 'last_name': 'Simon', 'email': 'pycollins2021@gmail.com'},
                     {'first_name': 'Mike', 'last_name': 'Abdul', 'email': 'collinsanele@gmail.com'},
                     {'first_name': 'Collins', 'last_name': 'Anele', 'email': 'chuks_capon@yahoo.com'}
                    ],
                
                }



#Needed when creating a mailing list
USERNAMES_DATA = {
    'murat': {'from_name': 'Murat','email': 'collinsanele@gmail.com', 
    'reply_to': 'collinsanele@gmail.com', 'company': 'murat company', 
    'address': 'vegas island', 'city': 'some city', 
    'state': 'some state', 'zip': '1234', 
    'country': 'Quatar', 'from_name': 'Murat', 
    'from_email': 'collinsanele@gmail.com', 'subject': 'Put a subject here'}
    
}




























