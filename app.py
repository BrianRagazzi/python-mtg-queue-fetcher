import os
import sys
import json
import pika
from pika.exceptions import AMQPConnectionError
import requests
from requests.exceptions import HTTPError
from minio import Minio
from minio.error import S3Error
from crypt import methods
from flask import Flask, request, render_template, jsonify
import gunicorn

app = Flask(__name__) #necessary?

client = "VMware"
framework = "Python with Pipenv"
title = "Learning Flask"

scryfall_set_search="https://api.scryfall.com/sets"
scryfall_card_serch="https://api.scryfall.com/cards/search?format=json&include_extras=true&include_multilingual=false&include_variations=true&order=name&page=1&unique=cards&q=s%3A"

host = os.getenv("RABBITMQ_HOST") or "192.168.103.27"
qname = os.getenv("RABBITMQ_QUEUE") or "cards"
rabbitmq_username = os.getenv("RABBITMQ_USERNAME") or "myuser"
rabbitmq_password = os.getenv("RABBITMQ_PASSWORD") or "mypass"

s3server = os.getenv("S3SERVER") or "minio.lab.brianragazzi.com"
s3bucket = os.getenv("S3BUCKET") or "cardimages"
s3accesskey = os.getenv("S3ACCESSKEY") or "MCACCESS"
s3secretkey = os.getenv("S3SECRETKEY") or "MCSECRET"


@app.route("/")
def index():
    return render_template('index.html', client=client, framework=framework,cards=cardsInQueue(),cardimagecount=imagesinBucket())

# @app.route('/messages')
# def get_incomes():
#     return jsonify(messages)

@app.route('/versions')
def versions():
    gu_version = gunicorn.__version__
    return "Gunicorn version: " + gu_version

# @app.route('/my-link')
# def my_link():
#     print ('Button Clicked')
#     return render_template('template.html',title="click", placeholder="Method: %s" % request.method)

# @app.route('/hello/<string:user>')
# def hellothere(user):
#     return render_template('template.html',title="hello", placeholder="hello there %s" % user)

@app.route('/loadset', methods=['GET','POST'])
def loadset():
    if request.method == 'POST':
        # first_name = request.form.get("fname")
        # last_name = request.form.get("lname")
        setcode = request.form.get("setcode")
        try:

            rabbit_credentials = pika.PlainCredentials(rabbitmq_username,rabbitmq_password)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials=rabbit_credentials))
            channel = connection.channel()
            channel.queue_declare(queue=qname, durable=True)
            

            if connection.is_open:
                cardData = json.loads(getCardData(setcode))
                for card in cardData:
                    #print("parsing cards")
                    print(card["name"])
                    
                    channel.basic_publish(exchange='',routing_key=qname,body=json.dumps(card))
                return render_template('submit.html', title="loadSet", client=setcode, placeholder="Items Added: %s" % len(cardData),codelist=setCodes(), list=cardData)
                connection.close()
            else:
                return render_template('submit.html', title="loadSet", client=setcode, placeholder="Channel is not open",codelist=setCodes())
                connection.close

        except AMQPConnectionError as amqp_error:
            print(f'AMQP Error Occurred: {amqp_error}')
            return render_template('submit.html', title="loadSet", client=setcode, placeholder="AMQP Error Occurred: %s" % amqp_error,codelist=setCodes())
        except Exception as err:
            print(f'Other error occurred: {err}')
            return render_template('submit.html', title="loadSet", client=setcode, placeholder="Error Occurred: %s" % err,codelist=setCodes())
        
    else:
        return render_template('submit.html', codelist=setCodes())
        connection.close

# @app.route('/envvar')
# def envvar():
#     host = os.getenv("RABBITMQ_HOST")
#     return render_template('template.html', client=client, title="env var", placeholder="found: %s" % host)

# @app.route('/cards')
# def cards():
#     list = ["savannah", "plains", "Black Lotus"]
#     return render_template('list.html', list=list)

# @app.route('/cardimagecount')
# def cardimagecount():
#     return str(imagesinBucket())



def setCodes():
    codeslist =[]
    # put setcodes into a list
    response = requests.get(scryfall_set_search)
    response.raise_for_status()
    y = json.loads(response.text)
    for set in y["data"]:
        codeslist.append(set)
    return codeslist


def getCardData(setcode):
    try:
        scryfallurl = scryfall_card_serch + setcode
        response = requests.get(scryfallurl)
        responseJson = json.loads(response.text)
        carddata = responseJson["data"]
        has_more = responseJson["has_more"]
        cardcount = len(carddata)
        while str(has_more) == "True":
            #print("getting next batch")
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
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def cardsInQueue():
    try:
        rabbit_credentials = pika.PlainCredentials(rabbitmq_username,rabbitmq_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials=rabbit_credentials))
        channel = connection.channel()
        q = channel.queue_declare(queue=qname, durable=True, passive=True, exclusive=False)
        q_len = q.method.message_count
        channel.close
        connection.close
        return q_len
    except AMQPConnectionError as amqp_error:
            print(f'AMQP Error Occurred: {amqp_error}')
            return 0
    except Exception as err:
        print(f'Other error occurred: {err}')
        return 0

def imagesinBucket():
    client = Minio(s3server,
    access_key=s3accesskey,
    secret_key=s3secretkey)
    objcnt=0
    if client.bucket_exists(s3bucket):
        objects = client.list_objects(s3bucket)
        for obj in objects:
            objcnt=objcnt+1
        return int(objcnt)
    else:
        return int(0)

# not sure this is necessary
# if __name__ == "__main__":
#   app.run(debug=True)

app.debug=False
