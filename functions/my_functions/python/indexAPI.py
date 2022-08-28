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
import json


def main(dict):
    databaseName = "reviews"

    try:
        # Trying to authenticates with IBM Cloudant service 
        # using the username and api key
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        # This call will return a Dict which content is all the database called 'databaseName'. 
        reviewsDatabaseDoc = client.get(key=databaseName, remote=True).all_docs(include_docs=True)
        print(reviewsDatabaseDoc)
        print(type(reviewsDatabaseDoc["rows"]))

        # This Dict contains a Key called row that contains all the entries of the database 
        # as a List of Dict 
        # For each row of this entry, we use the Key doc for get all the info necessary
        for row in reviewsDatabaseDoc["rows"]:
            formated_row = json.dumps(row['doc'], sort_keys=True, indent=4)
            print(formated_row)
            print("--------------------")

    except CloudantException as ce:
        print("unable to connect")
        print({"Error:": ce})
        return {"error": ce}
    
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    # Returing all the retrives databases
    return {"dbs": client.all_dbs()}

if __name__ == '__main__':

    temp_params = {

    }

    temp_selector = {
        'st': 'XX'
    }

    main(temp_params)