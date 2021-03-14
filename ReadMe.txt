################## NOTE TO CLIENT #############################################################
Do not forget to do (pip install -r requirements.txt) to install all needed libraries/modules

Please add your api key in the config.py file

You can only create one list (aka audience) with the free tier so add your contacts to the user murat in the config file

There are many functions but the functions that you would need according to your requirements are as follows:


create_a_list_and_add_contacts (run this after you make any changes to the contacts list in the config.py file)


delete_a_contact_from_a_list 


delete_all_campaigns (You would need to run this function after you have sent a campaign and you wish to create another campaign to send again)


delete_all_lists


get_all_contacts_from_a_list (Run this if you need to see all your contacts in a nice csv form)


get_lists_names_and_ids (To get a nice csv report of all list names and their ids. There would only be one list because of the free tier restrictions)


subscribe_a_contact


unsubscribe_a_contact


send_campaign_email (To send CAMPAIGN email after you have added all your contacts in the config file and have run create_a_list_and_add_contacts. You can add the html template to send in the template folder)


get_email_report ( Run this after you have sent the email using the send_campaign_email function. You would get a nice csv report of the status of the emails sent)


#DO NOT HESITATE TO CONTACT ME FOR CLARIFICATION AND MORE INFO



