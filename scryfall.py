#!/usr/bin/env python

import os
import sys
import time
import base64
import json
import pika
import wget
# import urllib3.request
from genericpath import isfile
# from minio import Minio
# from minio.error import S3Error
import requests
from requests.exceptions import HTTPError
# import hashlib


scryfall_set_search="https://api.scryfall.com/sets"
scryfall_card_serch="https://api.scryfall.com/cards/search?format=json&include_extras=true&include_multilingual=false&include_variations=true&order=name&page=1&unique=cards&q=s%3A"
host="192.168.103.27"
qname="cards"
rabbitmq_username="myuser"
rabbitmq_password="mypass"

def main():
    print(" [*] Starting up")

    # try:
    #     response = requests.get(scryfall_set_search)
    #     response.raise_for_status()
    #     #jsonResponse = response.json
    #     thing = setCodes(response.text)
    #     print(thing)
        
    # except HTTPError as http_err:
    #     print(f'HTTP error occurred: {http_err}')
    # except Exception as err:
    #     print(f'Other error occurred: {err}')
    rabbit_credentials = pika.PlainCredentials(rabbitmq_username,rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials=rabbit_credentials))
    channel = connection.channel()
    channel.queue_declare(queue=qname, durable=True)
    # channel.basic_publish(exchange='',routing_key=qname,body="Hello World")

    cardData = getCardData("mh2")
    for card in cardData:
        print(card["name"])
        #print(card)
        channel.basic_publish(exchange='',routing_key=qname,body=str(card))
    connection.close()


# def setCodes():
#     codeslist =[]
#     # put setcodes into a list
#     response = requests.get(scryfall_set_search)
#     response.raise_for_status()
#     y = json.loads(setjson)
#     for set in y["data"]:
#         codeslist.append(set["code"])
#     return codeslist



def getCardData(setcode):
    try:
        scryfallurl = scryfall_card_serch + setcode
        response = requests.get(scryfallurl)
        responseJson = json.loads(response.text)
        carddata = responseJson["data"]
        has_more = responseJson["has_more"]
        cardcount = len(carddata)
        while str(has_more) == "True":
            print("getting next batch")
            nextpage = responseJson["next_page"]
            response = requests.get(nextpage)
            responseJson = json.loads(response.text)
            carddata.extend(responseJson["data"]) #add the new list to the original
            has_more = responseJson["has_more"]
        cardcount = len(carddata)
        print("final card count: %s" % cardcount)

        return carddata

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')






if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)