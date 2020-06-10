#!/usr/bin/python3

from mitemp.mitemp_bt.mitemp_bt_poller import MiTempBtPoller
from mitemp.mitemp_bt.mitemp_bt_poller import MI_TEMPERATURE, MI_HUMIDITY, MI_BATTERY
from btlewrap.bluepy import BluepyBackend
from bluepy.btle import BTLEException
import paho.mqtt.publish as publish
import datetime
from mqtt_helper import mqtt_helper
import time


device = "lounge"

mqtt_helper = mqtt_helper(device)

mac = "58:2D:34:39:BB:B5"

time_out = 5

poller = MiTempBtPoller(mac, BluepyBackend, ble_timeout=time_out)

while True:

    try:

        temp = poller.parameter_value(MI_TEMPERATURE)
        humidity = poller.parameter_value(MI_HUMIDITY)
        batt = poller.parameter_value(MI_BATTERY)

    except BTLEException as e:
        availability = 'offline'
        print(datetime.datetime.now(), "Error connecting to device {0}: {1}".format(device, str(e)))
    except Exception as e:
        availability = 'offline'
        print(datetime.datetime.now(), "Error polling device {0}. Device might be unreachable or offline.".format(device))
        # print(traceback.print_exc())


    try:
        mqtt_helper.publish_message(temp, humidity, batt)
        mqtt_helper.publish_status()

    except Exception as ex:
        print(datetime.datetime.now(), "Error publishing to MQTT: {0}".format(str(ex)))

    time.sleep(5)