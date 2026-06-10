import requests
from bs4 import BeautifulSoup
import yagmail
from smtplib import SMTP
import csv 
from datetime import datetime
import time


def get_price(url):
    data=requests.get(url)
    soup=BeautifulSoup(data.text,"html.parser")
    price=soup.find("p", class_="price_color").text
    price_clean=float(price.replace('Â','').replace('£','').strip())
    return(price_clean)

def send_mail(current_price):
    yag=yagmail.SMTP('youremail@gmail.com',"your 16 character password")
    yag.send(
        to='youremail@gmail.com',
        subject='Price Drop Alert !!',
        contents=f"Price ahs dropped to {current_price}!"
    ) 
    print('Email Sent')

def record_data(price):
    with open('C:/booknames.csv','a',newline='') as file:
        writer=csv.writer(file)
        writer.writerow([datetime.now(),price])
        print(f"price ${price} saved to csv")

url='https://books.toscrape.com'
target=60.0

while True:
    try:
        price=get_price(url)
        print(f'Current Price ${price}')
        record_data(price)
        if price<target:
            send_mail(price)
            print('Alert sent')
        else:
            print('Price still higher. Checking again after an hour')
    except:
        print('Eror')
    time.sleep(3600)