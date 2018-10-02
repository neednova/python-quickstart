import os
import base64
import requests

BORROW_LOAN_DECISION_THRESHOLD = 650

"""
For demo purposes, we'll store the results of a Nova Credit Passport in-memory via a global variable
Note that production usage should store received data in a database, associated to its respective applicant
"""
received_report_data = dict()

"""
Here's where the magic happens!
Parse the credit passport we received for a given applicant, such as storing applicant metadata and analyzing the tradeline data for underwriting purposes
"""
def parse_nova_passport(public_token, user_args, credit_passport):
    global received_report_data
    scores = credit_passport['scores']
    personal = credit_passport['personal']

    """
    Now that we have this data, you can easily add Nova to your existing underwriting engine.
    In this example, our underwriting decision is: accept applicants whose NOVA_SCORE_BETA is greater than BORROW_LOAN_DECISION_THRESHOLD
    """

    nova_score_obj = next(score for score in scores if score['score_type'] == 'NOVA_SCORE_BETA')

    # Make our decision:
    borrow_loan_decision = 'APPROVE' if nova_score_obj['value'] > BORROW_LOAN_DECISION_THRESHOLD else 'DENY'

    """
    Finally, store applicant report data - refresh the page at localhost:3000/dashboard to see the results

    For demo purposes, we'll store the results of a Nova Credit Passport in a cache store
    Note that production usage should store received data in a database, associated to its respective applicant
    """
    received_report_data = {
        'user_args': user_args,
        'public_token': public_token,
        'applicant_name': personal['full_name'],
        'applicant_email': personal['email'],
        'nova_score': nova_score_obj['value'],
        'borrow_loan_decision': borrow_loan_decision,
    }

# Logic for handling the webhook sent by Nova Credit to the callback url once an applicant's report status has changed
def handle_nova_webhook(public_token, user_args):
    nova_env = os.getenv('nova_env')
    nova_access_token_url = os.getenv('nova_access_token_url')
    nova_passport_url = os.getenv('nova_passport_url')
    nova_client_id = os.getenv('nova_client_id')
    nova_secret_key = os.getenv('nova_secret_key')
    nova_basic_auth_creds = base64.b64encode("{0}:{1}".format(nova_client_id, nova_secret_key).encode()).decode()

    access_token_response = requests.get(nova_access_token_url, headers={
        'Authorization': 'Basic ' + nova_basic_auth_creds, # Send client id, secret as Basic Auth, base-64 encoded
        'X-ENVIRONMENT': nova_env # Specify the environment the applicant used to make the request (sandbox or production)
    })

    # Now make a request to Nova to fetch the Credit Passport for the public token provided in the webhook (i.e., unique identifier for the credit file request in Nova's system)
    access_token = access_token_response.json()['accessToken']
    passport_response = requests.get(nova_passport_url, headers={
        'Authorization': 'Bearer ' + base64.b64encode(access_token.encode()).decode(), # Use Bearer Auth since have accessToken, base-64 encoded
        'X-ENVIRONMENT': nova_env, # Must match the environment of the NovaConnect widget and access token
        'X-PUBLIC-TOKEN': public_token #The unique Passport identifier sent in the callback
    })

    parse_nova_passport(public_token, user_args, passport_response.json())
