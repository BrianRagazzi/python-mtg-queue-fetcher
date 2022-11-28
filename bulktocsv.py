#!/usr/bin/env python

import os
import sys
import csv
import json



source_json="default-cards-20221127100506.json"
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
        val=cardjson["prices"]["usd_foil"]
        if cardjson["nonfoil"]:
            val=cardjson["prices"]["usd"]
    except KeyError:
        val=""
    return val

def getCardRarity(cardjson):
    try:
        val=cardjson["rarity"]
    except KeyError:
        val=""
    return val

def cardisDigital(cardjson):
    try:
        val=cardjson["digital"]
    except KeyError:
        val="false"
    return val

def cardisFoil(cardjson):
    try:
        val=cardjson["foil"]
    except KeyError:
        val="false"
    return val


def main():
    print(" [*] Starting up")

    bulk= open(source_json,)
    cardData = json.load(bulk)
    print(" [*] Retrieved card data")
    with open(csv_filename,"w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',',doublequote=True,quoting=csv.QUOTE_ALL)
        writer.writerow(["name","cmc","type_line","usd","rarity","foil"])
        for card in cardData:
            name=getCardName(card)
            cmc=getCardCMC(card)
            cardtype=getCardType(card)
            usd=getCardValue(card)
            rarity=getCardRarity(card)
            if cardtype.startswith("Card"):
                print(" [-] Skipping fake Card: " + name)
            else:
                if cardisDigital(card):
                    print(" [-] Skipping Digital Card: " + name)
                else:
                    print(" [+] Adding " + name)
                    row = [name,cmc,cardtype,usd,rarity,str(cardisFoil(card))]
                    writer.writerow(row)
    print(" [*] Closing File, exiting")        
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