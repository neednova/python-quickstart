from flask import Flask, render_template, request
from dotenv import load_dotenv

import os
import utils

app = Flask(__name__)
load_dotenv()

"""
IMPORTANT! Your credentials should NOT be left unencrypted in your production integration
We recommend placing them in a hidden environment variable / file.
The variable file here is left unencrypted for demonstration purposes only
"""

nova_public_id = os.getenv('nova_public_id')
nova_env = os.getenv('nova_env')
nova_product_id = os.getenv('nova_product_id')

"""
Here is a sample loan application that has the NovaConnect widget added.
NovaConnect is a preconfigured modal pop up that gets attached with a single line of Javascript
More details: https://www.novacredit.com/quickstart-guide#clientside
"""
@app.route('/')
def application_loan():
    """
    Pass our Nova configs to the template so the widget can render
    We can also pass a string of data to `user_args` of NovaConnect, and this string will be returned in our webhook
    Example user_args: unique identifiers from your system, unique nonces for security
    """
    nova_user_args = 'borrow_loan_id_12345'
    return render_template('loan_application.html',
        nova_public_id = nova_public_id,
        nova_env = nova_env,
        nova_product_id = nova_product_id,
        nova_user_args = nova_user_args)

# Here is a sample internal dashboard, where your loan officer might view applicant profiles
@app.route('/dashboard')
def dashboard():
    # Pass the Nova Credit Passport data, if we've received it, to the dashboard view
    return render_template('dashboard.html', **utils.received_report_data)

"""
Route to handle Nova callback webhook, which you should specify on the dashboard as "https://your_domain_here.com/nova"
This route is POST'd to after an applicant completes NovaConnect, and we have updated the status of their NovaCredit Passport
When running this locally, you'll need a tunnel service like ngrok to expose your localhost: https://ngrok.com/
See our docs for a list of potential responses: https://docs.neednova.com/#error-codes-amp-responses
"""
@app.route('/nova', methods=['POST'])
def nova():
    request_json = request.get_json()
    status = request_json['status']
    public_token = request_json['publicToken']
    user_args = request_json['userArgs']

    app.logger.info('Received a callback to our webhook! Navigate your web browser to /dashboard to see the results');

    if status == 'SUCCESS':
        utils.handle_nova_webhook(public_token, user_args)
    else:
        """
        Handle unsuccessful statuses here, such as applicant NOT_FOUND and NOT_AUTHENTICATED
        For example, you might finalize your loan decision
        """
        app.logger.error('Report status %s received for Nova public token %s', status, public_token);

    return status
