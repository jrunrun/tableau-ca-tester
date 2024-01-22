import requests
import json
import jwt
import datetime
import uuid

import logging
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

# from ca_list_private import ca_list

def auth_CA_JWT_RestAPI():

    # Edit to a real user (bking@salesforce.com)
    ts_username = 'mario.salvatore@demo.com'


    # Create CA on pulse internal site
    # https://us-west-2a.online.tableau.com/site/pulseinternal/pulse/
    ts_ca_iss ='1d92b243-e331-4eb4-a78d-20ab84e00848'
    ts_ca_kid ='e4a54a9b-c20d-4b92-b613-5a5057f9d9cb'
    ts_ca_secret = 'bvr3qjSaPV+a7YVa5JUpoE/H204OZrt/4YTQ+c1czwk='


    # Add Pulse scopes here
    scopesList = ["tableau:content:read", "tableau:views:download"]

    logger.info("username value is {}".format(ts_username))

    CA_SSO_token = jwt.encode(
        {
            "iss": ts_ca_iss,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes = 5),
            "jti": str(uuid.uuid4()),
            "aud": "tableau",
            "sub": ts_username,
            # "scp": ["tableau:content:read", "tableau:views:download", "tableau:lenses:read"]
            "scp": scopesList,
            # "https://tableau.com/oda":"true",
		    # "https://tableau.com/groups": ["OnDemand2"],
		    # "Region": ["East", "Central"]
        },
        ts_ca_secret,
        algorithm = "HS256",
            headers = {
                'kid': ts_ca_kid,
                'iss': ts_ca_iss
            }
        )

    jwt_decode_link = 'https://jwt.io/#debugger-io?token=' + CA_SSO_token

    logger.info("jwt: {}".format(CA_SSO_token))
    logger.info("jwt_decode_link: {}".format(jwt_decode_link))
    

auth_CA_JWT_RestAPI()  