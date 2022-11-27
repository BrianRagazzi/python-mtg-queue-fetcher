#!/usr/bin/env python

import os
import sys
import csv
import time
#import base64
import json

#import pika
#import wget
# import urllib3.request
#from genericpath import isfile
# from minio import Minio
# from minio.error import S3Error
import requests
from requests.exceptions import HTTPError
# import hashlib


scryfall_set_search="https://api.scryfall.com/sets"
scryfall_card_serch="https://api.scryfall.com/cards/search?format=json&include_extras=true&include_multilingual=false&include_variations=true&order=name&page=1&unique=cards&q=s%3A"
csv_filename="cards.csv"
setcode="mb1"


def getCardName(cardjson):
    try:
        name=cardjson["card_faces"][0]["name"]
    except KeyError:
        name=cardjson["name"]
    return name

def getCardCMC(cardjson):
    try:
        val=cardjson["cmc"]
    except KeyError:
        val=""
    return val

def getCardType(cardjson):
    try:
        val=cardjson["type_line"]
    except KeyError:
        val=""
    return val

def getCardValue(cardjson):
    try:
        val=cardjson["prices"]["usd"]
    except KeyError:
        val=""
    return val


def main():
    print(" [*] Starting up")

    
    cardData = json.loads(getCardData(setcode))
    print(" [*] Retrieved card data")
    with open(csv_filename,"w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',',doublequote=False,quoting=csv.QUOTE_ALL)
        writer.writerow(["name","cmc","type_line","usd"])
        for card in cardData:
            name=getCardName(card)
            cmc=getCardCMC(card)
            cardtype=getCardType(card)
            usd=getCardValue(card)
            print(" [*] Adding " + name)
            row = [name,cmc,cardtype,usd]
            writer.writerow(row)
            
    csv_file.close()  

    
    




def getCardData(setcode):
    try:
        scryfallurl = scryfall_card_serch + setcode
        response = requests.get(scryfallurl)
        responseJson = json.loads(response.text)
        carddata = responseJson["data"]
        has_more = responseJson["has_more"]
        cardcount = len(carddata)
        while str(has_more) == "True":
            print(" [*] getting next batch")
            nextpage = responseJson["next_page"]
            response = requests.get(nextpage)
            responseJson = json.loads(response.text)
            carddata.extend(responseJson["data"]) #add the new list to the original
            has_more = responseJson["has_more"]
        cardcount = len(carddata)
        print("final card count: %s" % cardcount)
        carddata = json.dumps(carddata) #Restore valid json with double-quotes
        return carddata

    except HTTPError as http_err:
        print(f' [!] HTTP error occurred: {http_err}')
    except Exception as err:
        print(f' [!] Other error occurred: {err}')






if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)