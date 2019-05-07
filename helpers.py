from silverpeak import *
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from tabulate import tabulate
import json
import settings

# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sp = Silverpeak(user=settings.SP_USER, user_pass=settings.SP_PASS, sp_server=settings.SP_IP)

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
