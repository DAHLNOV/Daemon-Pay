import requests
import json
import random
from django.conf import settings
from paysystem.models import *

def crearTransaccion(user):
    buy_order = str(random.randrange(10000,999999))
    session_id = str(random.randrange(1000000,99999999))