#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(dict):
    databaseName = "dealerships"

    try:
        # Trying to authenticates with IBM Cloudant service 
        # using the username and api key
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    # Returing all the retrives databases
    return {"dbs": client.all_dbs()}

if __name__ == '__main__':

    temp_params = {
        "COUCH_URL": "NONE",
        "COUCH_USERNAME": "syncogame@gmail.com",
        "IAM_API_KEY": "NONE"
    }

    temp_selector = {
        'st': 'XX'
    }

    main(temp_params)