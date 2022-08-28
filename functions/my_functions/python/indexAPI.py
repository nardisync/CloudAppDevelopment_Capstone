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

databaseName = "reviews"

def main(dict):

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



def getAllReviewsWithSelector(dict, selector):
    
    try:
        # Trying to authenticates with IBM Cloudant service 
        # using the username and api key
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        # This call will return a Dict which content is all the entry in the database
        # 'databaseName' filtered by the selector. 
        reviewsDatabaseDocFiltered = client[databaseName].get_query_result(selector=selector, 
                                                                            raw_result=True)
        print("Element Filtered from Database: ")
        for elem in reviewsDatabaseDocFiltered['docs']:
            print(elem)


    except CloudantException as ce:
        if ce.status_code == 404:
            print("Code 404: dealerId does not exist")
            print({"Error:": ce })
            return {"Error": ce}
        elif ce.status_code == 500:
            print("Code 500: Something went wrong on the server")
            print({"Error:": ce })
            return {"Error": ce}
    
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("Connection error")
        return {"Error": err}

    # Returing all the retrives filtered entrys of the database
    return {"Databases Filtered : ": reviewsDatabaseDocFiltered}


def postReviewForDealership(dict, json_review):
    try:
        # Trying to authenticates with IBM Cloudant service 
        # using the username and api key
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        
        selector = {
            "id" : json_review['review']['id']
        }

        if not client[databaseName].get_query_result(selector=selector, raw_result=True)['docs']:
            print("Document does not exist")
            newDocument = reviewsDatabaseDocFiltered = client[databaseName].create_document(json_review["review"])
            if newDocument.exists():
                print(f"Document successfully created.")
        else :
            print("Document already exist")
            return "Document already exist"


    except CloudantException as ce:
        if ce.status_code == 500:
            print("Code 500: Something went wrong on the server")
            print({"Error:": ce })
            return {"Error": ce}
    
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("Connection error")
        return {"Error": err}

    return True






if __name__ == '__main__':

    temp_params = {
        "COUCH_URL": "NONE",
        "COUCH_USERNAME": "NONE",
        "IAM_API_KEY": "NONE"
    }

    temp_selector = {
        'dealership': {'$eq': 15}
    }
  
    temp_selector = {
        'dealership': 15
    }

    temp_review = {
        "review": 
        {
            "id": 1114,
            "name": "Upkar Lidder",
            "dealership": 15,
            "review": "Great service!",
            "purchase": 'false',
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021
        }
    }

    #main(temp_params)
    #getAllReviewsWithSelector(temp_params, temp_selector)
    postReviewForDealership(temp_params, temp_review)