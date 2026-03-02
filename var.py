# Modules
from dotenv import load_dotenv
import os

##### VARIABLES #####

load_dotenv()

##### LNBITS #####

x_api_key = os.getenv("LNBITS_KEY")
lnbits_server = os.getenv("LNBITS_SERVER", "send.laisee.org")