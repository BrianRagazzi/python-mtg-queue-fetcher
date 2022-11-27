#!/usr/bin/env python

import os
import sys
import csv
import json



source_json="oracle-cards-20221126100305.json"
csv_filename="cards.csv"


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

    bulk= open(source_json,)
    cardData = json.load(bulk)
    print(" [*] Retrieved card data")
    with open(csv_filename,"w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',',doublequote=True,quoting=csv.QUOTE_ALL)
        writer.writerow(["name","cmc","type_line","usd"])
        for card in cardData:
            name=getCardName(card)
            cmc=getCardCMC(card)
            cardtype=getCardType(card)
            usd=getCardValue(card)
            print(" [*] Adding " + name)
            if cardtype.startswith("Card"):
                print("ignoring fake card")
            else:
                row = [name,cmc,cardtype,usd]
            writer.writerow(row)
            
    csv_file.close()  
    bulk.close()





if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)