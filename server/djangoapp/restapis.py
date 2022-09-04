import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth



# A function to make HTTP GET requests.
# Return a JSON String
def get_request(url, dealerId=None, stateId=None, **kwargs):
    print("GET from {} ".format(url))
    try:
        if dealerId != None:
            print("Call Selector with Dealer ID")
            url += f"?id={dealerId}"
            print(f"URL: {url}")
            response = requests.get(url, 
                                    headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        elif stateId != None:
            print("Call Selector with Dealer State")
            url += f"?st={stateId}"
            print(f"URL: {url}")
            response = requests.get(url, 
                                    headers={'Content-Type': 'application/json'},
                                    params=kwargs )
        else:
            # Call get method of requests library with URL and parameters
            print("Classic Call, no Selector")
            response = requests.get(url, 
                                    headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(f"With status {status_code}.")
    print(response.text)
    json_data = json.loads(response.text)
    return json_data

# A function that process a JSON String into a CarDealer Object.
# Return a JSON String with all the CarDealer created
def car_dealer_from_json(json_result):
    results = []
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)



# A Function to get dealers from a cloud function
#   - Call get_request() with specified arguments
#   - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):

    # Call get_request with a URL parameter
    json_result = get_request(url)
    return car_dealer_from_json(json_result)


def get_dealer_by_id_from_cf(url, dealerId, **kwargs):

    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    

    return car_dealer_from_json(json_result)

def get_dealers_by_state(url, stateId, **kwargs):

    # Call get_request with a URL parameter
    json_result = get_request(url, stateId=stateId)

    return car_dealer_from_json(json_result)


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



if __name__ == '__main__':
    url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/syncogame%40gmail.com_djangoserver-space/CloudApp_FinalCapstone/getAllDealerships"
    print(f"get_dealers_from_cf: {get_dealers_from_cf(url)}")
    print("---------------------------")
    url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/syncogame%40gmail.com_djangoserver-space/CloudApp_FinalCapstone/getAllDealershipsWithState"
    print(f"get_dealers_from_cf: {get_dealer_by_id_from_cf(url, dealerId=15)}")
    print("---------------------------")
    print(f"get_dealers_from_cf: {get_dealers_by_state(url, stateId='TX')}")
    print("---------------------------")
