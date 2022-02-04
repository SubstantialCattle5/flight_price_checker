import json
import os
from datetime import datetime as dt
import requests
import datetime
import dateutil.relativedelta
from dotenv import load_dotenv  # pip install python-dotenv
load_dotenv("E:\PROJECTS\python\local_env\\flight_cheap\.env.txt")




now = dt.now()

class Flight_seach :
    def __init__(self , destination , min_price , month = 1 ):

        self.CURRENT_LOCATION  = 'BOM'
        self.CURRENT_DATE = now.strftime('%d/%m/%Y')

        self.dates , self.price = [] , []  # List of all the prices lower than min_price + their dates
        # Cheapest stuff
        self.cheapest , self.cheaper_date = 0 , 0 # Cheapest flight cost
        self.flag = True
        self.city_name = str()
        self.body = list()

        flight_api = os.getenv('flightapi')
        header = {
            'apikey': os.getenv('flightapikey')
        }

        self.query = {
            'fly_from': self.CURRENT_LOCATION,
            'fly_to': destination,
            'dateFrom': self.CURRENT_DATE,
            'dateTo': (datetime.date.today()+dateutil.relativedelta.relativedelta(months=month)).strftime('%d/%m/%Y'),
            'curr': 'INR',
            'price_to': int(min_price)
        }

        self.rep = requests.get(url=flight_api, headers=header, params=self.query)
        self.search()

        # Fixing the error for when flights are unavailable
        try :
            self.compare()
        except :
            print(f'{destination} cheap flights not available')
            print()
            self.flag = False

    def search(self):
        with open('flight_result.json' , 'w+') as file :
            json.dump(self.rep.json() , file , indent = 4)
        with open('flight_result.json' , 'r') as data :
            file = json.load(data)

            for i in range(0, len(file['data'])):
                    if file['data'][i]['availability']['seats'] == None : continue
                    self.price = self.price + [int(file['data'][i]['price'])]
                    self.dates = self.dates + [file['data'][i]['route'][0]['local_departure'].split('T')[0]]

    def compare(self):
        if self.flag:
            check = 0
            self.cheapest = min(self.price)

            with open('flight_result.json' , 'r' ) as data :
                file = json.load(data)
                for i in range(0 , len(file['data'])) :
                    if file['data'][i]['price'] == self.cheapest :
                        check = i
                        break

                self.cheaper_date  = file['data'][check]['route'][0]['local_departure'].split('T')[0]
                print(f"Id : {file['data'][check]['id']}")
                print(f"From : {file['data'][check]['cityFrom']}")
                print(f"To : {file['data'][check]['cityTo']}")
                print(f"Price : {file['data'][check]['price']} ")

                print(f"Seats Available : {file['data'][check]['availability']['seats']} ")
                print(f"Airline : {file['data'][check]['airlines']}")
                print(f"Flight Departure Date : {file['data'][check]['route'][0]['local_departure'].split('T')[0]}")
                print()

                # For the Email service
                body = f''' 
                Id : {file['data'][check]['id']}
                From : {file['data'][check]['cityFrom']}
                To : {file['data'][check]['cityTo']}
                Price : {file['data'][check]['price']}
                Seats Available : {file['data'][check]['availability']['seats']}
                Airline : {file['data'][check]['airlines']}
                Flight Departure Date : {file['data'][check]['route'][0]['local_departure'].split('T')[0]}
                
                '''

                with open('data_text' , 'a' ) as file :
                    file.write(body)
