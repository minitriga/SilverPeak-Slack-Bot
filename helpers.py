from silverpeak import *
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from tabulate import tabulate
import json

# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sp = Silverpeak(user="agitting", user_pass="Axians123!", sp_server="192.168.33.2")

def appliances():
    appliances = sp.get_appliances()
    appliances_table = [
              "Here are the appliances I know about...\n"
              "\n"
              ]

    for item in appliances.data:
        row = "        |> *{}* - {} - {} - {} - {} - {}\n"
        row = row.format(str(item['id']), item['hostName'], item['IP'], item['serial'], item['model'], item['softwareVersion'])
        appliances_table.append(row)

    return ''.join(appliances_table)
