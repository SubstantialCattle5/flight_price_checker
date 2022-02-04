import os
import smtplib
import json
from dotenv import load_dotenv  # pip install python-dotenv
load_dotenv("E:\PROJECTS\python\local_env\\flight_cheap\.env.txt")


# Sender's Email
MYEMAIL , MYPASSWORD = os.getenv('myemail') , os.getenv('mypw')

# Receiver's Email
sender = 'samless2@outlook.com'


# Figuring out the protocol for the email service
with open(file = 'web_smtp_protocols.json') as file :
    data = json.load(file)
    try :
        email_service_smtp = data[MYEMAIL.split('@')[1].split('.')[0]]
    except AttributeError :
        print()



class Email :
    def __init__(self):
        self.subject , self.body = 'test' , 'test'
        with  open('data_text' , 'r')  as filename :
            self.subject  , self.body  = 'Cheap Flights' , filename.read()



    def mail_system(self) :
        with smtplib.SMTP(email_service_smtp) as connection:
            if email_service_smtp != None :
                # Encrypting the mail contents
                connection.starttls()
                connection.login(user=MYEMAIL, password=MYPASSWORD)
                # sending the mail
                connection.sendmail(from_addr=MYEMAIL,
                                    to_addrs=f'{sender}',
                                    msg=f'Subject : {self.subject} \n\n {self.body} ')

