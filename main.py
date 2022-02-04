import requests
import json
from flight_search import Flight_seach as fs
from email_service import Email


# Clearing the data text file
with open('data_text' , 'w') as file :
    file.write('')


# Flight search
def flight_checker(des , min ) :
    sh = fs(destination=des , min_price=min , month = 6)

# Searches through the flight name json file
with open(file = 'flight_data.json' , mode = 'r') as flights :
    file = json.load(flights)
    for i in range(0 , len(file['data'])) :
        city_code , min_price = file['data'][i]["code"], file['data'][i]['lowestPrice']
        flight_checker(des = city_code , min = min_price)

mail = Email()
# Mailing the user
mail.mail_system()



