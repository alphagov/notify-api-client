# GOVUK Notify API Client

A python api client for the GOVUK Notify platform.

This project is currently in the alpha phase and this client is presented as a work in progress
for discussions and conversations. It is not supported and is not to be used in production applications
at this stage.

## Installing

The client can be pulled into python applications using [pip](pip.readthedocs.org/).
 
Place the following line into the requirements.txt file in your application.
 
    git+https://github.com/alphagov/notify-api-client.git@0.0.4#egg=notify-api-client==0.0.4
    
Then install with

    pip install -r requirements.txt


The client has a managed release process and should your build should pull in a specific version. The developers will 
release new functionality / breaking changes into a new client release. The history can be found on the [github releases](https://github.com/alphagov/notify-api-client/releases) page.


## Usage

Prior to usage an account must be created through the notify admin console. This will allow access to the API credentials you application.

Once credentials have been obtained the client is initialised as follows:

    from notify_client import NotifyAPIClient
    
Then to send an SMS message

    NotifyAPIClient(auth_token='your-token-here').send_sms(mobile-number, message)

Where:

* "mobile-number" is the mobile phone number to deliver to
    * Only UK mobiles are supported
    * Must start with +44
    * Must not have leading zero
    * Must not have any whitespace, punctuation etc.
    * valid formt is +447777111222
    
* "message" is the text to send
    * Must be between 1 and 160 characters in length
    

## Errors

Errors are returned as subclasses of the APIError class.

    HTTPError wraps all standard status codes
    
    HTTP503Error is a special subclass to allow clients to determine whether to retry  
  
Both error classes contain the message from the API plus the status code. Example usage.

        try:
            NotifyAPIClient(auth_token='your-token-here').send_sms(
                '+447777111111',
                'message'
            )
            return 'success'
        except APIError as ex:
            log(ex.response.json())
            return 'error'
            
## Release process

To update the client:

* Ensure the version number in `notify_client/__init__.py` is bumped to reflect the changes (minor/major revisions and so on)
* Perform the merge of the branch to master
* run `./scripts/push-tag.sh`

The script will perform a git release of that new tag.
            