# Nova Credit Python/Flask Sample App

Welcome to Nova Credit's Python/Flask sample application!

This app is designed to demonstrate how you might integrate with the Nova Credit ecosystem. Specifically, the sample integration shows how to do the following:

- Add the NovaConnect widget to your webpage, so applicants can request their foreign credit history be retrieved from their origin country
- Receive notification on the status of a foreign credit file and retrieve the data from the applicant's foreign credit file via serverside webhook
- Example of how you might parse the Nova Credit Passport data and integrate it into your existing underwriting

Please note that while these examples work, this sample app was designed for simplicity and clarity, rather than robustness. Comments are included within the source code to provide context and give best practice suggestions for how you might securely access and store Nova Credit data. These examples are not designed for production use out of the box. This example only provides access to fake, test data.



## Table of Contents

- [Requirements](#requirements)
- [Context](#context)
- [Getting set up](#getting-set-up)
- [Running the code](#run-via-heroku)
- [Resources](#resources)



## Requirements

- [Pipenv](https://docs.pipenv.org/)
- [ngrok](https://ngrok.com/) or [Heroku](https://www.heroku.com/) to test this source code quickly.
- [Nova Credit](https://dashboard.neednova.com/login) login ([request access](https://www.novacredit.com/request-access))



## Context

### Environment

Nova provides two environments: `sandbox` (suitable for developing and testing your integration) and `production` (for real applicants). The former provides a safe place for you to access Nova's resources and test different response types from the foreign credit bureaus using dummy data.

You will use the `sandbox` environment to test this app.

Be sure to use the sandbox credentials for the resource's environment you are requesting. Using the wrong credentials or tokens with your request usually leads to errors such as `UNKNOWN_CUSTOMER`.

### Callback URL

The Nova Credit ecosystem uses asynchronous webhooks to inform you when an international credit report status has changed (e.g.: found and retrieved report, could not authenticate applicant). This is to accommodate foreign credit reporting agencies' response times, which may take longer than generally accepted timeouts.

Nova will send an HTTP POST request to your specified `callback_url` once the report's status has changed. You can then use the identifiers provided by the webhook to retrieve a specific applicant's Passport. See how to configure this [below](#getting-set-up).

## Getting set up

1. Fork this repo to your own Github account.
2. Login to your Nova dashboard.
3. Copy and paste your `clientId`, `secretKey`, and `publicId` credentials from the `Developer` tab into the `.env` file of your cloned repo.
4. Copy a `productId` into your `.env` file. You can generate one by first creating a Product on your dashboard (found in the `Products` tab). You will then find the associated `productId` on the Developer tab.
5. Start the app by deploying your repository to [Heroku](#run-via-heroku) or running the app locally and [start an ngrok tunnel](#run-via-ngrok)
6. Save your `callback_url` in your Nova dashboard (found in the `Developer` tab).
   1. This should either be one of the following, based on whether you chose to test via ngrok or Heroku, **followed by the route you will use to receive the webhook**
        1. ngrok example: https://a15b052e.ngrok.io/nova
        2. Heroku example: https://limitless-crag-23820.herokuapp.com/nova
   2. Make sure to save it in the correct environment on the Nova dashboard (toggle `Use Test Data` so it is in `sandbox` mode).

## Run via Heroku

You may use the button below to deploy this source code to Heroku. This allows you to obtain a publicly accessible url so you can test the webhook callback. You will need to create or log in to your Heroku account. Please also note that your repository must be public in order for the button to work. Alternatively, you can see how to [change the button](https://devcenter.heroku.com/articles/heroku-button#private-github-repos) to accommodate a private repo.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Once you've successfully deployed your repository to Heroku, you may use the url they provide in your Nova callback.

## Run via ngrok

Alternatively, you may run this source code locally by exposing it to the internet via a tunnel. We recommend using [ngrok](https://ngrok.com). Here are the steps needed to configure ngrok:

1. Download and install [ngrok](https://ngrok.com/)
2. Expose your localhost by running "./ngrok http 5000" in your terminal
3. You will then be given a url provided by ngrok that allows external servers to reach your localhost. Make sure to use the `https` url in your Nova callback.

### Running the code with ngrok
1. `cd` to the project directory
2. Run the command: `pipenv install && pipenv shell`. To enter the pipenv shell.
3. Then run the command: `FLASK_APP=app.py flask run`. You should see a log in your terminal that the server is running and which port it is running on. You can now see the sample app at http://localhost:5000/.

## Testing the sample application
3. Navigate to the main `/` page (either via localhost or Heroku app). This is the sample loan application, which renders a NovaConnect widget configured with your Nova sandbox credentials.
4. Fill out NovaConnect. The fields will autopopulate a test applicant when you click "toggle sandbox inputs."
5. Once you have successfully sumitted NovaConnect, you will receive a `POST` request to your specified `callback_url` that the applicant's report status has changed.
6. Navigate to `/dashboard` (via your localhost or Heroku app). This renders a sample internal dashboard that your loan officers might use to make a credit decision.
   * Try changing the logic in `utils.py > parseNovaPassport` to see how you might use the Nova Credit Passport data!
   * If you are using Heroku, you will need to redeploy your app to see any code adjustments you make.

## Resources
- [Docs](https://docs.neednova.com/)
- [Quickstart](https://www.novacredit.com/quickstart-guide)
