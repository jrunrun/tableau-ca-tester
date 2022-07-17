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

from ca_list import ca_list

def auth_CA_JWT_RestAPI(ca):

    ts_server = ca['ts_server']
    ts_site = ca['ts_site']
    ts_username = ca['ts_username']
    ts_ca_iss = ca['ts_ca_iss']
    ts_ca_kid = ca['ts_ca_kid']
    ts_ca_secret = ca['ts_ca_secret']
    ts_serverType = ca['ts_serverType']
    ts_api_version = ca['ts_api_version']
    
    

    #logic to toggle between TS/TOL

    if ts_serverType == 'TOL':
        username =  ts_username + '@tableau.com'
    else:
        username =  ts_username

    logger.info("username value is {}".format(username))

    CA_SSO_token = jwt.encode(
        {
            "iss": ts_ca_iss,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes = 10),
            "jti": str(uuid.uuid4()),
            "aud": "tableau",
            "sub": username,
            "scp": ["tableau:content:read"]
        },
        ts_ca_secret,
        algorithm = "HS256",
            headers = {
                'kid': ts_ca_kid,
                'iss': ts_ca_iss
            }
        )

    
    auth_body = { "credentials": {'jwt': CA_SSO_token, "site": {"contentUrl": ts_site}} }
    headers = {
    'accept': 'application/json',
    'content-type': 'application/json'
    }

    ts_url = "{server}/api/{api_version}/auth/signin".format(server=ts_server, api_version=ts_api_version)
    now = datetime.datetime.utcnow()
    now_plus_10_min = datetime.datetime.utcnow() + datetime.timedelta(minutes = 5)
    # logger.debug("JWT time of encoding:{}".format(now))
    # logger.debug("JWT expiration time (+10 minutes):{}".format(now_plus_10_min))
    # logger.debug("request url:{}".format(ts_url))
    # logger.debug("request body:{}".format(auth_body))
    # logger.debug("request headers: {}".format(headers))

    # ADMIN AUTH TO REST API
    try:
        r = requests.post(ts_url, json= auth_body, headers=headers, verify=False)


    except requests.exceptions.RequestException as e: 
        logger.error(e)
        raise SystemExit(e)  

    if r.status_code == 200:
        logger.info('successful sign-in, received status code of {}'.format(str(r.status_code)))
        logger.info('site name of {}'.format(ts_site))
        logger.info('client ID of {}'.format(ts_ca_iss))
        response_auth = json.loads(r.content)
        logger.info(json.dumps(response_auth, indent=4))

    else:
        logger.info('unsuccessful sign-in, received status code of {}'.format(str(r.status_code)))
        logger.info('site name of {}'.format(ts_site))
        logger.info('client ID of {}'.format(ts_ca_iss))
        response_auth = json.loads(r.content)
        logger.info(json.dumps(response_auth, indent=4))
        # return ('Could not authenticate to tableau server api', str(r.status_code))    
        




# ts_server ='https://us-east-1.online.tableau.com'
# ts_site = 'wasabi'
# ts_username = 'n639986'
# ts_serverType = 'TOL'
# ts_ca_iss ='7f236b45-d72e-4ba6-b47a-cdac476d5ad6'
# ts_ca_kid ='542ad8a1-abc2-486b-9616-39dff87e64fe'
# ts_ca_secret = 'NKWKlD8HGZXRKj3RtQL/T5/lAGqY3mLIRa1GPeZm9n0='
# ts_api_version = '3.16'


for ca in ca_list:
    auth_CA_JWT_RestAPI(ca)  

