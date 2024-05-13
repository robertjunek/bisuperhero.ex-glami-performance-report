"""
Template Component main class.

"""
import logging
from datetime import datetime
import dateparser
from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

# configuration variables
KEY_API_TOKEN = '#api_token'
DATE_FROM = 'date_from'
INCREMENTAL_UPDATE = 'incremental_update'

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [KEY_API_TOKEN, DATE_FROM]
REQUIRED_IMAGE_PARS = []


class Component(ComponentBase):
    def __init__(self):
        super().__init__()

    def run(self):
        params = self.configuration.parameters
        DEFAULT_DAYS_AGO = 365

        # hidden_api_token is first 3 characters of the api_token and rest of the characters are replaced with '*'
        hidden_api_token = params.get(KEY_API_TOKEN)[:3] + '*' * (len(params.get(KEY_API_TOKEN)) - 3)

        logging.debug(f"Received date_from: {params.get(DATE_FROM)} \n"
                      f"Received incremental_update: {params.get(INCREMENTAL_UPDATE)} \n"
                      f"Received api_token: {hidden_api_token}")

        param_date_from = params.get(DATE_FROM, f"{DEFAULT_DAYS_AGO} days ago")

        date_from = dateparser.parse(param_date_from)
        if date_from is None:
            logging.error("Failed to parse 'dateFrom' parameter.")
            exit(1)

        formatted_date_from = date_from.strftime('%Y-%m-%d')
        date_to = datetime.today().strftime('%Y-%m-%d')

        logging.info(f"We will download data from {formatted_date_from} to {date_to}")


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
