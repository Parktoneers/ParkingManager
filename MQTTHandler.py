#!/usr/bin/python3

# import board
# import busio

# import RPi.GPIO as GPIO

import time
import config
import traceback
import os
from datetime import date
from config import *
import paho.mqtt.client as mqtt
from DatabaseHandler import DatabaseHandler
from Place import Place

BROKER_HOST = "io.adafruit.com"
PORT = 1883
ADAFRUIT_USERNAME = "szymonkieczka"
ADAFRUIT_KEY = "aio_JBkg13U2vZjeHxZlbvD5u91Py0EG"

PHONE_TOPIC = "szymonkieczka/feeds/phone-reservation-feed"
SMS_TOPIC = "szymonkieczka/feeds/sms-reservation-feed"

CARD_TOPIC = "szymonkieczka/feeds/gate-feed"
GATE_TOPIC = "szymonkieczka/feeds/gate-feed-opening"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("Connected OK")
        client.subscribe("test_user/errors", qos=0)
        client.subscribe(SMS_TOPIC, qos=0)
        client.subscribe(PHONE_TOPIC, qos=0)
        client.subscribe(CARD_TOPIC, qos=0)
    else:
        print("Bad connection Returned code=", rc)


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    # print("topic: {} value: {}".format(msg.topic, payload))
    db = DatabaseHandler()
    if msg.topic == PHONE_TOPIC or msg.topic == SMS_TOPIC:
        phone = payload
        user = db.getAccount(phoneNumber=phone)
        if user is None:
            print("User not found.")
            return
        if user.parkingSpace is None:
            place = db.getFreePlace()
            if place is not None:
                db.updatePlace(Place(place.parkingSpace, 1, 0))  # rezerwuje wolne miejsce
                user.parkingSpace = place.parkingSpace
                db.updateAccount(user)
                print(f"User {user.name} reserved space {place.parkingSpace}.")
            else:
                print(f"No parking spaces available for user {user.name}.")
        else:
            print(f"User {user.name} already has a parking space.")
    elif msg.topic == CARD_TOPIC:
        # GPIO.output(buzzerPin, True)
        # time.sleep(1)
        # GPIO.output(buzzerPin, False)
        uid = [int(uid) for uid in payload.split(" ")]
        user = db.getAccount(uid=uid)
        if user is None:
            print("User not found.")
            return
        if user.parkingSpace is None:
            print(f"User {user.name} doesn't have a parking space reserved.")
        else:
            place = db.getPlace(user.parkingSpace)
            if place.occupied == 0:
                print(f"User {user.name} enters the parking at place {user.parkingSpace}.")
                db.updatePlace(Place(place.parkingSpace, 1, 1))
            else:
                print(f"User {user.name} leaves the parking from place {user.parkingSpace}.")
                db.updatePlace(Place(place.parkingSpace, 0, 0))
                user.parkingSpace = None
                db.updateAccount(user)
            client.publish(GATE_TOPIC, "OPEN")
    db.db.close()


def run():
    mqtt.Client.connected_flag = False
    client = mqtt.Client("ClientServer")
    client.on_connect = on_connect
    client.on_message = on_message
    print("Connecting to broker ", BROKER_HOST)
    client.username_pw_set(ADAFRUIT_USERNAME, password=ADAFRUIT_KEY)
    client.connect(BROKER_HOST, port=PORT)
    client.loop_start()
    while not client.connected_flag:
        print("Waiting for connection")
        time.sleep(1)
